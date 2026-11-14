import type { MetadataRoute } from 'next';
import { siteConfig } from '@/config/site.config';

export const dynamic = 'force-static';

/**
 * Deliberately allows every crawler, including AI crawlers (GPTBot, CCBot,
 * Google-Extended, ...). For a content site the trade is: give up control over
 * AI reuse, get maximum crawl and citation surface. The production site group
 * does the same — none of them ship an AI-crawler block.
 */
export default function robots(): MetadataRoute.Robots {
  return {
    rules: [{ userAgent: '*', allow: '/' }],
    sitemap: `${siteConfig.url}/sitemap.xml`,
    host: siteConfig.url,
  };
}
