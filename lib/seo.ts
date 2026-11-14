import type { Metadata } from 'next';
import { siteConfig } from '@/config/site.config';
import { getLocaleRoutes, localesWithContent } from '@/lib/content';

type Params = {
  title: string;
  description: string;
  /** Path WITHOUT locale prefix, e.g. `/guide/Phantom-Blade-Zero-beginner-guide` */
  path: string;
  locale: string;
  image?: string;
  type?: 'website' | 'article';
  publishedTime?: string;
  modifiedTime?: string;
  /** Set false for pages that must stay out of the index (e.g. legal boilerplate
   *  that is only written in English but is served under every locale prefix). */
  indexable?: boolean;
  /** Locales that really serve this page as an indexable alternate. Legal
   *  boilerplate is English-only: its prefixed copies canonicalise to the
   *  default locale, so an hreflang cluster that points at them is wrong. */
  alternates?: string[];
};

/**
 * Builds page metadata and — critically — the full hreflang set.
 *
 * Each page emits only existing translations + x-default, pointing at the SAME
 * page in the other language. Omitting x-default, or pointing hreflang at the
 * wrong translation, is one of the most common reasons a multi-locale site
 * indexes badly.
 */
export function buildPageMetadata({
  title,
  description,
  path,
  locale,
  image,
  type = 'website',
  publishedTime,
  modifiedTime,
  indexable = true,
  alternates,
}: Params): Metadata {
  const clean = path === '/' ? '' : path;
  // A non-indexable page (English-only boilerplate served under a locale prefix)
  // canonicalises to the English original so the two copies never compete.
  const canonical =
    locale === siteConfig.defaultLocale || !indexable ? clean || '/' : `/${locale}${clean}`;

  // Emit the alternate set for locales that actually HAVE content, including the
  // default locale itself: an hreflang cluster that omits its own default is a
  // common cause of "duplicate, Google chose a different canonical".
  //
  // Gating on localesWithContent() rather than siteConfig.locales is essential
  // during a staged rollout. siteConfig lists locales we intend to translate to,
  // but until those markdown files exist those URLs do not exist — and an hreflang
  // pointing at a 404 teaches Google to distrust the whole cluster.
  const languages: Record<string, string> = {};
  const routes = getLocaleRoutes();
  const isContentPath = Object.values(siteConfig.hubs).some(
    ({ href }) => path === href || path.startsWith(`${href}/`),
  );
  if (!indexable) {
    languages[siteConfig.defaultLocale] = clean || '/';
  } else {
    for (const loc of alternates ?? localesWithContent()) {
      if (isContentPath && !routes[loc]?.includes(path.replace(/^\//, ''))) continue;
      languages[loc] = loc === siteConfig.defaultLocale ? clean || '/' : `/${loc}${clean}`;
    }
  }
  languages['x-default'] = clean || '/';

  return {
    title,
    description,
    robots: indexable
      ? {
          index: true,
          follow: true,
          googleBot: {
            index: true,
            follow: true,
            'max-video-preview': -1,
            'max-image-preview': 'large',
            'max-snippet': -1,
          },
        }
      : { index: false, follow: true },
    alternates: { canonical, languages },
    openGraph: {
      type,
      title,
      description,
      url: canonical,
      siteName: siteConfig.fullName,
      locale,
      images: [{ url: image ?? siteConfig.heroImage, width: 1920, height: 1080 }],
      ...(type === 'article' ? { publishedTime, modifiedTime } : {}),
    },
    twitter: {
      card: 'summary_large_image',
      creator: siteConfig.twitter,
      title,
      description,
      images: [image ?? siteConfig.heroImage],
    },
  };
}
