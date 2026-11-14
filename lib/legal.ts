import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';
import { remark } from 'remark';
import remarkGfm from 'remark-gfm';
import remarkHtml from 'remark-html';
import { siteConfig } from '@/config/site.config';

export type LegalPage = {
  slug: string;
  title: string;
  description: string;
  updated?: string;
  html: string;
};

/**
 * Path segments the catch-all route must NOT treat as hubs, because dedicated
 * top-level routes own them. Keep in sync with app/[locale]/* static folders.
 */
export const RESERVED_SLUGS = ['about', 'contact', 'privacy', 'terms', 'search'] as const;

export function isReservedSlug(slug: string) {
  return (RESERVED_SLUGS as readonly string[]).includes(slug);
}

export const LEGAL_SLUGS = ['about', 'contact', 'privacy', 'terms'] as const;

const LEGAL_ROOT = path.join(process.cwd(), 'content', 'legal');

function readLegalFile(slug: string, locale: string) {
  const localized = path.join(LEGAL_ROOT, locale, `${slug}.md`);
  const fallback = path.join(LEGAL_ROOT, `${slug}.md`);
  const file = fs.existsSync(localized) ? localized : fallback;
  if (!fs.existsSync(file)) return null;
  return fs.readFileSync(file, 'utf8');
}

/**
 * Substitutes tokens that come from config into legal copy.
 *
 * Content files must not hardcode the contact address: one operator runs many
 * sites, and an address baked into markdown gets stale the moment it changes.
 * Any `{{token}}` left unresolved is stripped so a typo cannot leak braces onto
 * a published page.
 */
function substituteTokens(text: string): string {
  const tokens: Record<string, string> = {
    contactEmail: siteConfig.contactEmail,
    siteName: siteConfig.fullName,
    gameName: siteConfig.name,
  };

  return text
    .replace(/\{\{(\w+)\}\}/g, (match, key: string) => tokens[key] ?? '')
    .replace(/[ \t]{2,}/g, ' ');
}

/**
 * Legal pages fall back to the default locale rather than 404ing.
 *
 * These pages exist so the site has the disclosure surface that search engines
 * and ad networks require. A missing privacy policy in a secondary locale is far
 * worse than one shown in English, so an untranslated page degrades instead of
 * disappearing.
 */
export async function getLegalPage(slug: string, locale: string): Promise<LegalPage | null> {
  const raw = readLegalFile(slug, locale);
  if (!raw) return null;

  const { data, content } = matter(raw);
  const html = (
    await remark().use(remarkGfm).use(remarkHtml, { sanitize: false }).process(substituteTokens(content))
  ).toString();

  return {
    slug,
    title: substituteTokens((data.title as string) ?? slug),
    description: substituteTokens((data.description as string) ?? `${siteConfig.fullName} ${slug}`),
    updated: data.updated as string | undefined,
    html,
  };
}
