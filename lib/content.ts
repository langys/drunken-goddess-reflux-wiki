import fs from 'node:fs';
import path from 'node:path';
import { randomUUID } from 'node:crypto';
import matter from 'gray-matter';
import { remark } from 'remark';
import remarkGfm from 'remark-gfm';
import remarkHtml from 'remark-html';
import { defaultSchema, type Schema } from 'hast-util-sanitize';
import { defaultHandlers, type Handler } from 'mdast-util-to-hast';
import type { Element } from 'hast';
import type { Image, Paragraph, PhrasingContent, Root } from 'mdast';
import { siteConfig } from '@/config/site.config';
import { slugifyHeading } from '@/lib/slug';
import { RESERVED_SLUGS } from '@/lib/legal';

export { slugifyHeading } from '@/lib/slug';

export type GuideHub = keyof typeof siteConfig.hubs;

export type GuideFrontmatter = {
  title: string;
  description: string;
  /** Hub key. Must exist in siteConfig.hubs — this is what forms the silo. */
  hub: GuideHub;
  /** URL segment: `<Game-Name>-<intent>`, e.g. `Phantom-Blade-Zero-beginner-guide`. */
  slug: string;
  published: string;
  modified?: string;
  /** 5 one-line bullets. Format: "<phrase>: <detail>". */
  quickGuide?: string[];
  faq?: { q: string; a: string }[];
  cards?: { title: string; body: string }[];
  image?: string;
  /** Descriptive alt for the cover image; falls back to the guide title. */
  imageAlt?: string;
  /** One-sentence context shown under the cover image. */
  imageCaption?: string;
};

export type Guide = GuideFrontmatter & {
  locale: string;
  href: string;
  excerpt: string;
  html?: string;
};

const CONTENT_ROOT = path.join(process.cwd(), 'content');

function readDir(locale: string) {
  const dir = path.join(CONTENT_ROOT, locale);
  return fs.existsSync(dir) ? dir : null;
}

/**
 * Coerces a frontmatter date to an ISO string.
 *
 * YAML parses an unquoted `published: 2026-09-14` into a Date object, and React
 * refuses to render one ("Objects are not valid as a React child"), which fails
 * the whole build at prerender time. Translations routinely write dates without
 * quotes while the English source quotes them, so this has to be handled in code
 * rather than left to content discipline.
 */
function asDateString(value: unknown): string {
  if (value instanceof Date) return value.toISOString().slice(0, 10);
  return typeof value === 'string' ? value : '';
}

function parse(filePath: string, locale: string): Guide {
  const raw = fs.readFileSync(filePath, 'utf8');
  const { data, content } = matter(raw);
  const fm = data as GuideFrontmatter;
  const prefix = locale === siteConfig.defaultLocale ? '' : `/${locale}`;
  const hub = fm.hub && fm.hub in siteConfig.hubs ? fm.hub : 'guide';
  const hubPath = siteConfig.hubs[hub].href;

  return {
    ...fm,
    hub,
    locale,
    published: asDateString(fm.published),
    modified: fm.modified ? asDateString(fm.modified) : undefined,
    href: `${prefix}${hubPath}/${fm.slug}`,
    excerpt: fm.description,
    html: content,
  };
}

/**
 * Per-locale cache.
 *
 * The header renders a nav dropdown from the guide list on every page, so an
 * uncached read means one full directory scan plus a file read per guide for
 * every prerendered page — on a 250-page site that is tens of thousands of
 * redundant reads during a single build.
 */
const guideCache = new Map<string, Guide[]>();

/** All guides for a locale, sorted by curated order in config/pages.ts if present. */
export function getAllGuides(locale: string = siteConfig.defaultLocale): Guide[] {
  const cached = guideCache.get(locale);
  if (cached) return cached;

  let pageOrderMap: Map<string, number> | null = null;
  try {
    const pages = (require('@/config/pages') as { pages: { slug: string }[] }).pages;
    pageOrderMap = new Map(pages.map((p, idx) => [p.slug, idx]));
  } catch {
    pageOrderMap = null;
  }

  const dir = readDir(locale);
  const guides = dir
    ? fs
        .readdirSync(dir)
        .filter((file) => file.endsWith('.md'))
        .map((file) => parse(path.join(dir, file), locale))
        .sort((a, b) => {
          if (pageOrderMap) {
            const indexA = pageOrderMap.get(a.slug) ?? 9999;
            const indexB = pageOrderMap.get(b.slug) ?? 9999;
            if (indexA !== indexB) return indexA - indexB;
          }
          return a.published < b.published ? 1 : -1;
        })
    : [];

  guideCache.set(locale, guides);
  return guides;
}

/**
 * Cross-checks content files against config/pages.ts.
 *
 * The two are maintained separately — pages.ts is generated from a keyword CSV,
 * markdown is written by hand — so they drift silently: a missing file becomes a
 * 404 that is only discovered after deploy. Calling this from
 * generateStaticParams turns that into a build-time warning instead.
 */
export function validateContentCoverage(locale: string = siteConfig.defaultLocale) {
  let declared: { slug: string }[] = [];
  try {
    declared = (require('@/config/pages') as { pages: { slug: string }[] }).pages;
  } catch {
    return { missing: [], orphaned: [] as string[] };
  }

  const onDisk = new Set(getAllGuides(locale).map((guide) => guide.slug));
  const inManifest = new Set(declared.map((page) => page.slug));

  // The manifest declares the full default-language catalog. Partial
  // translations are expected; their navigation already uses real files only.
  const missing = locale === siteConfig.defaultLocale
    ? [...inManifest].filter((slug) => !onDisk.has(slug)) : [];
  const orphaned = [...onDisk].filter((slug) => !inManifest.has(slug));

  if (missing.length > 0) {
    console.warn(
      `[content] ${missing.length} page(s) in config/pages.ts have no markdown file — ` +
        `the hub listing will link to 404s:\n  ${missing.join('\n  ')}`,
    );
  }
  if (orphaned.length > 0) {
    console.warn(
      `[content] ${orphaned.length} markdown file(s) are missing from config/pages.ts ` +
        `(they will not appear in listings):\n  ${orphaned.join('\n  ')}`,
    );
  }

  return { missing, orphaned };
}

export function getGuideBySlug(locale: string, slug: string): Guide | undefined {
  return getAllGuides(locale).find((guide) => guide.slug === slug);
}

export function getGuidesByHub(locale: string, hub: GuideHub): Guide[] {
  return getAllGuides(locale).filter((guide) => guide.hub === hub);
}

/**
 * Related guides for the silo. Same hub only — cross-hub linking is what turns a
 * clean hub-and-spoke structure into an undifferentiated link soup.
 */
export function getRelatedGuides(locale: string, current: Guide, limit = 3): Guide[] {
  return getGuidesByHub(locale, current.hub)
    .filter((guide) => guide.slug !== current.slug)
    .slice(0, limit);
}

/**
 * Locales that actually have at least one translated guide.
 *
 * A locale is often added to site.config.ts before its content is written. If the
 * sitemap and generateStaticParams use the raw locale list, those placeholder
 * locales produce sitemap entries that 404 — the fastest way to lose crawl trust.
 * Gating on real content keeps the sitemap honest at every stage of the rollout.
 */
/**
 * Every hub and hub/slug path that exists per locale.
 *
 * The locale switcher uses this to keep the reader on the same page when a
 * translation exists, and to fall back to the locale home when it does not —
 * partial translation coverage is the normal state, so a switcher that links to
 * untranslated pages would 404 constantly.
 */
export function getLocaleRoutes(): Record<string, string[]> {
  const map: Record<string, string[]> = {};
  for (const locale of siteConfig.locales) {
    const guides = getAllGuides(locale);
    if (guides.length === 0) {
      map[locale] = [];
      continue;
    }
    const hubs = Object.keys(siteConfig.hubs).filter((key) => guides.some((guide) => guide.hub === key)).map((key) =>
      siteConfig.hubs[key as keyof typeof siteConfig.hubs].href.replace(/^\//, ''),
    );
    map[locale] = [
      ...hubs,
      ...guides.map((g) => `${siteConfig.hubs[g.hub].href.replace(/^\//, '')}/${g.slug}`),
      ...RESERVED_SLUGS,
    ];
  }
  return map;
}

const contentLocaleCache: { value: string[] | null } = { value: null };

export function localesWithContent(): string[] {
  if (contentLocaleCache.value) return contentLocaleCache.value;
  contentLocaleCache.value = siteConfig.locales.filter(
    (locale) => getAllGuides(locale).length > 0,
  );
  return contentLocaleCache.value;
}

export type TocItem = {
  id: string;
  text: string;
  level: number;
};

export function extractToc(markdown: string): TocItem[] {
  const items: TocItem[] = [];
  const lines = markdown.split('\n');
  let inCode = false;

  for (const line of lines) {
    if (line.trim().startsWith('```')) {
      inCode = !inCode;
      continue;
    }
    if (inCode) continue;

    const match = line.match(/^(#{2,3})\s+(.+)$/);
    if (match) {
      const level = match[1].length;
      const rawText = match[2].trim();
      const cleanText = rawText
        .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
        .replace(/[*_`]/g, '')
        .trim();
      const id = slugifyHeading(cleanText);
      if (id) {
        items.push({ id, text: cleanText, level });
      }
    }
  }

  return items;
}

export type ArticleVideo = { id: string; title: string; start?: number };
export type ArticlePart = { type: 'html'; html: string } | { type: 'video'; video: ArticleVideo };

function parseArticleVideo(rawUrl: string, title: string | null | undefined): ArticleVideo | null {
  if (!title?.trim()) return null;

  try {
    const url = new URL(rawUrl);
    if (url.protocol !== 'https:' || url.username || url.password || url.port || url.hash) return null;
    const host = url.hostname.toLowerCase();
    let id: string | null = null;
    const paths = url.pathname.split('/');
    const youtubeHosts = ['youtube.com', 'www.youtube.com', 'm.youtube.com', 'youtube-nocookie.com', 'www.youtube-nocookie.com'];
    if (youtubeHosts.includes(host)) {
      if (url.pathname === '/watch' && url.searchParams.getAll('v').length === 1) {
        id = url.searchParams.get('v');
      } else if (paths.length === 3 && ['embed', 'shorts'].includes(paths[1])) {
        id = paths[2];
      }
    } else if (host === 'youtu.be' && paths.length === 2) {
      id = paths[1];
    }
    if (!id || !/^[a-zA-Z0-9_-]{11}$/.test(id)) return null;

    const times = [...url.searchParams.getAll('t'), ...url.searchParams.getAll('start')];
    if (times.length > 1 || (times.length === 1 && !/^\d+$/.test(times[0]))) return null;
    const start = times.length ? Number(times[0]) : undefined;
    if (start !== undefined && !Number.isSafeInteger(start)) return null;
    return { id, title: title.trim(), start };
  } catch {
    return null;
  }
}

const imageSizeCache = new Map<string, { width: number; height: number }>();

function imageDimensions(src: string): { width: number; height: number } | undefined {
  const cached = imageSizeCache.get(src);
  if (cached) return cached;

  let size: { width: number; height: number } | undefined;
  const configured = (siteConfig.media as any).imageSizes?.[src];
  if (configured && configured.width > 0 && configured.height > 0) {
    size = configured;
  } else if (src.startsWith('/') && !src.startsWith('//')) {
    try {
      const pathname = decodeURIComponent(new URL(src, 'https://local.invalid').pathname);
      const root = fs.realpathSync(path.join(process.cwd(), 'public'));
      const filename = fs.realpathSync(path.resolve(root, `.${pathname}`));
      if (filename.startsWith(`${root}${path.sep}`)) {
        // Next bundles the image header reader used by <Image>; keep the renderer
        // dependency-free and read dimensions exactly as the framework does.
        const imageSize = require('next/dist/compiled/image-size') as (data: Buffer) => { width?: number; height?: number };
        const { width, height } = imageSize(fs.readFileSync(filename));
        if (width && height) size = { width, height };
      }
    } catch {
      // Remote, missing and unsupported images use the bounded fallback in CSS.
    }
  }
  if (size) imageSizeCache.set(src, size);
  return size;
}

const markdownImage: Handler = (state, node: Image) => {
  const result = defaultHandlers.image(state, node);
  if (result && !Array.isArray(result) && result.type === 'element') {
    Object.assign(result.properties, { loading: 'lazy', decoding: 'async', ...imageDimensions(node.url) });
  }
  return result;
};

const markdownParagraph: Handler = (state, node: Paragraph) => {
  const [image, next, ...rest] = node.children;
  // A second image in the same paragraph is not caption text; keep both inline
  // rather than nesting one image inside another image's figcaption.
  const captionHasImage = rest.some((item) => item.type === 'image');
  const standalone = image?.type === 'image' && !captionHasImage && (node.children.length === 1 ||
    next?.type === 'text' && (next.value.startsWith('\n') || !next.value.trim() && rest.length > 0));
  if (!standalone || image.type !== 'image') return defaultHandlers.paragraph(state, node);

  const imageElement = state.one(image, node);
  if (!imageElement || Array.isArray(imageElement)) return defaultHandlers.paragraph(state, node);
  const children: Element['children'] = [imageElement];
  const caption: PhrasingContent[] | null = next?.type === 'text'
    ? [{ ...next, value: next.value.replace(/^\n/, '') }, ...rest]
    : image.title?.trim() ? [{ type: 'text', value: image.title }] : null;
  if (caption?.some((item) => item.type !== 'text' || item.value.trim())) {
    children.push({ type: 'element', tagName: 'figcaption', properties: {}, children: state.all({ ...node, children: caption }) });
  }
  return { type: 'element', tagName: 'figure', properties: {}, children };
};

const articleSchema: Schema = {
  ...defaultSchema,
  tagNames: [...(defaultSchema.tagNames ?? []), 'figure', 'figcaption'],
  attributes: {
    ...defaultSchema.attributes,
    img: [...(defaultSchema.attributes?.img ?? []), ['loading', 'lazy'], ['decoding', 'async']],
  },
};

export async function renderMarkdown(markdown: string): Promise<ArticlePart[]> {
  const videos = new Map<string, ArticleVideo>();
  const markerPrefix = `article-video-${randomUUID()}-`;
  const processed = await remark()
    .use(remarkGfm)
    .use(() => (tree: Root) => {
      tree.children.forEach((node) => {
        if (node.type !== 'paragraph' || node.children.length !== 2) return;
        const [prefix, link] = node.children;
        if (prefix.type !== 'text' || prefix.value.trim() !== '@' || link.type !== 'link' ||
            link.children.length !== 1 || link.children[0].type !== 'text' || link.children[0].value !== 'youtube') return;
        const video = parseArticleVideo(link.url, link.title);
        if (!video) return;
        const marker = `${markerPrefix}${videos.size}`;
        videos.set(marker, video);
        node.children = [{ type: 'text', value: marker }];
      });
    })
    .use(remarkHtml, { sanitize: articleSchema, handlers: { image: markdownImage, paragraph: markdownParagraph } })
    .process(markdown);
  let html = processed.toString();

  // Keep the heading IDs aligned with the separately rendered table of contents.
  const toc = extractToc(markdown);
  let headingIndex = 0;
  html = html.replace(/<(h[23])>(.*?)<\/\1>/gis, (_match, tag, inner) => {
    const item = toc[headingIndex++];
    if (!item || item.level !== Number(tag[1])) {
      throw new Error('Markdown headings and table of contents are out of sync');
    }
    return `<${tag} id="${item.id}">${inner}</${tag}>`;
  });
  if (headingIndex !== toc.length) {
    throw new Error('Markdown headings and table of contents are out of sync');
  }

  const parts: ArticlePart[] = [];
  let remaining = html;
  for (const [marker, video] of videos) {
    const placeholder = `<p>${marker}</p>`;
    const offset = remaining.indexOf(placeholder);
    if (offset < 0) continue;
    const previous = remaining.slice(0, offset);
    if (previous.trim()) parts.push({ type: 'html', html: previous });
    parts.push({ type: 'video', video });
    remaining = remaining.slice(offset + placeholder.length);
  }
  if (remaining.trim()) parts.push({ type: 'html', html: remaining });
  return parts;
}
