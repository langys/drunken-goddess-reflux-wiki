import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { setRequestLocale } from 'next-intl/server';
import { routing } from '@/i18n/routing';
import { LegalPageView } from '@/components/LegalPageView';
import { getLegalPage } from '@/lib/legal';
import { buildPageMetadata } from '@/lib/seo';

const SLUG = 'terms';

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  const page = await getLegalPage(SLUG, locale);
  if (!page) return {};
  return buildPageMetadata({
    title: page.title,
    description: page.description,
    path: `/terms`,
    locale,
  });
}

export default async function Page({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!routing.locales.includes(locale as (typeof routing.locales)[number])) notFound();
  // next-intl narrows this to the literal locale union; params arrive as string.
  setRequestLocale(locale as never);
  return <LegalPageView slug={SLUG} locale={locale} />;
}
