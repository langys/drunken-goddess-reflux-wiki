'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { useTranslations } from 'next-intl';
import { siteConfig } from '@/config/site.config';
import { validAdsterraPlacement } from '@/lib/adsterra';
import { AdPlacement } from './AdPlacement';
import { AdPreview } from './AdPreview';

const dismissalKey = 'sponsored-banner-dismissed';

/** Compact dock below the desktop rail breakpoint; never scales the creative. */
export function SponsoredBanner() {
  const t = useTranslations('common');
  const ads = siteConfig.ads.adsterra;
  const mobile = validAdsterraPlacement(ads.dock, 'banner');
  const enabled = siteConfig.ads.enabled && (mobile || siteConfig.ads.preview);
  const [activated, setActivated] = useState(false);
  const [open, setOpen] = useState(false);
  const [dismissed, setDismissed] = useState(false);
  const banner = useRef<HTMLElement>(null);
  const reserve = useRef<HTMLDivElement>(null);
  const previousFocus = useRef<HTMLElement | null>(null);

  const close = useCallback(() => {
    setDismissed(true);
    try { window.sessionStorage.setItem(dismissalKey, '1'); } catch {}
    const visible = (element: HTMLElement) => {
      const rect = element.getBoundingClientRect();
      return element.isConnected && rect.height > 0 && rect.top >= 84 && rect.bottom <= window.innerHeight;
    };
    const target = previousFocus.current && visible(previousFocus.current)
      ? previousFocus.current
      : Array.from(document.querySelectorAll<HTMLElement>('main p, main h2, main h3, [data-sponsored-trigger]')).find(visible);
    if (target) {
      if (!target.hasAttribute('tabindex') && !target.matches('a, button, input, select, textarea')) {
        target.setAttribute('tabindex', '-1');
        target.addEventListener('blur', () => target.removeAttribute('tabindex'), { once: true });
      }
      target.focus({ preventScroll: true });
    }
  }, []);

  useEffect(() => {
    if (!enabled || dismissed) return;
    try {
      if (window.sessionStorage.getItem(dismissalKey) === '1') {
        setDismissed(true);
        return;
      }
    } catch { /* The close control also works when storage is unavailable. */ }

    let reached = false;
    let frame = 0;
    const update = () => {
      frame = 0;
      const target = document.querySelector('.reading-article .article-body h2, [data-sponsored-trigger]');
      const fits = window.innerWidth >= 320 && window.innerWidth < 1360 && window.innerHeight > 480;
      const remainingScroll = document.documentElement.scrollHeight - window.innerHeight;
      const reading = remainingScroll < 240 || window.scrollY >= 240;
      // Computed CSS height includes safe-area insets, even on this hidden marker.
      const dockHeight = reserve.current ? parseFloat(getComputedStyle(reserve.current).height) : 104;
      const footer = document.querySelector('[data-site-footer]');
      const atFooter = !!footer && footer.getBoundingClientRect().top <= window.innerHeight - dockHeight - 8;
      const inDialog = !!document.querySelector('[role="dialog"][aria-modal="true"], dialog[open]');
      if (!reached && fits && reading && !atFooter && !inDialog && target && target.getBoundingClientRect().top <= window.innerHeight * 0.65) {
        reached = true;
        setActivated(true);
      }
      setOpen(reached && fits && !atFooter && !inDialog);
    };
    const schedule = () => {
      if (!frame) frame = window.requestAnimationFrame(update);
    };
    schedule();
    window.addEventListener('scroll', schedule, { passive: true });
    window.addEventListener('resize', schedule);
    window.addEventListener('pageshow', schedule);
    document.addEventListener('focusin', schedule);
    document.addEventListener('focusout', schedule);
    return () => {
      window.cancelAnimationFrame(frame);
      window.removeEventListener('scroll', schedule);
      window.removeEventListener('resize', schedule);
      window.removeEventListener('pageshow', schedule);
      document.removeEventListener('focusin', schedule);
      document.removeEventListener('focusout', schedule);
    };
  }, [enabled, dismissed]);

  useEffect(() => {
    if (!enabled) return;
    const root = document.documentElement;
    root.dataset.adDock = open && !dismissed ? 'shown' : 'hidden';
    // Preserve the lifecycle probe contract after retiring the wide dock.
    root.dataset.adDockFormat = 'compact';
    return () => {
      delete root.dataset.adDock;
      delete root.dataset.adDockFormat;
    };
  }, [enabled, open, dismissed]);

  useEffect(() => {
    if (!open || dismissed) return;
    const protectFocus = (event: FocusEvent) => {
      const target = event.target;
      const dock = banner.current;
      if (!(target instanceof HTMLElement) || !dock || dock.contains(target) || target.closest('[role="dialog"]')) return;
      if (target.closest('[data-site-footer]')) {
        setOpen(false);
        return;
      }
      previousFocus.current = target;
      const rect = target.getBoundingClientRect();
      const top = parseFloat(getComputedStyle(document.querySelector('.site-content') ?? document.body).getPropertyValue('--reading-sticky-top')) || 72;
      if (rect.bottom > dock.getBoundingClientRect().top || rect.top < top) {
        target.scrollIntoView({ block: 'center', behavior: 'instant' });
      }
    };
    const escape = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && banner.current?.contains(document.activeElement)) {
        event.preventDefault();
        close();
      }
    };
    document.addEventListener('focusin', protectFocus);
    document.addEventListener('keydown', escape);
    return () => {
      document.removeEventListener('focusin', protectFocus);
      document.removeEventListener('keydown', escape);
    };
  }, [open, dismissed, close]);

  if (!enabled) return null;

  return (
    <>
      {/* CSS sizing marker only: no document-flow space changes on load/error/close. */}
      <div ref={reserve} className="sponsored-banner-reserve" hidden aria-hidden="true" />
      {activated && !dismissed && (
        <aside ref={banner} className="sponsored-banner" hidden={!open} aria-label={t('sponsored')} data-sponsored-banner="">
          <div className="sponsored-banner-inner">
            <div className="sponsored-banner-toolbar">
              <span className="sponsored-banner-label">{t('sponsored')}</span>
              <button type="button" className="sponsored-banner-close" aria-label={t('closeSponsored')} onClick={close}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18" /></svg>
              </button>
            </div>
            {mobile
              ? <AdPlacement placement={ads.dock} size={{ width: 320, height: 50 }} showLabel={false} />
              : <AdPreview width={320} height={50} name="dock" showLabel={false} />}
          </div>
        </aside>
      )}
    </>
  );
}
