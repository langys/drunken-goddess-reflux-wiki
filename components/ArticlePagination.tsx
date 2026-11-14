import Link from 'next/link';
import type { Guide } from '@/lib/content';

export function ArticlePagination({
  guides, current, hubHref, hubLabel, labels,
}: {
  guides: Guide[];
  current: Guide;
  hubHref: string;
  hubLabel: string;
  labels: { hub: string; previous: string; next: string; articleNavigation: string };
}) {
  const index = guides.findIndex((guide) => guide.slug === current.slug);
  const previous = index > 0 ? guides[index - 1] : null;
  const next = index >= 0 ? guides[index + 1] : null;
  return (
    <nav className="article-pagination" aria-label={labels.articleNavigation} data-pagefind-ignore>
      <Link href={hubHref} className="article-pagination-hub">{labels.hub}: {hubLabel} →</Link>
      <div className="article-pagination-pair">
        {previous ? <Link href={previous.href} className="article-pagination-card">
          <span>{labels.previous}</span><strong>← {previous.title}</strong>
        </Link> : <span />}
        {next ? <Link href={next.href} className="article-pagination-card">
          <span>{labels.next}</span><strong>{next.title} →</strong>
        </Link> : <span />}
      </div>
    </nav>
  );
}
