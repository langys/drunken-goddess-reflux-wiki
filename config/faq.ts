import type { Guide } from '@/lib/content';

/**
 * Shared FAQ block for the home page. Keep answers factual and point readers at
 * official sources for anything that changes (release status, price, codes) —
 * that way the page stays accurate without daily edits.
 */
export const homeFaq: { q: string; a: string }[] = [
  {
    q: 'What is Drunken Goddess Reflux?',
    a: "Drunken Goddess Reflux is a psychological drinking survival game styled around shot-glass Russian roulette. Set in Hell's Pandemonium bar, you face off against the devoted demon Femme Soule where the loser must spill their soul.",
  },
  {
    q: 'Is Drunken Goddess Reflux the same as PUKEY GODDESS SHOT TRICK?',
    a: 'Yes. Drunken Goddess Reflux was originally announced and is officially known in Japan as PUKEY GODDESS SHOT TRICK (醉娘回流, often abbreviated DGR). Both titles refer to the exact same game developed by WHO YOU (Fuyuki Hayashi) and published by Alliance Arts (Steam App ID: 4150720).',
  },
  {
    q: 'When is the Drunken Goddess Reflux release date and price?',
    a: 'Drunken Goddess Reflux is scheduled to release on PC via Steam on December 8, 2026. The expected price point is $9.99 – $14.99 USD (¥1,200 – ¥1,800 JPY), developed by WHO YOU and published by Alliance Arts.',
  },
  {
    q: 'Who is the demon bartender character in Drunken Goddess Reflux?',
    a: 'The demoness you face across the mahogany counter is named Femme Soule (also referred to as Fam Sour), designed by artist odyk and voiced by Japanese voice actress Nanahira.',
  },
  {
    q: 'How does the shot-glass Russian roulette mechanic work?',
    a: 'You and Femme Soule take turns choosing and drinking from an array of unlabelled shot glasses with varying alcohol proof. As intoxication builds, rules break down and players unlock wild drunken deception tricks.',
  },
  {
    q: 'Is Drunken Goddess Reflux an NSFW / R18 game or does it have extreme gore?',
    a: 'No. While the game features suggestive dark romance, alcohol themes, and dramatic soul-expulsion (reflux) animations when intoxication exceeds 100%, it is a stylized psychological indie game on Steam, not an R18 adult or gore title.',
  },
  {
    q: 'Who composed the theme song for Drunken Goddess Reflux / PUKEY GODDESS SHOT TRICK?',
    a: "The viral title theme song 'DEMON'S SHOT' was composed and arranged by Japanese electronic artist Aiobahn +81, with lead rap vocals by DEMONDICE and character voice backing by Nanahira.",
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
