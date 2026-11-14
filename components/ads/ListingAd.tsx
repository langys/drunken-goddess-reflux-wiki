import { siteConfig } from '@/config/site.config';
import { validAdsterraPlacement } from '@/lib/adsterra';
import { AdPlacement } from './AdPlacement';
import { AdPreview } from './AdPreview';

/**
 * The site's only banner row: one 728×90 leaderboard, placed once per page.
 *
 * Phones never mount it — the container query hides the row below 728px of
 * available width, which is the creative's own width. That is deliberate: the
 * mobile inventory is the single 320×50 dock, so no page carries two banner
 * formats side by side. Gate on container width, not viewport width, because
 * home and hub pages lose 240–300px to the index rail before the row is drawn.
 */
export function ListingAd({ className = '' }: { className?: string }) {
  const placement = siteConfig.ads.adsterra.leaderboard;
  const live = siteConfig.ads.enabled && validAdsterraPlacement(placement, 'banner');
  if (!live && !siteConfig.ads.preview) return null;

  return (
    <div className={`ad-size-container ${className}`}>
      <div className="listing-ad-wide">
        {live
          ? <AdPlacement placement={placement} size={{ width: 728, height: 90 }} />
          : <AdPreview width={728} height={90} name="leaderboard" />}
      </div>
    </div>
  );
}
