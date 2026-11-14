'use client';

import { useEffect, useRef, useState } from 'react';
import { useTranslations } from 'next-intl';
import { siteConfig } from '@/config/site.config';
import { cn } from '@/lib/utils';
import { loadYouTubeApi } from '@/lib/youtube';

/**
 * Click-to-load official trailer.
 *
 * A raw <video> or YouTube <iframe> on the home page costs hundreds of kilobytes
 * to a megabyte before the visitor has asked for anything, and it lands directly
 * on the LCP element. So the first render is only a poster image, and the player
 * is mounted on click.
 *
 * Two sources are supported because neither is universally available:
 *  - YouTube, when the developer publishes there (needs a real video id).
 *  - Steam's CDN, which still serves the movie files even though the public API
 *    payload now exposes only DASH/HLS manifests.
 */
export function TrailerEmbed({ className, video }: {
  className?: string;
  video?: { id: string; title: string; start?: number };
}) {
  const youtubeId = video?.id ?? siteConfig.media.youtubeId;
  const steamMovieId = video ? '' : siteConfig.media.steamMovieId;
  const title = video?.title ?? (siteConfig.media.trailerTitle || `${siteConfig.name} official trailer`);
  const trailerCredit = video ? '' : siteConfig.media.trailerCredit;
  // Article videos use the official YouTube thumbnail as their poster. It is
  // the publisher's own still for that video, so the preview matches what plays.
  const poster = video
    ? `https://i.ytimg.com/vi/${video.id}/hqdefault.jpg`
    : (siteConfig.media.trailerPoster || siteConfig.heroImage);
  const start = video?.start;
  const articleVideo = Boolean(video);
  const [playing, setPlaying] = useState(false);
  const [error, setError] = useState(false);
  const playerTarget = useRef<HTMLDivElement>(null);
  const trigger = useRef<HTMLButtonElement>(null);
  const moveFocus = useRef(false);
  const t = useTranslations('video');

  useEffect(() => {
    if (!playing || !youtubeId || !playerTarget.current) return;
    let cancelled = false;
    let player: { destroy(): void } | undefined;
    void loadYouTubeApi().then((api) => {
      if (cancelled || !playerTarget.current) return;
      player = new api.Player(playerTarget.current, {
        host: 'https://www.youtube-nocookie.com',
        width: '100%',
        height: '100%',
        videoId: youtubeId,
        playerVars: articleVideo
          ? { autoplay: 1, ...(start !== undefined ? { start } : {}), rel: 0, playsinline: 1 }
          : { autoplay: 1, mute: 1, loop: 1, playlist: youtubeId, rel: 0, playsinline: 1 },
        events: {
          onReady: (event: { target: { getIframe(): HTMLIFrameElement } }) => {
            const iframe = event.target.getIframe();
            iframe.title = title;
            if (moveFocus.current && document.activeElement === document.body) iframe.focus();
          },
          onError: () => { setError(true); setPlaying(false); },
        },
      });
    }).catch(() => {
      if (!cancelled) { setError(true); setPlaying(false); }
    });
    return () => { cancelled = true; player?.destroy(); };
  }, [playing, youtubeId, start, title, articleVideo]);

  useEffect(() => {
    if (playing && error) trigger.current?.focus();
  }, [error, playing]);

  if ((!youtubeId && !steamMovieId) || (video && !/^[a-zA-Z0-9_-]{11}$/.test(video.id))) return null;

  return (
    <figure className={cn('relative overflow-hidden rounded-2xl border border-border', className)}>
      {playing ? (
        <div className="relative aspect-video">
          {youtubeId ? (
            <div ref={playerTarget} className="absolute inset-0 h-full w-full" aria-label={title} />
          ) : (
            <video
              src={`https://cdn.akamai.steamstatic.com/steam/apps/${steamMovieId}/movie480.mp4`}
              poster={poster || undefined}
              controls
              autoPlay
              playsInline
              className="absolute inset-0 h-full w-full bg-black"
            />
          )}
        </div>
      ) : (
        <button
          ref={trigger}
          type="button"
          aria-label={t('play', { title })}
          onClick={(event) => {
            moveFocus.current = document.activeElement === event.currentTarget;
            setError(false);
            setPlaying(true);
          }}
          className="group relative block aspect-video w-full bg-muted focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
        >
          {poster && (
            /* eslint-disable-next-line @next/next/no-img-element */
            <img
              src={poster}
              alt=""
              width={1280}
              height={720}
              loading="lazy"
              className="absolute inset-0 h-full w-full object-cover transition duration-300 group-hover:scale-[1.02]"
              // Keep failed posters on the site's own image host; never retry in a loop.
              onError={(event) => {
                const img = event.currentTarget;
                const fallback = siteConfig.heroImage;
                if (fallback && img.getAttribute('src') !== fallback) {
                  img.src = fallback;
                }
              }}
            />
          )}
          <span className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/10 to-transparent" />
          <span className="absolute left-1/2 top-1/2 flex h-16 w-16 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full bg-red-600 shadow-lg transition group-hover:scale-110">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="#fff" aria-hidden="true">
              <path d="M8 5v14l11-7z" />
            </svg>
          </span>
          {!articleVideo && (
            <span className="absolute bottom-0 left-0 right-0 p-4 text-left">
              <span className="block text-base font-semibold text-white drop-shadow sm:text-lg">{title}</span>
              {trailerCredit && (
                <span className="mt-0.5 block text-xs text-white/80">{t('officialTrailer')} · {trailerCredit}</span>
              )}
            </span>
          )}
        </button>
      )}
      {error && (
        <p role="alert" className="px-4 py-2 text-sm text-muted-foreground">
          {t('unavailable')}{' '}
          <a href={`https://www.youtube.com/watch?v=${youtubeId}${start ? `&t=${start}` : ''}`} target="_blank" rel="noopener noreferrer" className="font-medium text-primary underline underline-offset-2" onClick={() => { moveFocus.current = false; }}>
            {t('watchOnYouTube')}
          </a>
        </p>
      )}
      {youtubeId && (
        <figcaption className="flex items-start justify-between gap-3 border-t border-border/50 bg-background/80 px-4 py-2 text-xs text-muted-foreground">
          <span className="min-w-0">
            <span className="block font-medium text-foreground">
              {title}
              {trailerCredit ? ` · ${trailerCredit}` : ''}
            </span>
            <span className="mt-0.5 block">{t('unofficial')}</span>
          </span>
          <a
            href={`https://www.youtube.com/watch?v=${youtubeId}${start ? `&t=${start}` : ''}`}
            target="_blank"
            rel="noopener noreferrer"
            className="flex shrink-0 items-center gap-1 font-medium text-foreground hover:text-primary hover:underline"
          >
            <span>{t('watchOnYouTube')}</span>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
              <polyline points="15 3 21 3 21 9" />
              <line x1="10" y1="14" x2="21" y2="3" />
            </svg>
          </a>
        </figcaption>
      )}
    </figure>
  );
}
