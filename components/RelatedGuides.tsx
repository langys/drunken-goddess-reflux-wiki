import Link from 'next/link';
import { useTranslations } from 'next-intl';
import type { Guide } from '@/lib/content';
import { GuideThumb, guideImage } from '@/components/Hero';

/**
 * Related guides from the same silo. Three links is deliberate: enough to spread
 * link equity across the hub, few enough that each one is a real recommendation.
 * Site-wide random interlinking dilutes relevance and reads as spam.
 */
export function RelatedGuides({ guides, locale }: { guides: Guide[]; locale: string }) {
  const t = useTranslations('reading');
  if (guides.length === 0) return null;

  return (
    <section className="mt-12 border-t border-border pt-8">
      <h2 className="mb-4 text-xl font-bold">{t('related')}</h2>
      <div className="grid gap-4 sm:grid-cols-3">
        {guides.map((guide) => (
          <Link
            key={guide.slug}
            href={guide.href}
            className="group overflow-hidden rounded-xl border border-border transition hover:border-primary/60 hover:bg-muted/50"
          >
            <GuideThumb src={guideImage(guide.image, guide.slug)} alt={guide.title} />
            <div className="p-4">
              <p className="font-medium leading-snug group-hover:text-primary">{guide.title}</p>
              {guide.excerpt && (
                <p className="mt-2 line-clamp-3 text-sm text-muted-foreground">{guide.excerpt}</p>
              )}
            </div>
          </Link>
        ))}
      </div>
    </section>
  );
}
