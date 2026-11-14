import Link from 'next/link';
import { notFound } from 'next/navigation';
import { getTranslations, setRequestLocale } from 'next-intl/server';
import { routing } from '@/i18n/routing';
import { siteConfig } from '@/config/site.config';
import { homeFaq, latestUpdates } from '@/config/faq';
import { getAllGuides, localesWithContent } from '@/lib/content';
import { formatDate } from '@/lib/utils';
import { buildPageMetadata } from '@/lib/seo';
import { HomeSchema } from '@/components/seo/HomeSchema';
import { FaqSection } from '@/components/game/FaqSection';
import { Hero, GuideThumb, guideImage, type HeroShortcut } from '@/components/Hero';
import { TrailerEmbed } from '@/components/TrailerEmbed';
import { ReadingIndex, type IndexGroup } from '@/components/ReadingIndex';
import { HomeModuleHeader } from '@/components/home/HomeModuleHeader';
import { SponsoredBanner } from '@/components/ads/SponsoredBanner';

/** Only locales with real content are prerendered — see localesWithContent(). */
export function generateStaticParams() {
  return localesWithContent().map((locale) => ({ locale }));
}

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  return buildPageMetadata({
    title: siteConfig.title,
    description: siteConfig.description,
    path: '/',
    locale,
  });
}

export default async function HomePage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!routing.locales.includes(locale as (typeof routing.locales)[number])) notFound();
  // next-intl narrows this to the literal locale union; params arrive as string.
  setRequestLocale(locale as never);
  const t = await getTranslations({ locale });

  const prefix = locale === siteConfig.defaultLocale ? '' : `/${locale}`;
  const guides = getAllGuides(locale);
  const updates = latestUpdates(guides);
  const hubKeys = (Object.keys(siteConfig.hubs) as Array<keyof typeof siteConfig.hubs>)
    .filter((key) => guides.some((guide) => guide.hub === key));

  const hubLabel = (key: string) =>
    t.has(`hubs.${key}.label`) ? t(`hubs.${key}.label`) : siteConfig.hubs[key].label;
  const hubDescription = (key: string) =>
    t.has(`hubs.${key}.description`) ? t(`hubs.${key}.description`) : siteConfig.hubs[key].description;
  const hubHref = (key: string) => `${prefix}${siteConfig.hubs[key].href}`;
  const featuredOrder = (siteConfig.home as any).featuredGuideOrderByLocale?.[locale]
    ?? siteConfig.home.featuredGuides.map(({ key }) => key);
  const featuredGuides: HeroShortcut[] = (featuredOrder as string[]).flatMap((key: string) => {
    const configured = siteConfig.home.featuredGuides.find((entry) => entry.key === key);
    const guide = configured && guides.find((entry) => entry.slug === configured.slug);
    return guide
      ? [{ label: t(`home.featuredGuides.${key}`), href: guide.href }]
      : [];
  });
  const indexGroups: IndexGroup[] = hubKeys.map((key) => ({
    label: hubLabel(key),
    href: hubHref(key),
    guides: guides
      .filter((guide) => guide.hub === key)
      .map((guide) => ({ title: guide.title, href: guide.href })),
  }));

  return (
    <>
      <HomeSchema locale={locale} />

      <Hero locale={locale} hubs={hubKeys} featuredGuides={featuredGuides} />

      <div className="home-layout">
        <div className="home-content">
          {/* Latest updates: freshness signal, and it surfaces new pages to crawlers */}
          {updates.length > 0 && (
            <section className="home-module" data-sponsored-trigger="">
              <HomeModuleHeader title={t('home.latest')} />
              <div className="home-card-grid">
                {updates.map((guide) => (
                  <Link key={guide.slug} href={guide.href} className="group home-card">
                    <GuideThumb src={guideImage(guide.image, guide.slug)} alt={guide.title} />
                    <span className="home-card-body">
                      <span className="home-card-meta">
                        <time dateTime={guide.modified ?? guide.published}>
                          {formatDate(guide.modified ?? guide.published, locale)}
                        </time>
                      </span>
                      <span className="home-card-title group-hover:text-primary transition">{guide.title}</span>
                      <span className="home-card-description line-clamp-2">{guide.description}</span>
                    </span>
                  </Link>
                ))}
              </div>
            </section>
          )}

          {/* One summary block per hub. The header carries the section scope and
              the only "view all" link, so the cards stay about individual reads. */}
          {hubKeys.map((key) => {
            const hubGuides = guides.filter((guide) => guide.hub === key).slice(0, 4);
            if (hubGuides.length === 0) return null;
            return (
              <section key={key} className="home-module">
                <HomeModuleHeader
                  title={`${siteConfig.name} ${hubLabel(key)}`}
                  description={hubDescription(key)}
                  href={hubHref(key)}
                  browseLabel={t('home.moduleBrowse')}
                />
                <div className="home-card-grid">
                  {hubGuides.map((guide) => (
                    <Link key={guide.slug} href={guide.href} className="group home-card">
                      <GuideThumb src={guideImage(guide.image, guide.slug)} alt={guide.title} />
                      <span className="home-card-body">
                        <span className="home-card-title group-hover:text-primary transition">{guide.title}</span>
                        <span className="home-card-description line-clamp-4">{guide.description}</span>
                        <span className="home-card-arrow" aria-hidden="true">→</span>
                      </span>
                    </Link>
                  ))}
                </div>
              </section>
            );
          })}

          {/* Official media is evidence of the game, not the first thing a player
              needs; it follows the sections that answer a question. */}
          {(siteConfig.media.youtubeId || siteConfig.media.steamMovieId) && (
            <section className="home-module">
              <HomeModuleHeader
                title={t('home.officialMedia')}
                description={t('home.officialMediaDescription')}
              />
              <TrailerEmbed />
            </section>
          )}

          <section className="home-module">
            <FaqSection
              items={homeFaq}
              heading={t('home.faq', { game: siteConfig.name })}
              className="mt-0"
            />
          </section>

          <section className="mt-4 rounded-xl border border-primary/25 bg-primary/5 p-8 text-center">
            <h2 className="text-2xl font-bold">{t('home.readyTitle', { game: siteConfig.name })}</h2>
            <p className="mx-auto mt-3 max-w-xl text-sm text-foreground/80">
              {t('home.readyDescription')}
            </p>
          </section>
        </div>

        <aside className="home-rail">
          <ReadingIndex groups={indexGroups} title={t('reading.index')} currentHref={prefix || '/'} />
        </aside>
      </div>

      <SponsoredBanner key={`home-${locale}`} />
    </>
  );
}
