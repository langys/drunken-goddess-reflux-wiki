import { JsonLd } from '@/components/seo/JsonLd';
import { siteConfig } from '@/config/site.config';

const SUBJECT_SCHEMA = {
  VideoGame: 'VideoGame',
  SoftwareApplication: 'SoftwareApplication',
} as const;

/**
 * Home-page entity graph: the site, the organisation behind it, and the thing the
 * site is about. Keying them by @id lets Google merge them into one entity rather
 * than three unrelated nodes.
 */
export function HomeSchema({ locale }: { locale?: string } = {}) {
  const graph = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebSite',
        '@id': `${siteConfig.url}/#website`,
        url: siteConfig.url,
        name: siteConfig.fullName,
        alternateName: [
          siteConfig.name,
          `${siteConfig.name} Wiki`,
          'Pukey Goddess Shot Trick',
          'Pukey Goddess Shot Trick Wiki',
        ],
        description: siteConfig.description,
        inLanguage: siteConfig.defaultLocale,
        publisher: { '@id': `${siteConfig.url}/#organization` },
      },
      {
        '@type': 'Organization',
        '@id': `${siteConfig.url}/#organization`,
        name: siteConfig.fullName,
        url: siteConfig.url,
        logo: {
          '@type': 'ImageObject',
          url: `${siteConfig.url}/android-chrome-512x512.png`,
        },
        sameAs: siteConfig.external.store ? [siteConfig.external.store] : undefined,
      },
      {
        '@type': SUBJECT_SCHEMA[siteConfig.subjectType],
        name: siteConfig.name,
        alternateName: ['Pukey Goddess Shot Trick'],
        url: siteConfig.external.store ?? siteConfig.url,
        applicationCategory: 'Game',
        operatingSystem: siteConfig.operatingSystem,
        publisher: { '@id': `${siteConfig.url}/#organization` },
      },
    ],
  };

  return <JsonLd data={graph} />;
}
