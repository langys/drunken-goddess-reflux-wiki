import Link from 'next/link';
import { notFound } from 'next/navigation';
import { getTranslations, setRequestLocale } from 'next-intl/server';
import { routing } from '@/i18n/routing';
import { siteConfig } from '@/config/site.config';
import {
  extractToc,
  getAllGuides,
  getGuideBySlug,
  getGuidesByHub,
  getRelatedGuides,
  localesWithContent,
  renderMarkdown,
  validateContentCoverage,
  type GuideHub,
} from '@/lib/content';
import { isReservedSlug } from '@/lib/legal';
import { buildPageMetadata } from '@/lib/seo';
import { Breadcrumbs } from '@/components/seo/Breadcrumbs';
import { ArticleSchema } from '@/components/seo/ArticleSchema';
import { QuickGuide } from '@/components/game/QuickGuide';
import { TableOfContents } from '@/components/TableOfContents';
import { ReadingIndex, type IndexGroup } from '@/components/ReadingIndex';
import { ArticlePagination } from '@/components/ArticlePagination';
import { Callout, CardGrid } from '@/components/game/Callout';
import { FaqSection } from '@/components/game/FaqSection';
import { RelatedGuides } from '@/components/RelatedGuides';
import { GuideThumb, guideImage, hasCompleteGuideImages } from '@/components/Hero';
import { SponsoredBanner } from '@/components/ads/SponsoredBanner';
import { ReadingAdRail } from '@/components/ads/ReadingAdRail';
import { TrailerEmbed } from '@/components/TrailerEmbed';
import { formatDate } from '@/lib/utils';

type HubKey = keyof typeof siteConfig.hubs;

/** Maps a first path segment back to a hub key via its configured href. */
function resolveHub(segment: string): HubKey | null {
  return (
    (Object.keys(siteConfig.hubs) as HubKey[]).find(
      (key) => siteConfig.hubs[key].href.replace(/^\//, '') === segment,
    ) ?? null
  );
}

/**
 * One catch-all route serves both hub pages (`/guide`) and spoke pages
 * (`/guide/drunken-goddess-reflux-beginner-guide`). A single segment means hub, two means
 * spoke. Next.js cannot have both `[hub]` and `[slug]` at the same position, so
 * the catch-all is the clean way to express this two-level taxonomy.
 */
export function generateStaticParams() {
  // Surfaces pages.ts <-> markdown drift as build output instead of 404s later.
  for (const locale of localesWithContent()) validateContentCoverage(locale);

  return localesWithContent().flatMap((locale) => {
    const hubs = (Object.keys(siteConfig.hubs) as HubKey[]).map((key) => ({
      locale,
      slug: [siteConfig.hubs[key].href.replace(/^\//, '')],
    }));
    const spokes = getAllGuides(locale).map((guide) => ({
      locale,
      slug: [siteConfig.hubs[guide.hub].href.replace(/^\//, ''), guide.slug],
    }));
    return [...hubs, ...spokes];
  });
}

type RouteParams = { locale: string; slug: string[] };

export async function generateMetadata({ params }: { params: Promise<RouteParams> }) {
  const { locale, slug } = await params;
  if (!slug?.length) return {};

  if (slug.length === 1) {
    const hub = resolveHub(slug[0]);
    if (!hub) return {};
    const meta = siteConfig.hubs[hub];
    const t = await getTranslations({ locale });
    const hubLabel = t.has(`hubs.${hub}.label`) ? t(`hubs.${hub}.label`) : meta.label;
    const hubDesc = t.has(`hubs.${hub}.description`) ? t(`hubs.${hub}.description`) : meta.description;
    const metadata = buildPageMetadata({
      title: `${siteConfig.name} ${hubLabel}`,
      description: hubDesc,
      path: meta.href,
      locale,
    });
    return getGuidesByHub(locale, hub).length > 0
      ? metadata : { ...metadata, robots: { index: false, follow: true } };
  }

  const guide = getGuideBySlug(locale, slug[1]);
  if (!guide) return {};
  return buildPageMetadata({
    title: guide.title,
    description: guide.description,
    path: `${siteConfig.hubs[guide.hub].href}/${guide.slug}`,
    locale,
    type: 'article',
    image: guide.image,
    publishedTime: guide.published,
    modifiedTime: guide.modified ?? guide.published,
  });
}

export default async function CatchAllPage({ params }: { params: Promise<RouteParams> }) {
  const { locale, slug } = await params;
  if (!routing.locales.includes(locale as (typeof routing.locales)[number])) notFound();
  if (!slug?.length) notFound();
  // next-intl narrows this to the literal locale union; params arrive as string.
  setRequestLocale(locale as never);
  const t = await getTranslations({ locale });

  // Reserved segments are owned by dedicated top-level routes (about, privacy,
  // terms, contact, search). Without this guard a request for /about would fall
  // through to the hub lookup, fail to resolve, and 404 — which is exactly how a
  // footer full of legal links ends up broken.
  if (isReservedSlug(slug[0])) notFound();

  // ---------------------------------------------------------------- hub page
  if (slug.length === 1) {
    const hub = resolveHub(slug[0]);
    if (!hub) notFound();
    const meta = siteConfig.hubs[hub];
    const hubLabel = t.has(`hubs.${hub}.label`) ? t(`hubs.${hub}.label`) : meta.label;
    const hubDesc = t.has(`hubs.${hub}.description`) ? t(`hubs.${hub}.description`) : meta.description;
    const guides = getGuidesByHub(locale, hub as GuideHub);
    const showGuideImages = hasCompleteGuideImages(guides);

    const hasOverview = t.has(`hubs.${hub}.overview`);
    const overviewParagraphs: string[] = hasOverview ? (t.raw(`hubs.${hub}.overview`) as string[]) : [];
    const hasPillars = t.has(`hubs.${hub}.pillars`);
    const pillars: { title: string; body: string }[] = hasPillars ? (t.raw(`hubs.${hub}.pillars`) as { title: string; body: string }[]) : [];
    const hasFaq = t.has(`hubs.${hub}.faqItems`);
    const faqItems: { q: string; a: string }[] = hasFaq ? (t.raw(`hubs.${hub}.faqItems`) as { q: string; a: string }[]) : [];
    const overviewHeading = t.has('hubs.overviewTitle')
      ? t('hubs.overviewTitle', { hub: hubLabel })
      : `${hubLabel} Overview`;
    const guidesHeading = t.has('hubs.guidesTitle')
      ? t('hubs.guidesTitle', { hub: hubLabel })
      : `All ${hubLabel} Guides`;
    const faqHeading = t.has(`hubs.${hub}.faqHeading`)
      ? t(`hubs.${hub}.faqHeading`)
      : `${hubLabel} FAQ`;

    return (
      <>
        <Breadcrumbs
          locale={locale}
          items={[
            { name: t.has('nav.home') ? t('nav.home') : 'Home', url: '/' },
            { name: hubLabel, url: meta.href },
          ]}
        />
        <h1 className="text-3xl font-extrabold tracking-tight sm:text-4xl">
          {siteConfig.name} {hubLabel}
        </h1>
        <p className="mt-3 text-lg text-muted-foreground">{hubDesc}</p>

        <div className="listing-ad-grid">
          <div>
            {overviewParagraphs.length > 0 && (
              <section className="mt-8 space-y-4 rounded-xl border border-border bg-card/40 p-6">
                <h2 className="text-xl font-bold tracking-tight text-foreground sm:text-2xl">
                  {overviewHeading}
                </h2>
                <div className="space-y-3 text-sm leading-relaxed text-muted-foreground sm:text-base">
                  {overviewParagraphs.map((para, i) => (
                    <p key={i}>{para}</p>
                  ))}
                </div>
              </section>
            )}

            {pillars.length > 0 && <CardGrid cards={pillars} />}

            <section className="mt-10" data-sponsored-trigger="">
              <h2 className="text-xl font-bold tracking-tight text-foreground sm:text-2xl mb-4">
                {guidesHeading}
              </h2>
              <div className="grid gap-4 sm:grid-cols-2">
                {guides.map((guide) => (
                  <Link
                    key={guide.slug}
                    href={guide.href}
                    className="group overflow-hidden rounded-xl border border-border transition hover:border-primary/60 hover:bg-muted/50"
                  >
                    <GuideThumb src={guideImage(guide.image, guide.slug)} alt={guide.title} />
                    <span className="block p-5">
                      <span className="block font-medium leading-snug group-hover:text-primary">
                        {guide.title}
                      </span>
                      <span className="mt-2 line-clamp-3 text-sm text-muted-foreground">
                        {guide.description}
                      </span>
                      <span className="mt-3 block text-xs text-muted-foreground">{guide.published}</span>
                    </span>
                  </Link>
                ))}
              </div>

              {guides.length === 0 && (
                <p className="mt-8 text-sm text-muted-foreground">
                  {t('hub.empty')}
                </p>
              )}
            </section>

            {faqItems.length > 0 && (
              <FaqSection
                items={faqItems}
                heading={faqHeading}
                className="mt-12"
              />
            )}
          </div>
          {guides.length > 0 && <ReadingAdRail key={`hub-ad-${locale}-${hub}`} />}
        </div>

        {guides.length > 0 && <SponsoredBanner key={`hub-${locale}-${hub}`} />}
      </>
    );
  }

  // -------------------------------------------------------------- spoke page
  const guide = getGuideBySlug(locale, slug[1]);
  if (!guide) notFound();

  const articleParts = await renderMarkdown(guide.html ?? '');
  // Deterministic lead image and secondary inline screenshot from official gallery.
  // Neither will duplicate an image that is already present in the article markdown body.
  const shots = siteConfig.media.screenshots;
  const isImageInBody = (url: string) => articleParts.some((part) => part.type === 'html' && part.html.includes(url));

  let leadCandidate = guideImage(guide.image, guide.slug);
  if (leadCandidate && isImageInBody(leadCandidate) && shots.length > 0) {
    const altShot = shots.find((s) => !isImageInBody(s.url));
    if (altShot) leadCandidate = altShot.url;
  }
  const leadImageFinal = leadCandidate;

  let inlineImageFinal: string | undefined;
  if (shots.length > 1) {
    const startIndex = (guide.slug.length * 7) % shots.length;
    for (let i = 0; i < shots.length; i += 1) {
      const candidate = shots[(startIndex + i) % shots.length]?.url;
      if (candidate && candidate !== leadImageFinal && !isImageInBody(candidate)) {
        inlineImageFinal = candidate;
        break;
      }
    }
  }
  const related = getRelatedGuides(locale, guide);
  const hubMeta = siteConfig.hubs[guide.hub];
  const hubLabel = t.has(`hubs.${guide.hub}.label`) ? t(`hubs.${guide.hub}.label`) : hubMeta.label;
  const toc = extractToc(guide.html ?? '');
  const path = `${hubMeta.href}/${guide.slug}`;
  const prefix = locale === siteConfig.defaultLocale ? '' : `/${locale}`;
  const sameHub = getGuidesByHub(locale, guide.hub);
  // Only hubs that publish something in this locale appear in the index; an
  // empty group would link readers to a section with no articles.
  const indexGroups: IndexGroup[] = (Object.keys(siteConfig.hubs) as HubKey[])
    .map((key) => ({
      key,
      label: t.has(`hubs.${key}.label`) ? t(`hubs.${key}.label`) : siteConfig.hubs[key].label,
      href: `${prefix}${siteConfig.hubs[key].href}`,
      active: key === guide.hub,
      guides: getGuidesByHub(locale, key).map((item) => ({ title: item.title, href: item.href })),
    }))
    .filter((group) => group.guides.length > 0)
    .map(({ key: _key, ...group }) => group);

  return (
    <>
    <article className="reading-grid" aria-labelledby="article-title">
    <header className="reading-header">
      <ArticleSchema
        title={guide.title}
        description={guide.description}
        path={path}
        published={guide.published}
        modified={guide.modified}
        image={guide.image}
      />

      <Breadcrumbs
        locale={locale}
        items={[
          { name: t.has('nav.home') ? t('nav.home') : 'Home', url: '/' },
          { name: hubLabel, url: hubMeta.href },
          { name: guide.title, url: path },
        ]}
      />

      <h1 id="article-title" className="text-3xl font-extrabold leading-tight tracking-tight sm:text-4xl">{guide.title}</h1>
      <p className="reading-description mt-4 text-lg text-muted-foreground">{guide.description}</p>
      <p className="mt-3 text-xs text-muted-foreground">
        {formatDate(guide.published, locale)} · {siteConfig.fullName} Team
        {guide.modified && guide.modified !== guide.published && ` · ${t('common.updated')} ${formatDate(guide.modified, locale)}`}
      </p>
    </header>
    <ReadingAdRail key={guide.href} />
    {toc.length >= 2 && <aside className="reading-toc-rail">
      <div className="reading-toc-sticky">
        <TableOfContents key={guide.href} items={toc} title={t('toc.title')} />
      </div>
    </aside>}
    <div className="reading-article">

      {/* Lead image. A guide with only text reads as unfinished, and this is
          also the image that shows up when the page is shared. */}
      {leadImageFinal && (
        <figure className="mt-6 overflow-hidden rounded-xl border border-border">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={leadImageFinal}
            alt={guide.imageAlt ?? `${guide.title} — ${siteConfig.name}`}
            width={1280}
            height={720}
            fetchPriority="high"
            className="aspect-video w-full object-cover"
          />
          <figcaption className="border-t border-border/60 bg-muted/30 px-4 py-2 text-xs leading-relaxed text-muted-foreground">
            {guide.imageCaption && <span className="text-foreground/80">{guide.imageCaption} · </span>}
            {siteConfig.media.screenshotCredit}
          </figcaption>
        </figure>
      )}

      {guide.quickGuide && <QuickGuide items={guide.quickGuide} heading={t('common.quickGuide')} />}

      <div className="reading-mobile-toc"><TableOfContents key={guide.href} items={toc} title={t('toc.title')} collapsible /></div>

      <div className="article-body mt-8">
        {articleParts.map((part, index) => part.type === 'html'
          ? <div key={index} dangerouslySetInnerHTML={{ __html: part.html }} />
          : <TrailerEmbed key={index} video={part.video} />)}
      </div>

      {/* A second official screenshot partway down. Long-form pages with no
          image after the first screen lose mobile readers at the scroll. */}
      {inlineImageFinal && (
        <figure className="mt-10 overflow-hidden rounded-xl border border-border">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={inlineImageFinal}
            alt={`${guide.title} gameplay screenshot`}
            width={1280}
            height={720}
            loading="lazy"
            className="aspect-video w-full object-cover"
          />
          <figcaption className="border-t border-border/60 bg-muted/30 px-4 py-2 text-xs leading-relaxed text-muted-foreground">
            {siteConfig.media.screenshotCredit}
          </figcaption>
        </figure>
      )}

      {guide.cards && <CardGrid cards={guide.cards} />}

      {guide.faq && <FaqSection items={guide.faq} heading={t('common.faqHeading')} />}

      <RelatedGuides
        locale={locale}
        guides={related}
      />

      <ArticlePagination
        guides={sameHub}
        current={guide}
        hubHref={`${prefix}${hubMeta.href}`}
        hubLabel={hubLabel}
        labels={{ hub: t('reading.hub'), previous: t('reading.previous'), next: t('reading.next'), articleNavigation: t('reading.articleNavigation') }}
      />

    </div>
    <aside className="reading-index-rail"><ReadingIndex groups={indexGroups} title={t('reading.index')} currentHref={guide.href} /></aside>
    </article>
    <SponsoredBanner key={guide.href} />
    </>
  );
}
