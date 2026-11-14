'use client';

import { useEffect, useRef } from 'react';
import { useTranslations } from 'next-intl';
import { siteConfig } from '@/config/site.config';
import { observeAdsterraSlot, validAdsterraPlacement, type Placement, type AdSize } from '@/lib/adsterra';

export type { Placement } from '@/lib/adsterra';

/** Load publisher code in the main document; only the network creates creative iframes. */
export function AdPlacement({
  placement,
  size,
  className = '',
  persistent = false,
  fluid = false,
  showLabel = true,
}: {
  placement: Placement;
  size?: AdSize;
  className?: string;
  persistent?: boolean;
  fluid?: boolean;
  /** A containing Sponsored toolbar may supply the visible label instead. */
  showLabel?: boolean;
}) {
  const t = useTranslations('common');
  const enabled = siteConfig.ads.enabled && validAdsterraPlacement(placement, size ? 'banner' : 'native');
  const { key, scriptUrl } = placement;
  const host = useRef<HTMLDivElement>(null);
  const width = size?.width;
  const height = size?.height;

  useEffect(() => {
    if (!enabled || !host.current) return;
    return observeAdsterraSlot(host.current, { key, scriptUrl }, width && height ? { width, height } : undefined);
  }, [enabled, key, scriptUrl, width, height, persistent]);

  if (!enabled) return null;
  return (
    <div className="ad-placement" style={{ width: fluid ? '100%' : width, maxWidth: '100%' }}>
      {showLabel && <span className="ad-sponsored-label">{t('sponsored')}</span>}
      <div
        ref={host}
        className={`ad-frame-container ${className}`}
        aria-label={t('sponsored')}
        data-ad-placement={placement.key}
        data-ad-format={size ? 'banner' : 'native'}
        style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: 1, minHeight: height ?? 420, width: fluid ? '100%' : width, maxWidth: '100%' }}
      >
        {/* Native's SDK watches navigation and needs its destination before loading. */}
        {!size && <div id={`container-${key}`} style={{ width: '100%' }} />}
      </div>
    </div>
  );
}
