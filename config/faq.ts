import type { Guide } from '@/lib/content';

/**
 * Shared FAQ block for the home page. Keep answers factual and point readers at
 * official sources for anything that changes (release status, price, codes) —
 * that way the page stays accurate without daily edits.
 */
export const homeFaq: { q: string; a: string }[] = [
  {
    q: 'What is Drunken Goddess Reflux?',
    a: 'Drunken Goddess Reflux is a psychological drinking survival game styled around shot-glass Russian roulette. Set in Hell\'s Pandemonium bar, you face off against the devoted demon Femme Soule where the loser must spill their soul.',
  },
  {
    q: 'When is the Drunken Goddess Reflux release date?',
    a: "Drunken Goddess Reflux is scheduled to release on PC via Steam on December 8, 2026, developed by WHO YOU (Fuyuki Hayashi) and published by Alliance Arts.",
  },
  {
    q: 'How does the shot-glass Russian roulette mechanic work?',
    a: 'You and Femme Soule take turns choosing and drinking from an array of unlabelled shot glasses with varying alcohol proof. As intoxication builds, rules break down and players unlock wild drunken deception tricks.',
  },
  {
    q: 'How many endings does Drunken Goddess Reflux have?',
    a: 'The game features seven distinct endings, referred to as seven flavors of ruin, ranging from outdrinking the demon to win your soul back, to becoming eternal barfly partners or hell cocktail ingredients.',
  },
  {
    q: 'Is there a demo for Drunken Goddess Reflux?',
    a: 'Alliance Arts previously planned a public demo for October 2026, but cancelled the public release to protect game assets from scraping, opting instead for closed playtests in their official community.',
  },
];

export function latestUpdates(guides: Guide[], limit = 6): Guide[] {
  return [...guides]
    .sort((a, b) => (a.published < b.published ? 1 : -1))
    .slice(0, limit);
}
