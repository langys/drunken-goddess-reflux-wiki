import { cn } from '@/lib/utils';

type Variant = 'info' | 'warning' | 'success' | 'tip';

const VARIANT_CLASS: Record<Variant, string> = {
  info: 'border-[hsl(var(--callout-info-border))] bg-[hsl(var(--callout-info-bg))] text-[hsl(var(--callout-info-text))]',
  warning: 'border-[hsl(var(--callout-warning-border))] bg-[hsl(var(--callout-warning-bg))] text-[hsl(var(--callout-warning-text))]',
  success: 'border-[hsl(var(--callout-success-border))] bg-[hsl(var(--callout-success-bg))] text-[hsl(var(--callout-success-text))]',
  tip: 'border-[hsl(var(--callout-tip-border))] bg-[hsl(var(--callout-tip-bg))] text-[hsl(var(--callout-tip-text))]',
};

const LABEL: Record<Variant, string> = {
  info: 'Note',
  warning: 'Caution',
  success: 'Confirmed',
  tip: 'Pro Tip',
};

/** Callout for provenance and warnings. Use it to mark uncertain information
 *  explicitly instead of stating a guess as fact. */
export function Callout({
  variant = 'tip',
  title,
  children,
}: {
  variant?: Variant;
  title?: string;
  children: React.ReactNode;
}) {
  return (
    <aside className={cn('my-6 rounded-xl border px-5 py-4 text-sm leading-6', VARIANT_CLASS[variant])}>
      <p className="mb-1 font-semibold">{title ?? LABEL[variant]}</p>
      <div>{children}</div>
    </aside>
  );
}

/** Three conclusion cards. Each one is a standalone takeaway, not a paragraph. */
export function CardGrid({ cards }: { cards: { title: string; body: string }[] }) {
  if (!cards?.length) return null;

  return (
    <div className="my-8 grid gap-4 sm:grid-cols-3">
      {cards.map((card) => (
        <div key={card.title} className="rounded-xl border border-border bg-card p-5">
          <p className="mb-2 font-semibold text-foreground">{card.title}</p>
          <p className="text-sm leading-6 text-muted-foreground">{card.body}</p>
        </div>
      ))}
    </div>
  );
}
