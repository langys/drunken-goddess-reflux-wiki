import { defineRouting } from 'next-intl/routing';
import { siteConfig } from '@/config/site.config';

export const routing = defineRouting({
  locales: siteConfig.locales,
  defaultLocale: siteConfig.defaultLocale,
  // 'as-needed' keeps the default locale unprefixed (/guide/...) which matches the
  // production template and keeps English URLs one level shallower.
  localePrefix: 'as-needed',

  // Locale detection is OFF on purpose.
  //
  // With it on, next-intl serves /guide/x to a Japanese browser by redirecting to
  // /ja/guide/x — so one URL returns different content depending on a request
  // header. That contradicts the canonical and hreflang tags, which declare the
  // English URL as the canonical for that page, and it makes what Googlebot sees
  // depend on Googlebot's Accept-Language. On a site whose entire strategy is
  // precise canonical control per keyword, that is a self-inflicted duplicate
  // content problem.
  //
  // Readers pick a language explicitly through the switcher; the URL is then the
  // single source of truth for which locale is being served.
  localeDetection: false,
});

/**
 * Host used for the www / non-www canonical redirect.
 *
 * Kept outside defineRouting on purpose: next-intl validates the routing object
 * and rejects unknown keys. Middleware reads this to collapse both host variants
 * onto one, because mixing them across canonical, sitemap and hreflang is the
 * fastest way to break indexing on a new domain.
 */
export const canonicalHost = siteConfig.domain;

export type Locale = (typeof routing.locales)[number];
