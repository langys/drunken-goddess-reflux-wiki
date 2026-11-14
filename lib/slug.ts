/**
 * Shared heading id generation.
 *
 * The table of contents, rendered heading anchors and in-page search results must
 * all produce the same fragment, so this lives outside lib/content.ts — which is
 * server-only — and is imported by both the renderer and the client search panel.
 */
export function slugifyHeading(text: string): string {
  return text
    .toLowerCase()
    .replace(/<[^>]*>/g, '')
    .replace(/[^\p{L}\p{N}\s-]/gu, '')
    .trim()
    .replace(/\s+/g, '-');
}
