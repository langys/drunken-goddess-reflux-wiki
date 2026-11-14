import { highlightSegments } from '@/lib/search';

/** Renders highlighted search text without injecting HTML. */
export function HighlightedText({ text, tokens }: { text: string; tokens: string[] }) {
  return (
    <>
      {highlightSegments(text, tokens).map((segment, index) =>
        segment.match ? (
          <mark key={index} className="rounded-sm bg-primary/25 px-0.5 text-foreground">
            {segment.text}
          </mark>
        ) : (
          <span key={index}>{segment.text}</span>
        ),
      )}
    </>
  );
}
