import { notFound } from 'next/navigation';
import { getLegalPage } from '@/lib/legal';
import { formatDate } from '@/lib/utils';

/** Shared renderer for about / contact / privacy / terms. */
export async function LegalPageView({ slug, locale }: { slug: string; locale: string }) {
  const page = await getLegalPage(slug, locale);
  if (!page) notFound();

  return (
    <article className="mx-auto max-w-3xl">
      <h1 className="text-3xl font-extrabold tracking-tight sm:text-4xl">{page.title}</h1>
      {page.updated && (
        <p className="mt-3 text-xs text-muted-foreground">Last updated {formatDate(page.updated, locale)}</p>
      )}
      <div className="article-body mt-8" dangerouslySetInnerHTML={{ __html: page.html }} />
    </article>
  );
}
