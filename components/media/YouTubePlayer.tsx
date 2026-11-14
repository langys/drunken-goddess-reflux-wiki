'use client';

import { useCallback, useEffect, useId, useRef, useState } from 'react';

interface Props {
  videoId: string;
  className?: string;
  aspectRatio?: string;
}

/**
 * Production-grade YouTube IFrame Player API Component.
 *
 * Reverses the immersive background/hero trailer experience:
 * 1. Loads YouTube IFrame API on-demand with singleton protection.
 * 2. Background autoplays muted in an infinite loop without controls clutter.
 * 3. Provides custom glassmorphism mute/unmute control.
 * 4. Gracefully recovers if strict browser autoplay policies block unmuting
 *    by recreating the player at the exact current timestamp.
 * 5. Cleans up player instances to prevent SPA memory leaks.
 */
export function YouTubePlayer({ videoId, className = '', aspectRatio = '16 / 9' }: Props) {
  const containerWrapperRef = useRef<HTMLDivElement | null>(null);
  const playerRef = useRef<any>(null);
  const playerId = `yt-player-${useId().replace(/:/g, '')}`;

  const [isMuted, setIsMuted] = useState(true);
  const [isReady, setIsReady] = useState(false);
  const scriptLoadingRef = useRef(false);

  const initPlayer = useCallback(
    (muted: boolean, startTime = 0) => {
      const existingContainer = document.getElementById(playerId);
      if (existingContainer && existingContainer.parentNode) {
        const replacementDiv = document.createElement('div');
        replacementDiv.id = playerId;
        replacementDiv.className = 'w-full h-full';
        existingContainer.parentNode.replaceChild(replacementDiv, existingContainer);
      }

      if (!(window as any).YT?.Player) return;

      playerRef.current = new (window as any).YT.Player(playerId, {
        videoId,
        playerVars: {
          autoplay: 1,
          mute: muted ? 1 : 0,
          loop: 1,
          playlist: videoId, // In YouTube API, loop: 1 requires playlist to be set to videoId
          controls: 0,
          showinfo: 0,
          rel: 0,
          modestbranding: 1,
          playsinline: 1,
          start: Math.floor(startTime),
        },
        events: {
          onReady: () => {
            setIsReady(true);
            if (!muted) {
              playerRef.current?.setVolume(100);
              playerRef.current?.playVideo();
            }
          },
        },
      });
    },
    [videoId, playerId],
  );

  const toggleMute = useCallback(() => {
    const player = playerRef.current;
    if (!player) return;

    if (isMuted) {
      // Unmute request
      player.unMute();
      player.setVolume(100);
      player.playVideo();

      // Browser autoplay policy verification
      setTimeout(() => {
        if (playerRef.current?.isMuted()) {
          // If browser policy blocked unmuting, recreate player with audio starting at current second
          const currentTime = playerRef.current?.getCurrentTime() ?? 0;
          playerRef.current?.destroy();
          playerRef.current = null;
          setIsReady(false);
          initPlayer(false, currentTime);
        }
      }, 300);

      setIsMuted(false);
    } else {
      // Mute request
      player.mute();
      setIsMuted(true);
    }
  }, [isMuted, initPlayer]);

  useEffect(() => {
    const onApiReady = () => {
      initPlayer(true);
    };

    if ((window as any).YT?.Player) {
      onApiReady();
    } else if (scriptLoadingRef.current) {
      const interval = setInterval(() => {
        if ((window as any).YT?.Player) {
          clearInterval(interval);
          onApiReady();
        }
      }, 100);
      return () => clearInterval(interval);
    } else {
      scriptLoadingRef.current = true;
      const script = document.createElement('script');
      script.src = 'https://www.youtube.com/iframe_api';
      const firstScript = document.getElementsByTagName('script')[0];
      firstScript?.parentNode?.insertBefore(script, firstScript);

      window.onYouTubeIframeAPIReady = () => {
        window.onYouTubeIframeAPIReady = undefined;
        onApiReady();
      };
    }

    return () => {
      if (playerRef.current) {
        playerRef.current.destroy();
        playerRef.current = null;
      }
    };
  }, [initPlayer]);

  return (
    <div className={`relative w-full overflow-hidden rounded-2xl ${className}`} style={{ aspectRatio }}>
      <div ref={containerWrapperRef} className="w-full h-full pointer-events-none">
        <div id={playerId} className="w-full h-full" />
      </div>

      {isReady && (
        <button
          type="button"
          onClick={toggleMute}
          className="absolute bottom-3 left-3 z-10 flex items-center gap-1.5 rounded-lg bg-black/60 px-2.5 py-1.5 text-white/80 hover:bg-black/80 hover:text-white transition-colors backdrop-blur-sm border border-white/10"
          aria-label={isMuted ? 'Unmute video audio' : 'Mute video audio'}
        >
          {isMuted ? (
            // VolumeX Icon
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M11 4.702a.705.705 0 0 0-1.203-.498L6.413 7.587A1.4 1.4 0 0 1 5.416 8H3a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2.416a1.4 1.4 0 0 1 .997.413l3.383 3.384A.705.705 0 0 0 11 19.298z" />
              <line x1="22" y1="9" x2="16" y2="15" />
              <line x1="16" y1="9" x2="22" y2="15" />
            </svg>
          ) : (
            // Volume2 Icon
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M11 4.702a.705.705 0 0 0-1.203-.498L6.413 7.587A1.4 1.4 0 0 1 5.416 8H3a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2.416a1.4 1.4 0 0 1 .997.413l3.383 3.384A.705.705 0 0 0 11 19.298z" />
              <path d="M16 9a5 5 0 0 1 0 6" />
              <path d="M19.364 18.364a9 9 0 0 0 0-12.728" />
            </svg>
          )}
          <span className="text-xs font-medium">{isMuted ? 'Sound Off' : 'Sound On'}</span>
        </button>
      )}
    </div>
  );
}
