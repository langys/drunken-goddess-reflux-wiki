import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { setRequestLocale } from 'next-intl/server';
import Link from 'next/link';
import { routing } from '@/i18n/routing';
import { siteConfig } from '@/config/site.config';
import { getAllGuides } from '@/lib/content';
import { buildPageMetadata } from '@/lib/seo';

/**
 * A crawlable landing page for search.
 *
 * The dialog in the header is the primary way in, but a real page gives the
 * WebSite SearchAction target something to point at, and gives readers a
 * browsable fallback if JavaScript is unavailable. It is marked noindex — a
 * search page has no content of its own and would only compete with the guides.
 */
export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  return {
    ...buildPageMetadata({
      title: `Search ${siteConfig.name} Guides`,
      description: `Search every ${siteConfig.fullName} guide by keyword.`,
      path: '/search',
      locale,
    }),
    robots: { index: false, follow: true },
  };
}

export default async function SearchPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!routing.locales.includes(locale as (typeof routing.locales)[number])) notFound();
  setRequestLocale(locale as never);

  const prefix = locale === siteConfig.defaultLocale ? '' : `/${locale}`;
  const guides = getAllGuides(locale);
  const hubKeys = Object.keys(siteConfig.hubs) as Array<keyof typeof siteConfig.hubs>;

  return (
    <div className="mx-auto max-w-3xl">
      <h1 className="text-3xl font-extrabold tracking-tight sm:text-4xl">Search</h1>
      <p className="mt-3 text-muted-foreground">
        Press <kbd className="rounded border border-border px-1.5 py-0.5 text-xs">⌘K</kbd> anywhere on the site
        to search. Or browse by section below.
      </p>

      {hubKeys.map((key) => {
        const hubGuides = guides.filter((guide) => guide.hub === key);
        if (hubGuides.length === 0) return null;
        return (
          <section key={key} className="mt-8">
            <h2 className="mb-3 text-lg font-bold">{siteConfig.hubs[key].label}</h2>
            <ul className="space-y-2 text-sm">
              {hubGuides.map((guide) => (
                <li key={guide.slug}>
                  <Link href={`${prefix}${siteConfig.hubs[guide.hub].href}/${guide.slug}`} className="text-primary hover:underline">
                    {guide.title}
                  </Link>
                </li>
              ))}
            </ul>
          </section>
        );
      })}
    </div>
  );
}
