/**
 * Renders a JSON-LD block. Google reads these to understand what the page is;
 * using @graph on the home page ties the site, the organisation and the game
 * into one entity graph instead of three unrelated blobs.
 */
export function JsonLd({ data }: { data: Record<string, unknown> }) {
  return (
    <script
      type="application/ld+json"
      // JSON.stringify output is safe here: no user input is interpolated into
      // the graph, only values from config and page frontmatter.
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}

type Crumb = { name: string; url: string };

export function breadcrumbSchema(items: Crumb[], siteUrl: string) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: `${siteUrl}${item.url}`,
    })),
  };
}
