'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect, useRef, useState } from 'react';
import { siteConfig } from '@/config/site.config';

export const LOCALE_LABELS: Record<string, string> = {
  en: 'English',
  es: 'Español',
  de: 'Deutsch',
  fr: 'Français',
  it: 'Italiano',
  pt: 'Português',
  'pt-BR': 'Português (BR)',
  ru: 'Русский',
  ja: '日本語',
  ko: '한국어',
  zh: '中文',
  vi: 'Tiếng Việt',
  th: 'ไทย',
  id: 'Bahasa Indonesia',
  tr: 'Türkçe',
  pl: 'Polski',
  nl: 'Nederlands',
  ar: 'العربية',
  hi: 'हिन्दी',
};

export type LocaleRouteMap = Record<string, string[]>;

/** English-only boilerplate; prefixed copies canonicalise to the default locale. */
const NON_TRANSLATED_PATHS = new Set(['about', 'contact', 'privacy', 'terms']);

/**
 * Builds the equivalent URL in another locale for the CURRENT page.
 *
 * Two rules, in order:
 *  1. If the page exists in the target locale, keep the reader in place — someone
 *     reading a tier list who switches to Japanese wants the Japanese tier list.
 *  2. If it does not exist yet, fall back to that locale's home page. Linking to a
 *     page that was never translated would 404, which is worse than losing the
 *     reader's position: translation happens in batches, so partial coverage is
 *     the normal state, not an edge case.
 */
export function localeHref(
  pathname: string,
  target: string,
  defaultLocale: string,
  locales: readonly string[],
  routes?: LocaleRouteMap,
): string {
  const segments = pathname.split('/').filter(Boolean);
  const hasLocalePrefix =
    segments.length > 0 && locales.includes(segments[0]) && segments[0] !== defaultLocale;
  const rest = hasLocalePrefix ? segments.slice(1) : segments;
  const base = target === defaultLocale ? '' : `/${target}`;

  if (rest.length === 0) return base || '/';

  // Legal pages exist only in English. Sending a reader to /de/about would serve
  // the same English text at a second URL, so the switcher goes to that locale's
  // home instead of a prefixed duplicate.
  if (rest.length === 1 && NON_TRANSLATED_PATHS.has(rest[0])) return base || '/';

  // `rest` is either [hub] (a hub page) or [hub, slug] (a spoke page).
  const key = rest.join('/');
  const exists = routes?.[target]?.includes(key);

  return exists || routes === undefined
    ? `${base}/${key}`.replace(/\/+$/, '')
    : base || '/';
}

type Props = {
  locale: string;
  /** Locales that actually have content — offered as switch targets. */
  available: string[];
  /** locale -> list of "hub" and "hub/slug" paths that exist in that locale. */
  routes?: LocaleRouteMap;
  /** Every locale the site is configured for, translated or not. */
  configured?: string[];
};

export function LocaleSwitcher({ locale, available, routes, configured }: Props) {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  // Dismiss on outside click and on Escape, so the menu never traps the reader.
  useEffect(() => {
    if (!open) return;
    const onPointerDown = (event: MouseEvent) => {
      if (!containerRef.current?.contains(event.target as Node)) setOpen(false);
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

  // Close after navigating, for the same reason the nav dropdown does.
  useEffect(() => setOpen(false), [pathname]);

  // Only offer locales that have real content generated (available).
  // In Next.js static export (output: 'export'), routes for locales without content
  // do not exist and will 404 on Cloudflare Pages.
  const targets = (available ?? []).filter((l) => siteConfig.locales.includes(l));
  if (targets.length < 2) return null;
  const translated = new Set(available);

  const current = LOCALE_LABELS[locale] ?? locale;

  return (
    <div ref={containerRef} className="relative">
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        aria-haspopup="menu"
        aria-expanded={open}
        aria-label={`Language: ${current}`}
        className="inline-flex h-8 items-center gap-1.5 rounded-md border border-border px-2 text-xs text-muted-foreground transition hover:bg-muted hover:text-foreground"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
          <circle cx="12" cy="12" r="10" />
          <path d="M2 12h20M12 2a15 15 0 0 1 0 20a15 15 0 0 1 0-20" />
        </svg>
        <span className="uppercase">{locale}</span>
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" aria-hidden="true">
          <path d="m6 9 6 6 6-6" />
        </svg>
      </button>

      {open && (
        <div
          role="menu"
          className="absolute right-0 top-full z-50 mt-1 min-w-[12rem] overflow-hidden rounded-lg border border-border bg-background py-1 shadow-lg"
        >
          {targets.map((target) => {
            const isCurrent = target === locale;
            const href = localeHref(
              pathname,
              target,
              siteConfig.defaultLocale,
              siteConfig.locales as unknown as string[],
              routes,
            );
            return (
              <Link
                key={target}
                role="menuitem"
                href={href}
                hrefLang={target}
                onClick={() => setOpen(false)}
                aria-current={isCurrent ? 'true' : undefined}
                title={
                  translated.has(target)
                    ? undefined
                    : `${LOCALE_LABELS[target] ?? target} translation in progress — showing English for now`
                }
                className={
                  isCurrent
                    ? 'flex items-center justify-between gap-3 bg-muted/60 px-3 py-2 text-sm font-medium'
                    : 'flex items-center justify-between gap-3 px-3 py-2 text-sm text-muted-foreground transition hover:bg-muted hover:text-foreground'
                }
              >
                <span>{LOCALE_LABELS[target] ?? target}</span>
                <span className="flex items-center gap-1.5">
                  {!translated.has(target) && (
                    <span className="rounded bg-muted px-1 py-0.5 text-[9px] uppercase text-muted-foreground">
                      en
                    </span>
                  )}
                  <span className="text-[10px] uppercase text-muted-foreground">{target}</span>
                </span>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}
