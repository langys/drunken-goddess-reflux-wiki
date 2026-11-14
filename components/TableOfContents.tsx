'use client';

import { useEffect, useRef, useState } from 'react';

export type TocItem = {
  id: string;
  text: string;
  level: number;
};

type Props = {
  items: TocItem[];
  title: string;
  collapsible?: boolean;
};

export function TableOfContents({ items, title, collapsible = false }: Props) {
  const [activeId, setActiveId] = useState<string | null>(null);
  const listRef = useRef<HTMLUListElement>(null);

  useEffect(() => {
    const headings = items
      .map((item) => document.getElementById(item.id))
      .filter((heading): heading is HTMLElement => heading !== null);
    let frame = 0;

    const update = () => {
      frame = 0;
      // This line sits just below the fixed header and matches the heading
      // scroll margin. The latest heading above it is the current section.
      const activeLine = headings[0] ? (parseFloat(window.getComputedStyle(headings[0]).scrollMarginTop) || 150) + 20 : 170;
      let current: string | null = headings[0]?.id ?? null;
      for (const heading of headings) {
        if (heading.getBoundingClientRect().top > activeLine) break;
        current = heading.id;
      }
      setActiveId(current);
    };
    const schedule = () => {
      if (!frame) frame = window.requestAnimationFrame(update);
    };

    schedule();
    window.addEventListener('scroll', schedule, { passive: true });
    window.addEventListener('resize', schedule);
    window.addEventListener('hashchange', schedule);
    return () => {
      window.cancelAnimationFrame(frame);
      window.removeEventListener('scroll', schedule);
      window.removeEventListener('resize', schedule);
      window.removeEventListener('hashchange', schedule);
    };
  }, [items]);

  useEffect(() => {
    const list = listRef.current;
    const active = list?.querySelector('a[aria-current="location"]');
    if (!list || !active || !list.getClientRects().length) return;
    const listBox = list.getBoundingClientRect();
    const activeBox = active.getBoundingClientRect();
    if (activeBox.top < listBox.top) list.scrollTop += activeBox.top - listBox.top - 8;
    if (activeBox.bottom > listBox.bottom) list.scrollTop += activeBox.bottom - listBox.bottom + 8;
  }, [activeId]);

  if (!items || items.length < 2) return null;

  const heading = (
      <span className="flex items-center gap-2 text-sm font-semibold text-foreground">
        <svg
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
          className="text-primary"
        >
          <line x1="8" y1="6" x2="21" y2="6" />
          <line x1="8" y1="12" x2="21" y2="12" />
          <line x1="8" y1="18" x2="21" y2="18" />
          <line x1="3" y1="6" x2="3.01" y2="6" />
          <line x1="3" y1="12" x2="3.01" y2="12" />
          <line x1="3" y1="18" x2="3.01" y2="18" />
        </svg>
        <span>{title}</span>
      </span>
  );
  const list = (
      <ul ref={listRef} className="mt-3 space-y-2 text-sm">
        {items.map((item) => (
          <li
            key={item.id}
            className={`${item.level === 3 ? 'ml-3 text-xs' : ''} border-l-2 ${activeId === item.id ? 'border-primary bg-primary/10' : 'border-transparent'}`}
          >
            <a
              href={`#${item.id}`}
              aria-current={activeId === item.id ? 'location' : undefined}
              className={`block rounded-r px-3 py-1 transition hover:text-primary hover:underline underline-offset-4 ${activeId === item.id ? 'font-semibold text-primary' : 'text-muted-foreground'}`}
            >
              {item.text}
            </a>
          </li>
        ))}
      </ul>
  );

  return (
    <nav
      aria-label={title}
      data-toc=""
      className="my-8 rounded-xl border border-border bg-card/60 p-4"
    >
      {collapsible ? (
        <details className="toc-collapse">
          <summary>
            {heading}
            <svg className="toc-collapse-chevron text-muted-foreground" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true"><path d="m6 9 6 6 6-6" /></svg>
          </summary>
          {list}
        </details>
      ) : (
        <>
          <div className="border-b border-border/70 pb-3">{heading}</div>
          {list}
        </>
      )}
    </nav>
  );
}
