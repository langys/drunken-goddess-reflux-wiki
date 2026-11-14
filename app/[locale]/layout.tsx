import type { Metadata, Viewport } from 'next';
import { GeistSans } from 'geist/font/sans';
import { GeistMono } from 'geist/font/mono';
import { NextIntlClientProvider } from 'next-intl';
import { getMessages, setRequestLocale } from 'next-intl/server';
import { notFound } from 'next/navigation';
import { routing } from '@/i18n/routing';
import { siteConfig } from '@/config/site.config';
import { getAllGuides, getLocaleRoutes, localesWithContent } from '@/lib/content';
import { SiteHeader, type NavItem } from '@/components/SiteHeader';
import { SiteFooter } from '@/components/SiteFooter';
import { ThemeProvider, themeInitScript } from '@/components/ThemeProvider';
import { GoogleAnalytics } from '@/components/analytics/GoogleAnalytics';
import '../globals.css';

export const metadata: Metadata = {
  metadataBase: new URL(siteConfig.url),
  title: { default: siteConfig.title, template: `%s - ${siteConfig.fullName}` },
  description: siteConfig.description,
  // Ownership tags must remain present to keep search properties verified.
  verification: {
    google: siteConfig.verification.google,
    other: siteConfig.verification.bing ? { 'msvalidate.01': siteConfig.verification.bing } : undefined,
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  alternates: {
    canonical: '/',
    // Gate on localesWithContent(), not siteConfig.locales: hreflang must never
    // point at a URL that does not exist yet (see the note in the layout body).
    languages: {
      ...Object.fromEntries(
        localesWithContent().map((l) => [l, l === siteConfig.defaultLocale ? '/' : `/${l}`]),
      ),
      'x-default': '/',
    },
  },
  openGraph: {
    type: 'website',
    siteName: siteConfig.fullName,
    title: siteConfig.title,
    description: siteConfig.description,
    images: [{ url: siteConfig.heroImage, width: 1920, height: 1080 }],
  },
  twitter: {
    card: 'summary_large_image',
    creator: siteConfig.twitter,
    title: siteConfig.title,
    description: siteConfig.description,
    images: [siteConfig.heroImage],
  },
  icons: {
    // Generated per site by scripts/make_logo.py so no two sites in a portfolio
    // share a favicon. SVG first: it stays sharp at every size.
    icon: [
      { url: '/icon.svg', type: 'image/svg+xml' },
      { url: '/favicon.ico', sizes: 'any' },
      { url: '/favicon-32x32.png', sizes: '32x32', type: 'image/png' },
      { url: '/favicon-96x96.png', sizes: '96x96', type: 'image/png' },
    ],
    apple: [{ url: '/apple-touch-icon.png', sizes: '180x180' }],
  },
};

export const viewport: Viewport = {
  themeColor: siteConfig.themeColorHex,
  width: 'device-width',
  initialScale: 1,
};

/** Only locales with real content are prerendered — see localesWithContent(). */
export function generateStaticParams() {
  return localesWithContent().map((locale) => ({ locale }));
}

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!routing.locales.includes(locale as (typeof routing.locales)[number])) notFound();
  const availableLocales = localesWithContent();
  // A locale declared in siteConfig but with no translated markdown yet must 404
  // rather than render the default locale's content under its own <html lang> and
  // canonical. next-intl's middleware rewrites /es to [locale]=es regardless, so
  // without this gate an untranslated locale ships as a prerendered duplicate of
  // the English page — self-inflicted duplicate content, and the fastest way to
  // teach Google to distrust the hreflang cluster.
  if (!availableLocales.includes(locale)) notFound();
  // next-intl narrows this to the literal locale union; params arrive as string.
  setRequestLocale(locale as never);
  const messages = await getMessages();
  const localeRoutes = getLocaleRoutes();

  // Nav data is resolved here, on the server. SiteHeader is a client component
  // for its hover state, so it receives finished hrefs instead of reading disk.
  const localePrefix = locale === siteConfig.defaultLocale ? '' : `/${locale}`;
  const guides = getAllGuides(locale);
  const hubMessages = (messages as { hubs?: Record<string, { label?: string }> })?.hubs;
  const navItems: NavItem[] = (Object.keys(siteConfig.hubs) as Array<keyof typeof siteConfig.hubs>)
    // A hub with no articles in this locale renders an empty page, so it stays
    // out of the nav until its first translation lands. That keeps partial
    // rollouts from advertising dead sections.
    .filter((key) => guides.some((guide) => guide.hub === key))
    .map((key) => {
      const hub = siteConfig.hubs[key];
      const localizedLabel = hubMessages?.[key]?.label ?? hub.label;
      return {
        key,
        label: localizedLabel,
        href: `${localePrefix}${hub.href}`,
        // Five links per menu dropdown.
        items: guides
          .filter((guide) => guide.hub === key)
          .slice(0, 5)
          .map((guide) => ({ title: guide.title, href: `${localePrefix}${hub.href}/${guide.slug}` })),
      };
    });

  return (
    // Brand tokens are injected here rather than duplicated in globals.css, so
    // `siteConfig.themeColor` is genuinely the single source of truth. An inline
    // custom property outranks the stylesheet's `.dark` block, which means one
    // value drives BOTH themes and they cannot drift apart.
    <html
      lang={locale}
      suppressHydrationWarning
      style={
        {
          '--primary': siteConfig.themeColor,
          '--accent': siteConfig.themeColor,
          '--ring': siteConfig.themeColor,
        } as React.CSSProperties
      }
    >
      <head>
        {/* Applies the stored colour scheme before first paint. Without this the
            browser paints light and then flips, which reads as a white flash on
            every navigation for dark-mode readers. */}
        <script dangerouslySetInnerHTML={{ __html: themeInitScript }} />
      </head>
      <body className={`${GeistSans.variable} ${GeistMono.variable} font-sans`}>
        <ThemeProvider>
          <NextIntlClientProvider messages={messages}>
            <SiteHeader
              locale={locale}
              navItems={navItems}
              availableLocales={availableLocales}
              configuredLocales={[...siteConfig.locales]}
              localeRoutes={localeRoutes}
            />
            <div className="site-content" style={{ '--reading-sticky-top': '72px' } as React.CSSProperties}>
              <main className="site-main">{children}</main>
            </div>
            <SiteFooter locale={locale} />
          </NextIntlClientProvider>
        </ThemeProvider>
        <GoogleAnalytics />
      </body>
    </html>
  );
}
