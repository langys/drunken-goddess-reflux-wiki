import { JsonLd } from './JsonLd';
import { siteConfig } from '@/config/site.config';

type Props = {
  title: string;
  description: string;
  path: string;
  published: string;
  modified?: string;
  image?: string;
};

/** Article schema for every spoke page (guide / codes / tier list / release ...). */
export function ArticleSchema({ title, description, path, published, modified, image }: Props) {
  return (
    <JsonLd
      data={{
        '@context': 'https://schema.org',
        '@type': 'Article',
        headline: title,
        description,
        image: `${siteConfig.url}${image ?? siteConfig.heroImage}`,
        datePublished: published,
        dateModified: modified ?? published,
        author: { '@type': 'Organization', name: `${siteConfig.fullName} Team` },
        publisher: {
          '@type': 'Organization',
          name: siteConfig.fullName,
          logo: {
            '@type': 'ImageObject',
            url: `${siteConfig.url}/android-chrome-512x512.png`,
          },
        },
        mainEntityOfPage: { '@type': 'WebPage', '@id': `${siteConfig.url}${path}` },
      }}
    />
  );
}
