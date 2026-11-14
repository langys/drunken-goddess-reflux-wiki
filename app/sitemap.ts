import type { MetadataRoute } from 'next';
import { siteConfig } from '@/config/site.config';
import { getAllGuides, localesWithContent } from '@/lib/content';
import { LEGAL_SLUGS } from '@/lib/legal';

export const dynamic = 'force-static';

/**
 * Single-file sitemap (not an index) — matching the production template.
 * Only real, published pages are listed: padding a sitemap with thin or
 * non-existent URLs is a fast way to lose crawl trust on a new domain.
 *
 * Locales are gated on actually having content, so adding `es` to the config
 * before translating does not publish 404s.
 */
export default function sitemap(): MetadataRoute.Sitemap {
  const today = new Date().toISOString();
  const entries: MetadataRoute.Sitemap = [];

  const hubHrefs = Object.keys(siteConfig.hubs).map(
    (key) => siteConfig.hubs[key as keyof typeof siteConfig.hubs].href,
  );

  const locales = localesWithContent();
  // Only advertise alternates for locales that really exist.
  const languageMap = Object.fromEntries(
    locales.map((l) => [
      l,
      `${siteConfig.url}${l === siteConfig.defaultLocale ? '' : `/${l}`}` || siteConfig.url,
    ]),
  );

  for (const locale of locales) {
    const prefix = locale === siteConfig.defaultLocale ? '' : `/${locale}`;
    const isDefault = locale === siteConfig.defaultLocale;

    entries.push({
      url: `${siteConfig.url}${prefix}` || siteConfig.url,
      lastModified: today,
      changeFrequency: 'daily',
      priority: 1,
      alternates: { languages: languageMap },
    });

    for (const href of hubHrefs) {
      entries.push({
        url: `${siteConfig.url}${prefix}${href}`,
        lastModified: today,
        changeFrequency: 'weekly',
        priority: 0.95,
      });
    }

    for (const guide of getAllGuides(locale)) {
      entries.push({
        url: `${siteConfig.url}${prefix}${siteConfig.hubs[guide.hub].href}/${guide.slug}`,
        lastModified: guide.modified ?? guide.published,
        changeFrequency: isDefault ? 'weekly' : 'monthly',
        priority: 0.9,
      });
    }

    // Legal and trust pages. Low priority for ranking, but they must be listed:
    // a privacy policy that is not discoverable is one of the things reviewers
    // and crawlers check when judging whether a site is legitimate.
    for (const slug of LEGAL_SLUGS) {
      entries.push({
        url: `${siteConfig.url}${prefix}/${slug}`,
        lastModified: today,
        changeFrequency: 'yearly',
        priority: 0.3,
      });
    }
  }

  return entries;
}
