'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { useTranslations } from 'next-intl';
import { siteConfig } from '@/config/site.config';
import { slugifyHeading } from '@/lib/slug';
import { entryHref, queryTokens, searchEntries, type SearchEntry } from '@/lib/search';
import { HighlightedText } from '@/components/HighlightedText';

type Status = 'idle' | 'loading' | 'ready' | 'error';

/**
 * Search results for the crawlable /search page.
 *
 * The header dialog is the shortcut; this page is the shareable, no-JS-safe form
 * and the landing target for the homepage search box. The index is only fetched
 * when there is a query, so opening /search costs no extra request.
 */
export function SearchPanel({ locale }: { locale: string }) {
  const t = useTranslations('search');
  const th = useTranslations('home');
  const [query, setQuery] = useState('');
  const [entries, setEntries] = useState<SearchEntry[]>([]);
  const [status, setStatus] = useState<Status>('idle');
  const prefix = locale === siteConfig.defaultLocale ? '' : `/${locale}`;

  useEffect(() => {
    const sync = () => {
      const next = new URLSearchParams(window.location.search).get('q')?.slice(0, 200) ?? '';
      setQuery(next);
    };
    sync();
    window.addEventListener('popstate', sync);
    window.addEventListener('pageshow', sync);
    return () => {
      window.removeEventListener('popstate', sync);
      window.removeEventListener('pageshow', sync);
    };
  }, []);

  const trimmedQuery = query.trim();
  const searching = trimmedQuery.length >= 2;

  useEffect(() => {
    if (trimmedQuery.length < 2 || entries.length > 0) return;
    let cancelled = false;
    setStatus('loading');
    fetch('/search-index.json')
      .then((response) => {
        if (!response.ok) throw new Error(String(response.status));
        return response.json() as Promise<SearchEntry[]>;
      })
      .then((data) => {
        if (cancelled) return;
        setEntries(data.filter((entry) => entry.locale === locale));
        setStatus('ready');
      })
      .catch(() => {
        if (!cancelled) setStatus('error');
      });
    return () => {
      cancelled = true;
    };
  }, [trimmedQuery, entries.length, locale]);

  const tokens = useMemo(() => queryTokens(trimmedQuery), [trimmedQuery]);
  const results = useMemo(
    () => (searching && entries.length > 0 ? searchEntries(entries, trimmedQuery, 30) : []),
    [entries, searching, trimmedQuery],
  );

  return (
    <>
      <form action={`${prefix}/search`} method="get" role="search" className="search-form">
        <label htmlFor="search-page-query" className="sr-only">
          {t('title')}
        </label>
        <input
          id="search-page-query"
          name="q"
          type="search"
          required
          minLength={2}
          maxLength={200}
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder={th('searchPlaceholder')}
          autoComplete="off"
          spellCheck={false}
          className="search-input"
        />
        <button type="submit" className="search-submit">
          {th('searchSubmit')}
        </button>
      </form>

      <p className="sr-only" role="status" aria-live="polite">
        {!searching && trimmedQuery.length > 0
          ? t('dialogHint')
          : searching && status === 'loading'
            ? t('loading')
            : searching && status === 'error'
              ? t('unavailable')
              : searching && status === 'ready'
                ? results.length > 0
                  ? t('results', { count: results.length, query })
                  : t('noResults', { query })
                : ''}
      </p>

      {!searching && trimmedQuery.length > 0 && (
        <p className="mt-4 text-sm text-muted-foreground">{t('dialogHint')}</p>
      )}

      <div className="mt-8">
        {searching && status === 'loading' && (
          <p className="text-sm text-muted-foreground">{t('loading')}</p>
        )}
        {searching && status === 'error' && (
          <p role="alert" className="rounded-lg border border-border bg-muted/50 p-4 text-sm">
            {t('unavailable')}
          </p>
        )}
        {searching && status === 'ready' && results.length === 0 && (
          <p className="rounded-lg border border-border bg-muted/50 p-4 text-sm">{t('noResults', { query })}</p>
        )}
        {searching && results.length > 0 && (
          <>
            <h2 className="text-lg font-bold">{t('results', { count: results.length, query })}</h2>
            <ul className="mt-4 space-y-4">
              {results.map(({ entry }) => {
                const href = entryHref(prefix, entry);
                // Legal pages render their headings without ids, so a deep link
                // there would land on the top of the page. Keep the result but
                // omit section links until the legal renderer emits anchors.
                const headings = entry.hub === 'legal'
                  ? []
                  : entry.headings
                      .filter((heading) => tokens.some((token) => heading.toLowerCase().includes(token)))
                      .slice(0, 3);
                return (
                  <li key={`${entry.locale}-${entry.slug}`} className="rounded-xl border border-border p-4">
                    <Link href={href} className="search-result-link font-semibold hover:underline">
                      <HighlightedText text={entry.title} tokens={tokens} />
                    </Link>
                    <p className="mt-1 line-clamp-2 text-sm text-muted-foreground">
                      <HighlightedText text={entry.description} tokens={tokens} />
                    </p>
                    {headings.length > 0 && (
                      <ul className="mt-3 space-y-1">
                        {headings.map((heading) => (
                          <li key={heading}>
                            <Link
                              href={`${href}#${slugifyHeading(heading)}`}
                              aria-label={`${t('inSection')}: ${heading} — ${entry.title}`}
                              className="text-sm text-muted-foreground underline-offset-4 hover:text-primary hover:underline"
                            >
                              ↳ <HighlightedText text={heading} tokens={tokens} />
                            </Link>
                          </li>
                        ))}
                      </ul>
                    )}
                  </li>
                );
              })}
            </ul>
          </>
        )}
      </div>
    </>
  );
}
