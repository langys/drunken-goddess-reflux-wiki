/**
 * FAQ rendered as plain visible HTML.
 *
 * No FAQPage JSON-LD on purpose: Google only surfaces FAQ rich results for a
 * small set of authoritative sites, so for a new domain the markup adds risk
 * (structured data must match visible content) without adding clicks.
 */
export function FaqSection({
  items,
  heading = 'Frequently Asked Questions',
  className = 'mt-12',
}: {
  items: { q: string; a: string }[];
  heading?: string;
  className?: string;
}) {
  if (!items?.length) return null;

  return (
    <section className={className}>
      <h2 className="mb-5 text-2xl font-bold tracking-tight">{heading}</h2>
      <div className="divide-y divide-border rounded-xl border border-border">
        {items.map((item) => (
          <details key={item.q} className="group px-5 py-4" open>
            <summary className="cursor-pointer list-none font-medium marker:content-['']">
              <span className="flex items-center justify-between gap-4">
                {item.q}
                <span className="text-muted-foreground transition group-open:rotate-45" aria-hidden="true">
                  +
                </span>
              </span>
            </summary>
            <p className="mt-3 text-sm leading-6 text-muted-foreground">{item.a}</p>
          </details>
        ))}
      </div>
    </section>
  );
}
