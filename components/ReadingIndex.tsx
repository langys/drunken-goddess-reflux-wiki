'use client';

import Link from 'next/link';

export type IndexGroup = {
  label: string;
  href: string;
  active?: boolean;
  guides: { title: string; href: string }[];
};

export function ReadingIndex({ groups, title, currentHref }: { groups: IndexGroup[]; title: string; currentHref: string }) {
  return (
    <nav className="reading-index" aria-label={title} data-pagefind-ignore>
      <p className="reading-rail-title">{title}</p>
      <div className="reading-index-scroll">
        {groups.map((group) => (
          <details key={group.href} className="reading-index-group" open={group.active}>
            <summary>
              <span aria-hidden="true" className="reading-index-chevron">▸</span>
              <Link href={group.href} className="category-title-link" onClick={(event) => event.stopPropagation()}>
                {group.label}
              </Link>
              <span className="reading-index-count">{group.guides.length}</span>
            </summary>
            <ul>
              {group.guides.map((guide) => (
                <li key={guide.href}><Link href={guide.href} aria-current={guide.href === currentHref ? 'page' : undefined}>{guide.title}</Link></li>
              ))}
            </ul>
          </details>
        ))}
      </div>
    </nav>
  );
}
