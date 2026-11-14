import { siteConfig } from '@/config/site.config';
import { cn } from '@/lib/utils';

/**
 * Official screenshot gallery.
 *
 * Image paths come from site config; official assets are stored locally with
 * their source URLs recorded in docs/local-media-images.json. Every image has
 * a descriptive alt for accessibility and image search.
 */
export function MediaGallery({ className }: { className?: string }) {
  const shots = siteConfig.media.screenshots;
  if (shots.length === 0) return null;

  return (
    <section className={cn('py-10', className)}>
      <h2 className="mb-2 text-2xl font-bold tracking-tight">{siteConfig.name} Screenshots</h2>
      <p className="mb-6 text-sm text-muted-foreground">
        Official screenshots from the store page.
      </p>

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {shots.slice(0, 6).map((shot) => (
          <figure key={shot.url} className="overflow-hidden rounded-xl border border-border bg-card">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={shot.url}
              alt={shot.alt}
              width={600}
              height={337}
              loading="lazy"
              className="aspect-video w-full object-cover transition duration-300 hover:scale-[1.03]"
            />
            {(shot as any).caption && (
              <figcaption className="px-4 py-3 text-sm leading-relaxed text-muted-foreground">
                {(shot as any).caption}
              </figcaption>
            )}
          </figure>
        ))}
      </div>
    </section>
  );
}
