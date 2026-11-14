'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import Link from 'next/link';
import { useTranslations } from 'next-intl';
import { siteConfig } from '@/config/site.config';
import { entryHref, queryTokens, searchEntries, type SearchEntry } from '@/lib/search';
import { HighlightedText } from './HighlightedText';

export function SearchDialog({ locale }: { locale: string }) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [entries, setEntries] = useState<SearchEntry[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);
  const t = useTranslations('search');
  const th = useTranslations('home');

  const prefix = locale === siteConfig.defaultLocale ? '' : `/${locale}`;

  // Cmd/Ctrl+K opens search from anywhere — the shortcut readers already expect.
  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault();
        setOpen((value) => !value);
      }
      if (event.key === 'Escape') setOpen(false);
    };
    document.addEventListener('keydown', onKeyDown);
    return () => document.removeEventListener('keydown', onKeyDown);
  }, []);

  // Fetch the index once, on first open. Fetching it at page load would put a
  // network request in front of LCP for a feature most visitors never use.
  useEffect(() => {
    if (!open || entries.length > 0) return;
    let cancelled = false;
    fetch('/search-index.json')
      .then((response) => (response.ok ? response.json() : []))
      .then((data: SearchEntry[]) => {
        if (!cancelled) setEntries(data.filter((entry) => entry.locale === locale));
      })
      .catch(() => {
        if (!cancelled) setEntries([]);
      });
    return () => {
      cancelled = true;
    };
  }, [open, entries.length, locale]);

  useEffect(() => {
    if (open) inputRef.current?.focus();
    else setQuery('');
  }, [open]);

  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : '';
    return () => {
      document.body.style.overflow = '';
    };
  }, [open]);

  const tokens = useMemo(() => queryTokens(query), [query]);
  const results = useMemo(() => searchEntries(entries, query), [entries, query]);

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        aria-label={t('title')}
        aria-keyshortcuts="Meta+K Control+K"
        title={t('triggerTitle')}
        className="inline-flex h-8 items-center gap-2 rounded-md border border-border px-2 text-xs text-muted-foreground transition hover:bg-muted hover:text-foreground sm:px-2.5"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden="true">
          <circle cx="11" cy="11" r="7" />
          <path d="m20 20-3.5-3.5" />
        </svg>
        <span className="hidden lg:inline">{th('searchSubmit')}</span>
      </button>

      {open && (
        <div
          className="fixed inset-0 z-[60] flex items-start justify-center bg-background/80 p-4 pt-[12vh] backdrop-blur-sm"
          role="dialog"
          aria-modal="true"
          aria-label={t('title')}
          onClick={() => setOpen(false)}
        >
          <div
            className="w-full max-w-xl overflow-hidden rounded-xl border border-border bg-background shadow-2xl"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="flex items-center gap-3 border-b border-border px-4">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="shrink-0 text-muted-foreground" aria-hidden="true">
                <circle cx="11" cy="11" r="7" />
                <path d="m20 20-3.5-3.5" />
              </svg>
              <input
                ref={inputRef}
                aria-label={t('title')}
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder={t('dialogPlaceholder', { game: siteConfig.name })}
                className="h-12 w-full bg-transparent text-sm outline-none placeholder:text-muted-foreground"
                autoComplete="off"
                spellCheck={false}
              />
              <button
                type="button"
                onClick={() => setOpen(false)}
                aria-label={`${t('close')} (ESC)`}
                className="shrink-0 rounded border border-border px-1.5 py-0.5 text-[10px] text-muted-foreground"
              >
                ESC
              </button>
            </div>

            <p className="sr-only" role="status" aria-live="polite">
              {query.trim().length < 2
                ? t('dialogHint')
                : entries.length === 0
                  ? ''
                  : results.length === 0
                    ? t('dialogNoResults', { query })
                    : t('results', { count: results.length, query })}
            </p>

            <div className="max-h-[55vh] overflow-y-auto">
              {query.trim().length < 2 && (
                <p className="px-4 py-6 text-center text-sm text-muted-foreground">
                  {t('dialogHint')}
                </p>
              )}

              {query.trim().length >= 2 && results.length === 0 && (
                <p className="px-4 py-6 text-center text-sm text-muted-foreground">
                  {t('dialogNoResults', { query })}
                </p>
              )}

              {results.map(({ entry, matchedHeading }) => (
                <Link
                  key={`${entry.locale}-${entry.slug}`}
                  href={entryHref(prefix, entry)}
                  onClick={() => setOpen(false)}
                  className="block border-b border-border/60 px-4 py-3 transition last:border-0 hover:bg-muted"
                >
                  <p className="text-sm font-medium">
                    <HighlightedText text={entry.title} tokens={tokens} />
                  </p>
                  <p className="mt-0.5 line-clamp-2 text-xs text-muted-foreground">
                    <HighlightedText text={entry.description} tokens={tokens} />
                  </p>
                  {matchedHeading && (
                    <p className="search-result-link mt-1 text-[11px]">
                      ↳ <HighlightedText text={matchedHeading} tokens={tokens} />
                    </p>
                  )}
                </Link>
              ))}
              {results.length > 0 && (
                <Link
                  href={`${prefix}/search?q=${encodeURIComponent(query.trim())}`}
                  onClick={() => setOpen(false)}
                  className="search-result-link block px-4 py-3 text-center text-xs font-medium hover:bg-muted"
                >
                  {t('viewAll')} →
                </Link>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
