'use client';

import { useTranslations } from 'next-intl';

/**
 * Nominal-size placeholder for `NEXT_PUBLIC_AD_PREVIEW=1`.
 *
 * It exists so a placement can be reviewed at its real dimensions before
 * Adsterra issues a key, and so a reviewer can see exactly what a phone never
 * receives. It never loads a script and never ships in a production build.
 */
export function AdPreview({ width, height, name, showLabel = true }: {
  width: number;
  height: number;
  name: string;
  /** The dock supplies its own Sponsored toolbar, exactly like a live unit. */
  showLabel?: boolean;
}) {
  const t = useTranslations('common');
  return (
    <div
      className="ad-preview"
      data-ad-preview={name}
      style={{ width, height, maxWidth: '100%' }}
      aria-hidden="true"
    >
      {showLabel && <span className="ad-preview-label">{t('sponsored')}</span>}
      <span className="ad-preview-name">{name}</span>
      <span className="ad-preview-size">
        {width} × {height}
      </span>
    </div>
  );
}
