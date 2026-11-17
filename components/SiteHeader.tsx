'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useTranslations } from 'next-intl';
import { useEffect, useRef, useState } from 'react';
import { siteConfig } from '@/config/site.config';
import { ThemeToggle } from './ThemeToggle';
import { LocaleSwitcher, type LocaleRouteMap } from './LocaleSwitcher';
import { SearchDialog } from './SearchDialog';

/** One nav entry, precomputed on the server.
 *
 *  SiteHeader is a client component (it needs hover/open state), so it must not
 *  import lib/content.ts — that would pull node:fs into the browser bundle and
 *  fail the build. The server layout computes these and passes them down. */
export type NavItem = {
  key: string;
  label: string;
  href: string;
  items: { title: string; href: string }[];
};

type Props = {
  locale: string;
  navItems: NavItem[];
  /** Locales that actually have content. Passed in because this is a server
   *  component and the switcher needs to avoid offering empty locales. */
  availableLocales: string[];
  /** locale -> paths that exist, so switching language keeps the reader in place. */
  localeRoutes?: LocaleRouteMap;
  /** Every locale the site is configured for, including untranslated ones. */
  configuredLocales?: string[];
};

/** One nav item: a link plus a dropdown listing that hub's most recent guides.
 *
 *  Trigger rules, deliberately distinct:
 *   - the label is a real `<a href>`: crawlable, middle-clickable, and it
 *     navigates to the hub. A top-level nav item must never be a button-only
 *     control, or every page loses its strongest internal link to the hub.
 *   - the chevron next to it is a separate disclosure button that opens the
 *     panel (click, tap, Enter or Space). Opening is click-only, never hover.
 *   - Escape closes it, an outside click closes it, and a route change closes
 *     it so the panel cannot linger over the next page.
 *
 *  The earlier CSS-only version used `focus-within`, which kept the panel open
 *  after a click because the link retained focus — so the menu appeared at the
 *  same time as the page it navigated to. Tracking open state in JS and closing
 *  it on route change removes that overlap.
 */
function NavDropdown({
  label,
  href,
  items,
}: {
  label: string;
  href: string;
  items: { title: string; href: string }[];
}) {
  const [open, setOpen] = useState(false);
  const wrapperRef = useRef<HTMLDivElement>(null);
  const pathname = usePathname();
  const t = useTranslations('common');
  const tn = useTranslations('nav');

  // Navigating away must close the panel, otherwise it stays on screen over the
  // new page.
  useEffect(() => setOpen(false), [pathname]);

  useEffect(() => {
    if (!open) return;
    const onPointerDown = (event: MouseEvent) => {
      if (!wrapperRef.current?.contains(event.target as Node)) setOpen(false);
    };
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') setOpen(false);
    };
    document.addEventListener('mousedown', onPointerDown);
    document.addEventListener('keydown', onKeyDown);
    return () => {
      document.removeEventListener('mousedown', onPointerDown);
      document.removeEventListener('keydown', onKeyDown);
    };
  }, [open]);

  const hasMenu = items.length > 0;

  if (!hasMenu) {
    return (
      <Link
        href={href}
        className="flex items-center gap-1.5 py-2 text-muted-foreground transition hover:text-primary"
      >
        <span>{label}</span>
      </Link>
    );
  }

  return (
    <div ref={wrapperRef} className="relative flex items-center">
      {/* The label stays a link on purpose: a button-only top-level item hides
          the hub from crawlers and blocks middle-click / long-press / no-JS
          navigation on every page of the site. */}
      <Link
        href={href}
        className="py-2 text-muted-foreground transition hover:text-primary"
      >
        {label}
      </Link>
      <button
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        aria-expanded={open}
        aria-haspopup="true"
        aria-label={`${label} — ${tn('openMenu')}`}
        className="-mr-2.5 ml-0.5 flex h-8 w-8 items-center justify-center rounded-md text-muted-foreground transition hover:text-primary focus:outline-none"
      >
        <svg
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.5"
          className={`transition-transform duration-200 ${open ? 'rotate-180' : ''}`}
          aria-hidden="true"
        >
          <path d="m6 9 6 6 6-6" />
        </svg>
      </button>

      {hasMenu && open && (
        <div className="absolute left-1/2 top-full z-50 w-72 -translate-x-1/2 pt-2">
          <div className="overflow-hidden rounded-lg border border-border bg-card shadow-lg">
            <ul className="py-2">
              {items.map((item) => (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    onClick={() => setOpen(false)}
                    className="flex items-start gap-2 px-4 py-2.5 text-sm text-foreground transition-colors hover:bg-muted"
                  >
                    <svg
                      width="12"
                      height="12"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2.5"
                      className="mt-1 flex-shrink-0 text-primary"
                      aria-hidden="true"
                    >
                      <path d="m9 18 6-6-6-6" />
                    </svg>
                    <span className="leading-snug">{item.title}</span>
                  </Link>
                </li>
              ))}
            </ul>
            <Link
              href={href}
              onClick={() => setOpen(false)}
              className="flex items-center justify-center gap-1 border-t border-border px-4 py-2.5 text-sm font-medium text-primary transition-colors hover:bg-muted"
            >
              {t('readMore')}
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                <path d="M5 12h14M13 6l6 6-6 6" />
              </svg>
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}

export function SiteHeader({
  locale,
  navItems,
  availableLocales,
  localeRoutes,
  configuredLocales,
}: Props) {
  const prefix = locale === siteConfig.defaultLocale ? '' : `/${locale}`;
  const pathname = usePathname();
  const mobileDetailsRef = useRef<HTMLDetailsElement>(null);
  const tn = useTranslations('nav');

  // Close mobile menu on route changes
  useEffect(() => {
    mobileDetailsRef.current?.removeAttribute('open');
  }, [pathname]);

  // Close mobile menu on outside pointerdown or Escape key
  useEffect(() => {
    function handlePointerDown(e: MouseEvent | TouchEvent) {
      if (
        mobileDetailsRef.current?.hasAttribute('open') &&
        !mobileDetailsRef.current.contains(e.target as Node)
      ) {
        mobileDetailsRef.current.removeAttribute('open');
      }
    }
    function handleKeyDown(e: KeyboardEvent) {
      if (e.key === 'Escape' && mobileDetailsRef.current?.hasAttribute('open')) {
        mobileDetailsRef.current.removeAttribute('open');
      }
    }
    document.addEventListener('pointerdown', handlePointerDown);
    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('pointerdown', handlePointerDown);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  const closeMobileMenu = () => {
    mobileDetailsRef.current?.removeAttribute('open');
  };

  return (
    <header className="sticky top-0 z-30 w-full border-b border-border bg-background/95 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-3 px-4">
        <div className="flex items-center gap-2">
          {/* Mobile hub menu with dismiss on navigation and outside click */}
          <details ref={mobileDetailsRef} className="group relative md:hidden">
            <summary
              aria-label={tn('openMenu')}
              className="flex h-8 w-8 cursor-pointer list-none items-center justify-center rounded-md border border-border text-muted-foreground marker:content-['']"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden="true">
                <path d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </summary>
            <nav className="absolute left-0 top-full z-50 mt-1 max-h-[70vh] min-w-[15rem] overflow-y-auto rounded-lg border border-border bg-background py-1 shadow-lg">
              {navItems.map((item) => (
                <div key={item.key}>
                  <Link
                    href={item.href}
                    onClick={closeMobileMenu}
                    className="block px-3 py-2 text-sm font-medium hover:bg-muted"
                  >
                    {item.label}
                  </Link>
                  {item.items.length > 0 && (
                    <ul className="pb-1">
                      {item.items.map((sub) => (
                        <li key={sub.href}>
                          <Link
                            href={sub.href}
                            onClick={closeMobileMenu}
                            className="block px-6 py-1.5 text-xs leading-snug text-muted-foreground hover:text-foreground"
                          >
                            {sub.title}
                          </Link>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </nav>
          </details>

          <Link
            href={prefix || '/'}
            className="flex items-center gap-2 transition hover:opacity-80"
            title={siteConfig.fullName}
            aria-label={siteConfig.fullName}
          >
            {/* Generated mark: a fish silhouette in the theme colour, regenerated
                per site by scripts/make_logo.py from config/brand-mark.json. */}
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src="/logo.svg"
              alt={`${siteConfig.fullName} logo`}
              width={36}
              height={36}
              className="h-9 w-9 rounded-lg"
            />
            <span className="hidden text-sm font-bold leading-tight min-[360px]:inline sm:text-lg sm:leading-normal">
              {siteConfig.name}{' '}
              <span className="text-primary font-extrabold">Wiki</span>
            </span>
          </Link>
        </div>

        <nav aria-label="Main" className="hidden items-center gap-5 text-sm md:flex">
          {navItems.map((item) => (
            <NavDropdown key={item.key} label={item.label} href={item.href} items={item.items} />
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <SearchDialog locale={locale} />
          <LocaleSwitcher
            locale={locale}
            available={availableLocales}
            routes={localeRoutes}
            configured={configuredLocales}
          />
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
