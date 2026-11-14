const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { test } = require('node:test');
const vm = require('node:vm');
const ts = require('typescript');
const source = ts.transpileModule(readFileSync('lib/adsterra.ts', 'utf8'), {
  compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS },
}).outputText;
const key = (letter) => letter.repeat(32);
const placement = (letter, format = 'banner') => ({ key: key(letter), scriptUrl: `https://bauval.org/${format === 'native' ? '21' : '22'}/${key(letter)}` });
const tick = () => new Promise((resolve) => setTimeout(resolve, 10));

function environment() {
  const requests = [];
  const listeners = new Map();
  const window = {
    location: { pathname: '/first' }, innerHeight: 900,
    getComputedStyle: (host) => ({ visibility: host.hidden ? 'hidden' : 'visible', opacity: '1' }),
    addEventListener: (type, callback) => {
      if (!listeners.has(type)) listeners.set(type, new Set());
      listeners.get(type).add(callback);
    },
    removeEventListener: (type, callback) => listeners.get(type)?.delete(callback),
  };
  const document = { createElement: (tagName) => ({ tagName, style: {}, setAttribute(name, value) { this[name] = value; } }) };
  const context = { window, document, exports: {}, URL, setTimeout, clearTimeout };
  vm.runInNewContext(source, context);
  function host(width = 728, hidden = false) {
    return {
      dataset: {}, children: [], isConnected: true, hidden, width,
      getBoundingClientRect() { return { width: this.width, height: 250, top: 0, bottom: 250 }; },
      getClientRects() { return this.hidden ? [] : [this.getBoundingClientRect()]; },
      querySelector(selector) { return this.children.find((child) => `#${child.id}` === selector); },
      appendChild(child) {
        this.children.push(child);
        if (child.tagName === 'script') requests.push({ child, options: window.atOptions && { ...window.atOptions }, host: this });
      },
    };
  }
  return { ...context.exports, window, requests, host,
    resize() { for (const callback of listeners.get('resize') ?? []) callback(); },
    load(host, letter, size = { width: 728, height: 90 }) {
      // Native's destination is part of server-rendered HTML, as in AdPlacement.
      if (!size && !host.querySelector(`#container-${key(letter)}`)) {
        host.appendChild({ tagName: 'div', id: `container-${key(letter)}`, style: {} });
      }
      return context.exports.observeAdsterraSlot(host, placement(letter, size ? 'banner' : 'native'), size);
    },
  };
}

test('serial Banner execution preserves each key and load/error advance the queue; Native is independent', async () => {
  const e = environment();
  e.load(e.host(), 'a');
  e.load(e.host(), 'b');
  e.load(e.host(), 'c', null);
  assert.equal(e.requests.length, 1); // Native starts immediately, before the Banner queue's microtask.
  const native = e.requests[0];
  assert.equal(native.child.src, placement('c', 'native').scriptUrl);
  await tick();
  assert.deepEqual(e.requests.map((r) => r.child.src), [placement('c', 'native').scriptUrl, placement('a').scriptUrl]);
  assert.equal(native.child.async, true);
  assert.equal(native.child['data-cfasync'], 'false');
  assert.equal(e.window.atOptions.key, key('a')); // B cannot overwrite a slow A.
  e.requests[1].child.onerror();
  await tick();
  const second = e.requests.find((r) => r.child.src === placement('b').scriptUrl);
  assert.equal(second.options.key, key('b'));
  assert.equal(second.child.async, true);
  assert.equal(second.child['data-cfasync'], 'false');
  second.child.onload();
  assert.equal(second.host.dataset.adState, 'loaded');
  assert.equal(native.host.children[0].id, `container-${key('c')}`);
});

test('Native preserves its pre-rendered container and a route fill received before lazy initialization', async () => {
  const e = environment();
  const host = e.host();
  const target = { tagName: 'div', id: `container-${key('a')}`, style: {}, textContent: 'SDK route fill' };
  host.appendChild(target);
  e.load(host, 'a', null);
  await tick();
  assert.equal(host.children.filter((child) => child.id === target.id).length, 1);
  assert.equal(host.children[0], target);
  assert.equal(target.textContent, 'SDK route fill');
  assert.equal(e.requests.length, 1);
  const missing = e.host();
  e.observeAdsterraSlot(missing, placement('b', 'native'), undefined, { delayMs: 0 });
  await tick();
  assert.equal(missing.dataset.adState, 'error');
  assert.equal(e.requests.length, 1); // Missing destinations must not consume the SDK's key guard.
});

test('duplicate components, Strict Mode effect replay and same-page remount request a key once', async () => {
  const e = environment();
  const first = e.host();
  const cleanup = e.load(first, 'a', null);
  e.load(e.host(), 'a', null);
  await tick();
  cleanup();
  e.load(first, 'a', null);
  first.isConnected = false;
  e.load(e.host(), 'a', null);
  await tick();
  assert.equal(e.requests.length, 1);
});

test('cancelled queued work cannot remove a replacement claim or execute on an old article', async () => {
  const e = environment();
  e.load(e.host(), 'a');
  const second = e.host();
  const cancel = e.load(second, 'b');
  await tick();
  cancel();
  e.load(second, 'b');
  await tick();
  e.requests[0].child.onload();
  await tick();
  assert.equal(e.requests.length, 2);
  assert.equal(e.requests[1].options.key, key('b'));
  const old = e.host();
  const stop = e.load(old, 'd');
  await tick();
  old.isConnected = false;
  stop();
  e.requests[1].child.onload();
  await tick();
  assert.equal(e.requests.length, 2);
});

test('route navigation preserves connected persistent owners and allows one new article instance per page', async () => {
  const e = environment();
  const persistent = e.host();
  const article = e.host();
  e.load(persistent, 'a', null);
  e.load(article, 'b', null);
  await tick();
  article.isConnected = false;
  e.window.location.pathname = '/second';
  e.load(e.host(), 'a', null);
  const nextArticle = e.host();
  e.load(nextArticle, 'b', null);
  await tick();
  assert.deepEqual(e.requests.map((r) => r.child.src), [placement('a', 'native').scriptUrl, placement('b', 'native').scriptUrl, placement('b', 'native').scriptUrl]);
  nextArticle.isConnected = false;
  e.window.location.pathname = '/first';
  e.load(e.host(), 'b', null);
  await tick();
  assert.equal(e.requests.length, 4);
});

test('hidden, narrow and invalid placements do not request; resizing activates an eligible Banner once', async () => {
  const e = environment();
  const narrow = e.host(390);
  const hidden = e.host(728, true);
  e.load(narrow, 'a');
  e.load(hidden, 'b');
  e.observeAdsterraSlot(e.host(), { key: '0', scriptUrl: '' });
  assert.equal(e.validAdsterraPlacement({ key: key('a'), scriptUrl: placement('b').scriptUrl }, 'banner'), false);
  assert.equal(e.validAdsterraPlacement({ key: key('a'), scriptUrl: `https://evil.example/22/${key('a')}` }, 'banner'), false);
  await tick();
  assert.equal(e.requests.length, 0);
  narrow.width = 728;
  e.resize();
  await tick();
  assert.equal(e.requests.length, 1);
  e.requests[0].child.onload();
  e.resize();
  await tick();
  assert.equal(e.requests.length, 1);
});

test('Banner and Native accept their own bauval entrypoints; stale, mismatched and disabled placements do not request', async () => {
  const e = environment();
  assert.equal(e.validAdsterraPlacement(placement('a'), 'banner'), true);
  assert.equal(e.validAdsterraPlacement(placement('a', 'native'), 'native'), true);
  for (const format of ['banner', 'native']) {
    const valid = placement('a', format);
    const wrongFormat = placement('a', format === 'native' ? 'banner' : 'native');
    const invalid = [
      wrongFormat,
      { ...valid, enabled: false },
      { ...valid, key: '0' },
      { ...valid, scriptUrl: '' },
      { ...valid, scriptUrl: `https://www.highrevenueformat.com/${key('a')}/invoke.js` },
      { ...valid, scriptUrl: `https://pl00000000.profitableratecpmnetwork.com/${key('a')}/invoke.js` },
      { ...valid, scriptUrl: valid.scriptUrl + '/invoke.js' },
      { ...valid, scriptUrl: valid.scriptUrl + '?legacy=1' },
      { ...valid, scriptUrl: valid.scriptUrl + '#legacy' },
      { ...valid, scriptUrl: valid.scriptUrl.replace('https:', 'http:') },
      { ...valid, scriptUrl: valid.scriptUrl.replace('bauval.org', 'bauval.org.example') },
    ];
    for (const candidate of invalid) {
      assert.equal(e.validAdsterraPlacement(candidate, format), false, candidate.scriptUrl);
      e.observeAdsterraSlot(e.host(), candidate, format === 'banner' ? { width: 728, height: 90 } : undefined);
    }
  }
  await tick();
  assert.equal(e.requests.length, 0);
});
