/**
 * The 5-second skim block. Everything important on the page is compressed into
 * five one-line bullets placed before the prose — this is what search snippets
 * and AI answers quote, and it decides whether a visitor stays.
 */

/**
 * Splits a bullet into its lead phrase and explanation.
 *
 * Accepts both the ASCII colon and the full-width `：` that CJK translators
 * naturally reach for. Splitting on ASCII alone silently failed for every
 * Japanese bullet — the whole line rendered unbolded, so the skim block lost the
 * exact structure that makes it scannable. Wide colons are also accepted without
 * a following space, which is correct Japanese typography.
 */
function splitBullet(item: string): [string, string] {
  const match = item.match(/^([^:：]+)[:：]\s*([\s\S]*)$/);
  if (!match) return [item.trim(), ''];
  return [match[1].trim(), match[2].trim()];
}

export function QuickGuide({ items, heading = 'Quick Guide' }: { items: string[]; heading?: string }) {
  if (!items?.length) return null;

  return (
    <section className="my-8 rounded-xl border border-primary/25 bg-primary/5 p-5">
      <h2 className="mb-3 text-base font-bold uppercase tracking-wide text-primary">{heading}</h2>
      <ul className="space-y-2">
        {items.map((item) => {
          const [lead, rest] = splitBullet(item);
          return (
            <li key={item} className="text-sm leading-6">
              <strong className="font-semibold text-foreground">{lead}</strong>
              {rest && <span>: {rest}</span>}
            </li>
          );
        })}
      </ul>
    </section>
  );
}
