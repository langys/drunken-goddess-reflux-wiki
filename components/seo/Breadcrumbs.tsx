import Link from 'next/link';
import { JsonLd, breadcrumbSchema } from './JsonLd';
import { siteConfig } from '@/config/site.config';

type Crumb = { name: string; url: string };

export function Breadcrumbs({ items, locale }: { items: Crumb[]; locale: string }) {
  const prefix = locale === siteConfig.defaultLocale ? '' : `/${locale}`;
  const localized = items.map((item) => ({ ...item, url: `${prefix}${item.url}` }));

  return (
    <>
      <JsonLd data={breadcrumbSchema(localized, siteConfig.url)} />
      <nav aria-label="Breadcrumb" className="mb-4 text-sm text-muted-foreground">
        <ol className="flex flex-wrap items-center gap-1">
          {localized.map((item, index) => (
            <li key={item.url} className="flex items-center gap-1">
              {index > 0 && <span aria-hidden="true">/</span>}
              {index === localized.length - 1 ? (
                <span className="text-foreground">{item.name}</span>
              ) : (
                <Link href={item.url} className="hover:text-primary">
                  {item.name}
                </Link>
              )}
            </li>
          ))}
        </ol>
      </nav>
    </>
  );
}
