type YouTubePlayer = { destroy(): void };
type YouTubeApi = { Player: new (target: HTMLElement, options: Record<string, unknown>) => YouTubePlayer };

declare global {
  interface Window {
    YT?: YouTubeApi;
    __ytApiLoadingPromise?: Promise<YouTubeApi>;
    onYouTubeIframeAPIReady?: () => void;
  }
}

/** Load on user interaction. A shared promise prevents duplicate scripts across players. */
export function loadYouTubeApi(): Promise<YouTubeApi> {
  if (window.YT?.Player) return Promise.resolve(window.YT);
  if (window.__ytApiLoadingPromise) return window.__ytApiLoadingPromise;

  window.__ytApiLoadingPromise = new Promise<YouTubeApi>((resolve, reject) => {
    const tag = document.createElement('script');
    const previous = window.onYouTubeIframeAPIReady;
    let settled = false;
    const timeout = window.setTimeout(() => fail(new Error('Video service timed out')), 4000);
    const fail = (error: Error) => {
      if (settled) return;
      settled = true;
      window.clearTimeout(timeout);
      tag.remove();
      window.onYouTubeIframeAPIReady = previous;
      window.__ytApiLoadingPromise = undefined;
      reject(error);
    };
    window.onYouTubeIframeAPIReady = () => {
      previous?.();
      if (!window.YT?.Player) return fail(new Error('Video service unavailable'));
      if (settled) return;
      settled = true;
      window.clearTimeout(timeout);
      resolve(window.YT);
    };
    tag.async = true;
    tag.src = 'https://www.youtube.com/iframe_api';
    tag.onerror = () => fail(new Error('Video service unavailable'));
    document.head.appendChild(tag);
  });
  return window.__ytApiLoadingPromise;
}
