import { siteConfig } from './site.config';

export type PageEntry = {
  /** Full URL segment under the hub: `<Game-Name>-<intent>` */
  slug: string;
  hub: keyof typeof siteConfig.hubs;
  title: string;
  description: string;
  /** 1 = must ship in the first batch, 2 = second batch, 3 = long tail */
  priority: 1 | 2 | 3;
};

/**
 * The site map. This drives the sitemap, the hub listings and the "what is still
 * missing" check. Keep it in sync with /content/<locale>/*.md — every entry here
 * should have a markdown file, and vice versa.
 */
export const pages: PageEntry[] = [
  // --- Hub: guide ---
  {
    slug: 'drunken-goddess-reflux-beginner-guide',
    hub: 'guide',
    title: 'Beginner Guide: Tips and Russian Roulette Mechanics',
    description: 'Master Drunken Goddess Reflux with beginner tips on shot roulette, intoxication meters, ice pick resets, and surviving Hell\'s Pandemonium bar.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-russian-roulette-mechanics',
    hub: 'guide',
    title: 'Russian Roulette Rules: Proof Odds & Mechanics Explained',
    description: 'Understand shot selection, proof mechanics, turn order, and rule-breaking systems in Drunken Goddess Reflux\'s demon drinking contest.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-intoxication-ice-pick-guide',
    hub: 'guide',
    title: 'Intoxication Meter and Ice Pick Emergency Reset Guide',
    description: 'How to manage intoxication levels, calculate risk thresholds, and use the ice pick mechanic to stay conscious in Drunken Goddess Reflux.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-femme-soule-boss-guide',
    hub: 'guide',
    title: 'Femme Soule Boss Guide: Dialogue, Tells and Counters',
    description: 'Learn Femme Soule\'s drinking patterns, voice line tells by Nanahira, bluff counters, and how to force the demon to vomit her soul.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-pandemonium-bar-secrets',
    hub: 'guide',
    title: 'Pandemonium Bar Secrets and 3D Exploration Guide',
    description: 'Explore the Pandemonium bar in Drunken Goddess Reflux. Uncover hidden lore notes, secret cocktail ingredients, and patron interactions.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-survival-strategies',
    hub: 'guide',
    title: 'Survival Strategies: Advanced Drinking Duel Tactics',
    description: 'Advanced strategies for surviving high-proof rounds, baiting demon moves, managing soul stability, and securing late-game victories.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-drunken-tricks-guide',
    hub: 'guide',
    title: 'Drunken Tricks & Deception Cards Complete Guide',
    description: 'Unlock and execute all drunken tricks and deception cards in Drunken Goddess Reflux, from glass swapping to multiplier bluffing.',
    priority: 1,
  },

  // --- Hub: drinks ---
  {
    slug: 'drunken-goddess-reflux-drink-tier-list',
    hub: 'drinks',
    title: 'Drink Tier List: Best Spirits and Lethal Shots Ranked',
    description: 'Ranked tier list of all drinks and spirits in Drunken Goddess Reflux by proof, tactical utility, debuff severity, and lethality.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-spiritum-lethal-shot-guide',
    hub: 'drinks',
    title: 'Spiritum Shot Guide: Mechanics, Spawn Rate and Counters',
    description: 'Everything about Spiritum in Drunken Goddess Reflux: how this lethal 96% spirit triggers, rules changes, and how to feed it to Femme Soule.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-all-drinks-proof-catalog',
    hub: 'drinks',
    title: 'All Drinks & Proof Catalog: Complete Beverage Database',
    description: 'Complete drink catalog in Drunken Goddess Reflux listing exact alcohol percentages, visual tells, glass markings, and soul gauge damage.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-cocktail-recipes-mixology',
    hub: 'drinks',
    title: 'Secret Cocktail Recipes and Underworld Mixology Guide',
    description: 'Discover secret bar recipes in Pandemonium, special drink concoctions, mixology Easter eggs, and their unique dialogue reactions.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-brimstone-absinthe-guide',
    hub: 'drinks',
    title: 'Brimstone Absinthe Guide: Effects and Hallucinations',
    description: 'Detailed breakdown of Brimstone Absinthe in Drunken Goddess Reflux: hallucination triggers, sensory distortion, and trick synergies.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-holy-water-contraband',
    hub: 'drinks',
    title: 'Holy Water Contraband: How to Find and Use Secret Drink',
    description: 'Locate Holy Water contraband in Drunken Goddess Reflux to stun Femme Soule, purge demonic influence, and invert shot glass roulette.',
    priority: 1,
  },

  // --- Hub: endings ---
  {
    slug: 'drunken-goddess-reflux-all-endings-guide',
    hub: 'endings',
    title: 'All Endings Guide: Unlocking All 7 Flavors of Ruin',
    description: 'Complete guide to unlocking all seven endings in Drunken Goddess Reflux, including choice trees, soul conditions, and achievement flags.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-true-ending-freedom',
    hub: 'endings',
    title: 'True Ending Guide: How to Break Contract & Escape Hell',
    description: 'Step-by-step walkthrough to achieve the True Ending in Drunken Goddess Reflux, reclaiming your mortal soul and escaping Pandemonium alive.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-eternal-partner-ending',
    hub: 'endings',
    title: 'Eternal Drinking Partner Ending Walkthrough (Bound by Love)',
    description: 'How to unlock the Eternal Partner romance ending with Femme Soule in Drunken Goddess Reflux through devoted dialogue and mutual drinking.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-hell-bartender-ending',
    hub: 'endings',
    title: 'Hell Bartender Ending: Taking Over Pandemonium Bar',
    description: 'Detailed walkthrough for the secret Hell Bartender ending in Drunken Goddess Reflux, seizing the shaker and claiming Pandemonium.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-mutual-reflux-secret-ending',
    hub: 'endings',
    title: 'Mutual Reflux Secret Ending Guide: Double Oblivion',
    description: 'Unlock the hidden Mutual Reflux ending in Drunken Goddess Reflux by simultaneously tipping both soul gauges past the breaking point.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-seven-flavors-of-ruin-breakdown',
    hub: 'endings',
    title: 'Seven Flavors of Ruin Explained: Lore and Themes',
    description: 'Deep dive into the narrative and thematic significance of the seven endings in Drunken Goddess Reflux, written by Fuyuki Hayashi.',
    priority: 1,
  },

  // --- Hub: codes ---
  {
    slug: 'drunken-goddess-reflux-codes-and-passwords',
    hub: 'codes',
    title: 'Codes and Secret Bar Passwords (Updated Promo List)',
    description: 'All active promo codes, VIP secret passwords, and redemption methods in Drunken Goddess Reflux for bonus coins and cosmetic glasses.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-steam-achievements-guide',
    hub: 'codes',
    title: 'Steam Achievements Guide: 100% Completion Walkthrough',
    description: 'Full 100% Steam achievements guide for Drunken Goddess Reflux with unlock criteria, hidden trophies, and optimal routing.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-release-date-platforms-specs',
    hub: 'codes',
    title: 'Release Date, Platforms & PC System Requirements',
    description: 'Official release date on Steam (December 8, 2026), PC system requirements, Steam Deck compatibility, and controller support info.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-pc-controls-and-settings',
    hub: 'codes',
    title: 'PC Controls, Keybinds and Interface Settings Guide',
    description: 'Comprehensive guide to keyboard, mouse, and gamepad controls for Drunken Goddess Reflux, including FOV and accessibility toggles.',
    priority: 1,
  },
  {
    slug: 'drunken-goddess-reflux-ost-demons-shot-tracklist',
    hub: 'codes',
    title: "OST & DEMON'S SHOT Theme Song Guide",
    description: 'Official soundtrack details for Drunken Goddess Reflux, featuring theme song DEMON\'S SHOT by Aiobahn +81, DEMONDICE, and Nanahira.',
    priority: 1,
  },
];
