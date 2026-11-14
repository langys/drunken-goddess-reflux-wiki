import Link from 'next/link';
import { useTranslations } from 'next-intl';
import { siteConfig } from '@/config/site.config';
import { cn } from '@/lib/utils';

type HubKey = keyof typeof siteConfig.hubs;
export type HeroShortcut = { label: string; href: string };

/**
 * Home hero: search, four player tasks, and a compact row of direct article
 * links selected from recent traffic. The page resolves shortcuts against real
 * locale content; the hero does not fetch analytics or require JavaScript.
 */
export function Hero({ locale, hubs }: {
  locale?: string;
  hubs?: HubKey[];
  featuredGuides?: HeroShortcut[];
}) {
  const t = useTranslations();
  const image = siteConfig.heroImage;
  const prefix = locale && locale !== siteConfig.defaultLocale ? `/${locale}` : '';
  const tagline = t.has('hero.tagline') ? t('hero.tagline') : siteConfig.tagline;

  const available = hubs ?? (Object.keys(siteConfig.hubs) as HubKey[]);
  const configured = (
    (siteConfig as { home?: { quickLinks?: string[] } }).home?.quickLinks ?? []
  ).filter((key): key is HubKey => key in siteConfig.hubs);
  const quickKeys = [...configured, ...available.filter((key) => !configured.includes(key))]
    .filter((key, index, all) => available.includes(key) && all.indexOf(key) === index)
    .slice(0, 4);

  const searchHref = `${prefix}/search`;

  return (
    <section className="full-bleed relative isolate overflow-hidden border-b border-border">
      {image ? (
        <>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={image}
            alt=""
            aria-hidden="true"
            fetchPriority="high"
            className="absolute inset-0 -z-20 h-full w-full object-cover object-[center_38%]"
          />
          <div
            className="absolute inset-0 -z-10 bg-gradient-to-t from-black/75 via-black/35 to-black/15"
            aria-hidden="true"
          />
          <div
            className="absolute inset-0 -z-10 bg-gradient-to-r from-black/75 via-black/30 to-transparent"
            aria-hidden="true"
          />
        </>
      ) : (
        <div
          className="absolute inset-0 -z-10 bg-gradient-to-br from-primary/25 via-background to-background"
          aria-hidden="true"
        />
      )}

      <div className="home-hero-frame">
        <div className={cn('home-hero-inner py-14 sm:py-20 lg:py-40', image && 'text-white')}>
          <div className="max-w-xl">
            <h1 className="text-4xl font-extrabold tracking-tight drop-shadow-sm sm:text-5xl">
              {siteConfig.fullName}
            </h1>
            <p className={cn('mt-3 text-base leading-relaxed sm:text-lg', image ? 'text-white/90' : 'text-muted-foreground')}>
              {tagline}
            </p>
          </div>

          <form action={searchHref} method="get" role="search" className="home-search-form mt-6">
            <label htmlFor="home-search-query" className="sr-only">
              {t('home.searchLabel')}
            </label>
            <input
              id="home-search-query"
              name="q"
              type="search"
              required
              minLength={2}
              maxLength={200}
              placeholder={t('home.searchPlaceholder')}
              autoComplete="off"
              spellCheck={false}
              className={cn('home-search-input', image && 'home-search-input--hero')}
            />
            <button type="submit" className="home-search-submit">
              {t('home.searchSubmit')}
            </button>
          </form>

          {siteConfig.home?.heroCta && (
            <div className="mt-5 flex flex-wrap items-center gap-3">
              {siteConfig.home.heroCta.primary && (
                <Link
                  href={`${prefix}${siteConfig.home.heroCta.primary.href}`}
                  className="inline-flex min-h-11 items-center gap-2 rounded-lg bg-primary px-5 text-sm font-semibold text-primary-foreground shadow-sm transition hover:opacity-90 active:scale-[0.98]"
                >
                  {siteConfig.home.heroCta.primary.icon && (
                    <span aria-hidden="true">{siteConfig.home.heroCta.primary.icon}</span>
                  )}
                  <span>
                    {t.has('hero.primaryCta')
                      ? t('hero.primaryCta')
                      : (siteConfig.home.heroCta.primary.label || 'Beginner Guide')}
                  </span>
                </Link>
              )}
              {siteConfig.home.heroCta.secondary && (
                <Link
                  href={`${prefix}${siteConfig.home.heroCta.secondary.href}`}
                  className={cn(
                    'inline-flex min-h-11 items-center gap-2 rounded-lg border px-5 text-sm font-semibold transition active:scale-[0.98]',
                    image
                      ? 'border-white/30 bg-black/30 text-white backdrop-blur-sm hover:border-white/50 hover:bg-black/45'
                      : 'border-border bg-background text-foreground hover:bg-muted',
                  )}
                >
                  {siteConfig.home.heroCta.secondary.icon && (
                    <span aria-hidden="true">{siteConfig.home.heroCta.secondary.icon}</span>
                  )}
                  <span>
                    {t.has('hero.secondaryCta')
                      ? t('hero.secondaryCta')
                      : (siteConfig.home.heroCta.secondary.label || 'Tier List')}
                  </span>
                </Link>
              )}
            </div>
          )}

          {quickKeys.length > 0 && (
            <nav aria-label={t('home.startHere')} className="mt-5 flex flex-wrap items-center gap-2">
              {quickKeys.map((key) => {
                const hubLabel = t.has(`hubs.${key}.label`) ? t(`hubs.${key}.label`) : siteConfig.hubs[key].label;
                return (
                  <Link
                    key={key}
                    href={`${prefix}${siteConfig.hubs[key].href}`}
                    className={cn(
                      'inline-flex items-center gap-1 rounded-full border px-3 py-1 text-xs font-medium transition',
                      image
                        ? 'border-white/25 bg-black/30 text-white/90 backdrop-blur-sm hover:border-white/50 hover:bg-black/50 hover:text-white'
                        : 'border-border bg-muted/50 text-foreground/80 hover:border-primary/50 hover:text-foreground',
                    )}
                  >
                    <span>{hubLabel}</span>
                    <span aria-hidden="true" className="opacity-65">→</span>
                  </Link>
                );
              })}
            </nav>
          )}
        </div>
      </div>
    </section>
  );
}

/**
 * Thumbnail for a guide card or article header.
 *
 * Uses explicitly selected images. Listings show thumbnails only when every
 * guide in the group has one; arbitrary gallery shots do not explain the topic.
 *
 * `image` points at the page's social card (`/images/og/…`), which has the page
 * title painted onto the artwork. Rendering that beside the card heading or the
 * `<h1>` printed every title twice, so the `card/` variant — the same artwork
 * with no painted title — is preferred for anything drawn inside the page. The
 * painted version stays in `og:image`, where the picture is the whole message.
 */
export function displayImage(image: string | undefined): string | undefined {
  if (!image) return undefined;
  // Only generated social cards have a title-free sibling; a hand-picked image
  // or a hot-linked Steam URL is used exactly as given.
  const match = image.match(/^(.*)\/images\/og\/(.+)$/);
  return match ? `${match[1]}/images/card/${match[2]}` : image;
}

export function guideImage(image: string | undefined, key?: string): string | undefined {
  if (image) return displayImage(image);
  if (!key) return undefined;
  const shots = siteConfig.media.screenshots;
  if (shots.length === 0) return undefined;
  let hash = 0;
  for (let index = 0; index < key.length; index += 1) {
    hash = (hash * 31 + key.charCodeAt(index)) % 100000;
  }
  return shots[hash % shots.length]?.url;
}

/** Keep each visible listing uniform without inventing covers for missing images. */
export function hasCompleteGuideImages(guides: readonly { image?: string; slug?: string }[]): boolean {
  return siteConfig.media.screenshots.length > 0 || (guides.length > 0 && guides.every((guide) => Boolean(guideImage(guide.image, guide.slug))));
}

export function GuideThumb({
  src,
  alt,
  className,
}: {
  src: string | undefined;
  alt: string;
  className?: string;
}) {
  if (!src) return null;
  return (
    <div className={cn('overflow-hidden rounded-lg bg-muted', className)}>
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={src}
        alt={alt}
        width={640}
        height={360}
        loading="lazy"
        className="aspect-video w-full object-cover transition duration-300 group-hover:scale-[1.03]"
      />
    </div>
  );
}
