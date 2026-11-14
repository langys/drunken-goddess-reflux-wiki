export type Placement = { key: string; scriptUrl: string; enabled?: boolean };
export type AdSize = { width: number; height: number };
type Claim = { host: HTMLElement; page: object };

declare global {
  interface Window {
    atOptions?: { key: string; format: string; width: number; height: number; params: Record<string, unknown> };
    __adSlotQueue?: Promise<void>;
  }
}

const claims = new Map<string, Claim>();
let currentPage = { pathname: '', identity: {} };

export function validAdsterraPlacement(placement: Placement, format: 'banner' | 'native'): boolean {
  if (placement.enabled === false) return false;
  if (!/^[a-f0-9]{32}$/i.test(placement.key)) return false;
  try {
    const url = new URL(placement.scriptUrl);
    return url.origin === 'https://bauval.org' &&
      url.pathname === `/${format === 'native' ? '21' : '22'}/${placement.key}` &&
      !url.search && !url.hash && !url.username && !url.password;
  } catch {
    return false;
  }
}

/** One request per key per page. Connected persistent slots also own their key after navigation. */
export function observeAdsterraSlot(
  host: HTMLElement,
  placement: Placement,
  size?: AdSize,
  { delayMs = 0, rootMargin = 350 }: { delayMs?: number; rootMargin?: number } = {},
): () => void {
  if (!validAdsterraPlacement(placement, size ? 'banner' : 'native')) return () => {};
  if (currentPage.pathname !== window.location.pathname) {
    currentPage = { pathname: window.location.pathname, identity: {} };
    // Keep connected persistent owners; discard old page records to bound memory.
    for (const [key, claim] of claims) if (!claim.host.isConnected) claims.delete(key);
  }
  const page = currentPage.identity;
  let cancelled = false;
  let scheduled = false;
  let near = false;
  let ownClaim: Claim | undefined;
  let timer: ReturnType<typeof setTimeout> | undefined;

  const fits = () => {
    const rect = host.getBoundingClientRect();
    const style = window.getComputedStyle(host);
    return host.isConnected && host.getClientRects().length > 0 && rect.height > 0 &&
      style.visibility !== 'hidden' && style.opacity !== '0' && (!size || rect.width >= size.width);
  };
  const unclaim = () => {
    if (ownClaim && claims.get(placement.key) === ownClaim && host.dataset.adState === 'queued') {
      claims.delete(placement.key);
      host.dataset.adState = 'idle';
    }
    scheduled = false;
  };
  const inject = (): Promise<void> => {
    if (cancelled || !near || !fits()) {
      unclaim();
      return Promise.resolve();
    }
    host.dataset.adState = 'loading';
    return new Promise<void>((resolve) => {
      try {
        if (size) {
          // Assign immediately before execution; never declare a non-configurable global var.
          window.atOptions = { key: placement.key, format: 'iframe', ...size, params: {} };
        } else {
          // Render this in HTML, before the SDK's pushState/popstate handler runs.
          // Recreating it here loses route fills and triggers the SDK's duplicate-key guard.
          if (!host.querySelector(`#container-${placement.key}`)) throw new Error('Missing Native container');
        }
        const script = document.createElement('script');
        script.async = true;
        script.setAttribute('data-cfasync', 'false');
        script.src = placement.scriptUrl;
        script.onload = () => { host.dataset.adState = 'loaded'; resolve(); };
        script.onerror = () => { host.dataset.adState = 'error'; resolve(); };
        host.appendChild(script);
      } catch {
        host.dataset.adState = 'error';
        resolve();
      }
    });
  };
  const load = () => {
    timer = undefined;
    if (cancelled || scheduled || !near || !fits()) return;
    const owner = claims.get(placement.key);
    if (owner) {
      if (owner.host === host) return; // Strict Mode and repeated effects never inject twice.
      if (owner.page === page || owner.host.isConnected) {
        host.dataset.adState = 'duplicate';
        return;
      }
    }
    scheduled = true;
    ownClaim = { host, page };
    claims.set(placement.key, ownClaim);
    host.dataset.adState = 'queued';
    if (size) {
      const previous = window.__adSlotQueue ?? Promise.resolve();
      const next = previous.then(inject, inject);
      // Release only on load/error: a timeout must not let a late script read another key.
      window.__adSlotQueue = next.then(() => {}, () => {});
    } else {
      void inject();
    }
  };
  const check = () => {
    if (!near || !fits() || scheduled || timer !== undefined) return;
    if (delayMs > 0) timer = setTimeout(load, delayMs);
    else load();
  };
  const intersection = typeof IntersectionObserver === 'undefined' ? undefined : new IntersectionObserver(
    (entries) => { near = entries.some((entry) => entry.isIntersecting); check(); },
    { rootMargin: `${rootMargin}px 0px` },
  );
  const fallback = () => {
    const rect = host.getBoundingClientRect();
    near = rect.bottom >= -rootMargin && rect.top <= window.innerHeight + rootMargin;
    check();
  };
  const resize = typeof ResizeObserver === 'undefined' ? undefined : new ResizeObserver(check);
  intersection?.observe(host);
  resize?.observe(host);
  window.addEventListener('resize', fallback);
  if (!intersection) {
    window.addEventListener('scroll', fallback, { passive: true });
    fallback();
  }
  return () => {
    cancelled = true;
    if (timer !== undefined) clearTimeout(timer);
    intersection?.disconnect();
    resize?.disconnect();
    window.removeEventListener('resize', fallback);
    window.removeEventListener('scroll', fallback);
    // Preserve started scripts/creatives on effect replay; React removes an unmounted host.
    unclaim();
  };
}
