import Link from 'next/link';
import { useTranslations } from 'next-intl';
import { cn } from '@/lib/utils';

/**
 * Shared header for a homepage module.
 *
 * Every module uses the same three parts — title, one-line scope, and an optional
 * link to the full section — so the page can be scanned top to bottom without
 * relearning each block. `href` is omitted for modules that have no destination
 * (latest updates, official media); do not invent a "view all" that goes nowhere.
 */
export function HomeModuleHeader({
  title,
  description,
  href,
  browseLabel,
  className,
}: {
  title: string;
  description?: string;
  href?: string;
  browseLabel?: string;
  className?: string;
}) {
  const t = useTranslations('home');
  const actionLabel = browseLabel ?? t('moduleBrowse');
  return (
    <div className={cn('home-module-header', className)}>
      <div className="min-w-0">
        <h2 className="text-2xl font-bold tracking-tight">{title}</h2>
        {description && <p className="mt-1 max-w-2xl text-sm text-muted-foreground">{description}</p>}
      </div>
      {href && (
        <Link href={href} aria-label={`${actionLabel}: ${title}`} className="home-module-all">
          {actionLabel}
          <span aria-hidden="true">→</span>
        </Link>
      )}
    </div>
  );
}
