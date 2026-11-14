import { siteConfig } from '@/config/site.config';
import { validAdsterraPlacement } from '@/lib/adsterra';
import { AdPlacement } from './AdPlacement';
import { AdPreview } from './AdPreview';

/** A separate grid column, outside both navigation cards and their scroll areas.
 *  `fixed` pins the rail beside the hero so it is visible in the first
 *  viewport (the Belmonts homepage behaviour); the grid column it leaves
 *  behind still reserves the gutter. */
export function ReadingAdRail({ fixed = false }: { fixed?: boolean }) {
  const placement = siteConfig.ads.adsterra.rail;
  const live = siteConfig.ads.enabled && validAdsterraPlacement(placement, 'banner');
  if (!live && !siteConfig.ads.preview) return null;

  return (
    <aside className={fixed ? 'reading-ad-rail reading-ad-rail--fixed' : 'reading-ad-rail'} data-ad-rail="">
      <div className="reading-ad-sticky">
        {live
          ? <AdPlacement placement={placement} size={{ width: 160, height: 600 }} />
          : <AdPreview width={160} height={600} name="rail" />}
      </div>
    </aside>
  );
}
