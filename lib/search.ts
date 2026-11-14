import { siteConfig } from '@/config/site.config';

export type SearchEntry = {
  slug: string;
  locale: string;
  hub: string;
  title: string;
  description: string;
  headings: string[];
  text: string;
};

export type Scored = { entry: SearchEntry; score: number; matchedHeading?: string };

export type TextSegment = { text: string; match: boolean };

/**
 * Deliberately simple scoring: exact title match beats prefix beats body match,
 * with a bonus for every distinct query token found. A fuzzy-search library
 * would add tens of kilobytes to do the same job for a few hundred pages.
 */
function scoreEntry(entry: SearchEntry, tokens: string[]): Scored | null {
  const title = entry.title.toLowerCase();
  const description = entry.description.toLowerCase();
  const headings = entry.headings.map((h) => h.toLowerCase());
  const text = entry.text.toLowerCase();

  let score = 0;
  let matchedHeading: string | undefined;

  for (const token of tokens) {
    let tokenScore = 0;
    if (title === token) tokenScore += 60;
    else if (title.startsWith(token)) tokenScore += 40;
    else if (title.includes(token)) tokenScore += 25;
    if (description.includes(token)) tokenScore += 10;

    const headingIndex = headings.findIndex((h) => h.includes(token));
    if (headingIndex >= 0) {
      tokenScore += 8;
      matchedHeading ??= entry.headings[headingIndex];
    }

    if (text.includes(token)) tokenScore += 4;
    if (tokenScore === 0) return null; // every token must match somewhere
    score += tokenScore;
  }

  return { entry, score, matchedHeading };
}

/** Splits a query the same way scoring does, so highlights match the ranking. */
export function queryTokens(query: string): string[] {
  return query.toLowerCase().split(/\s+/).filter((t) => t.length > 1);
}

function escapeRegExp(value: string) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Splits text into matching and non-matching segments.
 *
 * Returning data rather than HTML keeps this XSS-safe with no sanitizer: page
 * titles are authored content, but a search box is exactly the kind of place
 * where injected markup would otherwise become reachable.
 */
export function highlightSegments(text: string, tokens: string[]): TextSegment[] {
  if (!text || tokens.length === 0) return [{ text, match: false }];

  const pattern = new RegExp(`(${tokens.map(escapeRegExp).join('|')})`, 'gi');
  // Match against the token set rather than re-testing the /g/ regex: a global
  // regex carries lastIndex between calls, so .test() in a loop returns
  // alternating results and would highlight only every other occurrence.
  const lowered = new Set(tokens.map((token) => token.toLowerCase()));

  return text.split(pattern).filter(Boolean).map((part) => ({
    text: part,
    match: lowered.has(part.toLowerCase()),
  }));
}

export function searchEntries(entries: SearchEntry[], query: string, limit = 8): Scored[] {
  const tokens = queryTokens(query);
  if (tokens.length === 0) return [];

  return entries
    .map((entry) => scoreEntry(entry, tokens))
    .filter((result): result is Scored => result !== null)
    .sort((a, b) => b.score - a.score || a.entry.title.localeCompare(b.entry.title))
    .slice(0, limit);
}

/** Hub href for a search entry, falling back to the first configured hub. */
export function hubHref(hub: string) {
  // Legal pages are top-level routes, not spokes under a hub.
  if (hub === 'legal') return '';
  const hubs = siteConfig.hubs as Record<string, { href: string }>;
  const fallback = Object.values(hubs)[0]?.href ?? '/guide';
  return hubs[hub]?.href ?? fallback;
}

/** Full, locale-aware href for a search entry. */
export function entryHref(prefix: string, entry: SearchEntry) {
  const hub = hubHref(entry.hub);
  return hub ? `${prefix}${hub}/${entry.slug}` : `${prefix}/${entry.slug}`;
}
