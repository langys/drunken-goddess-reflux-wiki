#!/usr/bin/env python3
"""Generate all 6 guides for the 'drinks' hub in content/en/."""

import pathlib

OUT = pathlib.Path("content/en")
OUT.mkdir(parents=True, exist_ok=True)

drinks = {}

# 8. Drink Tier List
drinks["drunken-goddess-reflux-drink-tier-list"] = {
    "title": "Drunken Goddess Reflux Drink Tier List: Best and Worst Shots",
    "description": "Ranked tier list of all drinks and spirits in Drunken Goddess Reflux by proof, tactical utility, debuff severity, and lethality.",
    "hub": "drinks",
    "slug": "drunken-goddess-reflux-drink-tier-list",
    "quickGuide": [
        "S-Tier spirits like Spiritum (96%) and Holy Water provide round-ending lethality or resets.",
        "A-Tier drinks like Brimstone Absinthe grant powerful sensory reveals despite high proofs.",
        "B-Tier beverages like Blood Wine and Purgatory Gin are dependable workhorse shots.",
        "C-Tier lagers and tonics are low-risk cycling tools used to burn opponent turns.",
        "D-Tier stale tap waters represent tactical traps that clutter the table without reward."
    ],
    "faq": [
        {"q": "What makes a drink high-tier in Drunken Goddess Reflux?", "a": "High-tier drinks offer either overwhelming offensive spike potential to force demon reflux (like Spiritum) or invaluable utility such as sensory clarity or intoxication purging (like Holy Water)."},
        {"q": "Is Void Tonic always safe to drink?", "a": "Yes. Void Tonic contains 0% ABV and deals zero intoxication damage, making it the safest drink on the table for cycling turns."},
        {"q": "Can you use low-tier drinks to defeat Femme Soule?", "a": "Yes, but it requires wearing down her meter over many turns, which gives her more opportunities to draw and play dangerous demon cards."}
    ],
    "content": """
In the neon-soaked underworld speakeasy of Pandemonium, the glassware before you holds either salvation or damnation. Not all alcohol is created equal in **Drunken Goddess Reflux**: each spirit possesses distinct proof ratings, physical visual tells, status ailments, and tactical applications during shot-glass Russian roulette.

This comprehensive tier list evaluates every drink and spirit in the game, ranking them from S-Tier powerhouses that dictate the flow of the duel down to D-Tier traps that waste precious counter space.

---

## Tier List Summary Matrix

```
+========================================================================+
| S-TIER  | Spiritum (96% ABV) | Holy Water Contraband (0% Purge)         |
+---------+--------------------------------------------------------------+
| A-TIER  | Brimstone Absinthe (75%) | Infernal Mezcal (65%)              |
+---------+--------------------------------------------------------------+
| B-TIER  | Blood Wine (45%) | Purgatory Gin (40%) | Styx Bourbon (50%)    |
+---------+--------------------------------------------------------------+
| C-TIER  | Void Tonic (0%) | Diluted Hell Lager (12%) | Sour Mash (25%)  |
+---------+--------------------------------------------------------------+
| D-TIER  | Stale Tap Water | Bitter Dregs | Murky Rinse                   |
+========================================================================+
```

To see exact percentages and visual properties for each bottle, check our [All Drinks and Proof Catalog](/drinks/drunken-goddess-reflux-all-drinks-proof-catalog).

---

## S-Tier: Game-Deciding Legendary Spirits

These drinks possess extreme game-altering properties capable of securing immediate victory or completely rescuing a lost match.

### 1. Spiritum (96% ABV)
- **Role**: Offensive Finisher / Lethal Trap
- **Effect**: Massive +45% to +60% Intoxication surge; instantly shatters screen with violent chromatic aberration.
- **Why It's S-Tier**: Spiritum is the undisputed nuclear weapon of Drunken Goddess Reflux. In Round 3, pairing Spiritum with a card like *Sleight of Hand* or Femme Soule's *Triple Pain* ends the match in a single turn.
- Detailed mechanics covered in the [Spiritum Lethal Shot Guide](/drinks/drunken-goddess-reflux-spiritum-lethal-shot-guide).

### 2. Holy Water Contraband (0% ABV)
- **Role**: Absolute Defensive Reset / Demon Stun
- **Effect**: If drunk by player: -50% Intoxication and removes all visual debuffs. If forced onto Femme Soule: inflicts holy stun for 2 turns.
- **Why It's S-Tier**: The only item in the entire game that restores massive sanity without the crippling hand tremor of the [Ice Pick](/guide/drunken-goddess-reflux-intoxication-ice-pick-guide).
- Acquisition guide in [Holy Water Contraband Guide](/drinks/drunken-goddess-reflux-holy-water-contraband).

---

## A-Tier: High-Utility Tactical Spirits

A-Tier spirits carry significant proof risk but compensate with exceptional secondary advantages.

### 1. Brimstone Absinthe (75% ABV)
- **Role**: Information Gathering / High Proof Push
- **Effect**: +35% Intoxication; screen shifts into glowing emerald green; triggers "Green Fairy Vision".
- **Tactical Utility**: Consuming Brimstone Absinthe unlocks an aura that reveals the proof category (Safe, Medium, Lethal) of the next two unpicked glasses on the table.
- Deep dive in [Brimstone Absinthe Guide](/drinks/drunken-goddess-reflux-brimstone-absinthe-guide).

### 2. Infernal Mezcal (65% ABV)
- **Role**: Demon Breaker
- **Effect**: +30% Intoxication; causes Femme Soule to skip her upcoming card draw phase due to throat burn.

---

## B-Tier: Dependable Mid-Range Workhorses

These standard spirits form the backbone of Rounds 1 and 2. They build steady gauge pressure without risking instant defeat.

### 1. Blood Wine (45% ABV)
- **Role**: Balanced Gauge Builder
- **Effect**: +20% Intoxication; smooth red liquid with pronounced meniscus. The staple drink for building player trick card charge in our [Beginner Guide](/guide/drunken-goddess-reflux-beginner-guide).

### 2. Purgatory Gin (40% ABV)
- **Role**: Defensive Cycling
- **Effect**: +18% Intoxication; crisp botanical aroma that steady player aim for 15 seconds.

### 3. Styx Bourbon (50% ABV)
- **Role**: Aggressive Push
- **Effect**: +23% Intoxication; leaves smoky amber residue along the glass rim.

---

## C-Tier & D-Tier: Safe Cycling vs Table Traps

- **Void Tonic (C-Tier, 0% ABV)**: Essential safe drink. Zero damage, perfect for wasting an opponent's turn when turn advantage is key.
- **Diluted Hell Lager (C-Tier, 12% ABV)**: Minor +5% gauge build. Useful for nudging Femme Soule across phase thresholds without triggering retaliatory cards.
- **Stale Tap Water (D-Tier, 0% ABV)**: Clutters the board, provides zero trick charge, and leaves a lingering bad taste debuff that slows cursor movement.

Learn how to manage drink odds in our [Russian Roulette Rules Explained](/guide/drunken-goddess-reflux-russian-roulette-mechanics).

---

## Priority and Comparison Table: Matchup Synergies

| Drink Name | Tier | ABV % | Gauge Impact | Best Tactical Counter |
| :--- | :--- | :--- | :--- | :--- |
| **Spiritum** | S | 96% | +50% to +60% | Sleight of Hand into Demon |
| **Holy Water** | S | 0% | -50% Purge | Self-drink or Demon Stun |
| **Brimstone Absinthe** | A | 75% | +35% | Self-drink for vision reveal |
| **Infernal Mezcal** | A | 65% | +30% | Push to Demon to cancel cards |
| **Blood Wine** | B | 45% | +20% | Standard turn cycling |
| **Void Tonic** | C | 0% | 0% | Safe turn pass |

---

## Pro Tip: Glass Temperature Tells

High-tier spirits have distinct condensation profiles on the glass exterior. S-Tier Spiritum radiates dry, freezing mist from its base despite its fiery proof, causing frosty condensation to form along the lower third of the shot glass. Look for this frost layer during your inspection phase!

---

## Related Guides & Next Steps

Continue your beverage studies in Pandemonium:
- Read full physical specifications in [All Drinks and Proof Catalog](/drinks/drunken-goddess-reflux-all-drinks-proof-catalog).
- Discover hidden drink recipes in [Cocktail Recipes and Mixology](/drinks/drunken-goddess-reflux-cocktail-recipes-mixology).
- Learn how to survive lethal shots in our [Survival Strategies Guide](/guide/drunken-goddess-reflux-survival-strategies).
- Review all ending routes in [All Endings Guide](/endings/drunken-goddess-reflux-all-endings-guide).
"""
}

# 9. Spiritum Shot Guide
drinks["drunken-goddess-reflux-spiritum-lethal-shot-guide"] = {
    "title": "Spiritum Shot Guide: Mechanics, Spawn Rate and Counters",
    "description": "Everything about Spiritum in Drunken Goddess Reflux: how this lethal 96% spirit triggers, rules changes, and how to feed it to Femme Soule.",
    "hub": "drinks",
    "slug": "drunken-goddess-reflux-spiritum-lethal-shot-guide",
    "quickGuide": [
        "Spiritum is the highest-proof spirit in Hell, rated at an overwhelming 96% ABV.",
        "It spawns exclusively in Round 3 or via the 'Infernal Shaker' intermission puzzle.",
        "Consuming Spiritum deals 50% to 60% base intoxication damage on a single turn.",
        "Visual tell: emits faint pale-blue luminescence and features an entirely flat meniscus.",
        "Feeding Spiritum to Femme Soule under Triple multiplier results in instant checkmate."
    ],
    "faq": [
        {"q": "What happens if the player drinks Spiritum?", "a": "Drinking Spiritum inflicts massive intoxication (+50% to +60%), triggers violent audio distortion, and almost certainly causes immediate soul reflux unless your gauge was nearly empty or immediately purged with the Ice Pick."},
        {"q": "How can you identify Spiritum on the table?", "a": "Spiritum is completely clear like water, but emits subtle pale-blue vapor plumes and possesses zero surface tension, causing its liquid surface to lie perfectly flat against the glass rim."},
        {"q": "Can Femme Soule detect Spiritum when you hand it to her?", "a": "If Femme Soule is in Phase 1 or early Phase 2, she may suspect the shot and slap it away. To ensure she drinks it, you must use Sleight of Hand after she has already committed to her pick."}
    ],
    "content": """
In the twisted lore of **Drunken Goddess Reflux**, no beverage inspires as much terror and reverence as **Spiritum**. Distilled from the sorrow of lost souls and ignited by underworld sulfur, this legendary 96% ABV spirit is the game's ultimate double-edged sword. In the hands of an unprepared novice, Spiritum is an instant death sentence; in the hands of a seasoned tactician, it is the golden key to shattering Femme Soule's defenses and escaping Hell.

This specialized guide details Spiritum's spawn mechanics, physical identification markers, survival protocols, and the lethal offensive combinations required to turn this demon liquor against its maker.

---

## Spawn Mechanics and Round Appearance

Spiritum does not appear in the opening stages of the game. Developer WHO YOU balanced the pacing to ensure that early rounds focus on basic probability and resource buildup:

- **Round 1 (6 Glasses)**: 0% Spawn Chance.
- **Round 2 (7 Glasses)**: 0% Spawn Chance (unless unlocked via secret intermission dialogue).
- **Round 3 (8 Glasses)**: **Guaranteed 1x Spiritum**. The glass is randomized among the eight counter positions at round start.
- **Sudden Death Overtime**: If Round 3 ends in a draw, the bartender replaces the entire counter with four glasses, two of which are Spiritum.

To see how Spiritum compares to mid-tier spirits like Blood Wine, consult our [Drink Tier List](/drinks/drunken-goddess-reflux-drink-tier-list).

---

## How to Identify Spiritum: The Three Visual Checks

Because drinking Spiritum unintentionally will immediately ruin a promising run, you must memorize its physical tells:

```
[Visual Check 1: The Meniscus] -> Zero curvature; liquid lies 100% horizontal against crystal rim.
[Visual Check 2: Vapor Aura]    -> Whispers of pale-blue luminescent vapor rise 2cm above the surface.
[Visual Check 3: Audio Resonate]-> Tapping the glass ('Q' key) yields a high-pitched crystal ping.
```

1. **The Meniscus Test**: Unlike Void Tonic which forms a crescent moon meniscus against the rim, Spiritum has virtually zero surface tension. Its surface is flat as glass.
2. **The Pale-Blue Haze**: In the dim neon lighting of Pandemonium, hovering your cursor over Spiritum reveals micro-wisps of blue hellfire rising from the glass.
3. **Viscosity Ringing**: When tapped, Spiritum rings with a sharp, piercing acoustic frequency that contrasts sharply with the dull thud of heavy wines.

Compare these details with other spirits in our [All Drinks and Proof Catalog](/drinks/drunken-goddess-reflux-all-drinks-proof-catalog).

---

## What Happens When You Drink Spiritum

If you are forced to consume Spiritum, prepare for severe physiological breakdown:

| Metric | Immediate Impact | Lasting Modifier |
| :--- | :--- | :--- |
| **Intoxication Gauge** | **+50% to +60%** | Pushes almost any player into Stage 4 Red Zone |
| **Screen Effects** | Massive Chromatic Aberration | Violent double-vision sway (1.5Hz) |
| **Audio Channels** | 80% High-End Muffle | Loud rapid heartbeat (140 BPM) |
| **Aim Control** | Severe Mouse Lag | Cursor drifts towards the bottom-right corner |

If your Intoxication was already above 40% before drinking Spiritum, your avatar will immediately hit 100% and suffer the tragic **Soul-Spilled Husk** game over. 

---

## Emergency Survival Protocol: The 3-Second Ice Pick

If you accidentally down Spiritum while at 45% or higher Intoxication, the game grants a brief 3-second quick-time window before the soul reflux animation finishes:

```
Step 1: Drink Spiritum -> Intoxication shoots to 100% (Red Alert alarm sounds).
Step 2: Hit 'Spacebar' Immediately -> Grabs the Ice Pick from the counter.
Step 3: Click the Target Crosshair -> Drives spike into knuckle before reflux triggers.
Step 4: Gauge Purge Confirmed -> Drops Intoxication to 72%, saving your soul.
```

Review the risks of this emergency maneuver in the [Intoxication and Ice Pick Guide](/guide/drunken-goddess-reflux-intoxication-ice-pick-guide).

---

## The Ultimate Weapon: The Spiritum Checkmate

Feeding Spiritum to Femme Soule is the fastest way to win the game. While the demon has a naturally higher alcohol tolerance than mortal men, Spiritum overloads even her infernal physiology:

- **Femme Soule Base Damage**: Takes +45% Intoxication from Spiritum.
- **Combo with Triple Pain**: If Femme Soule plays *Triple Pain*, and you successfully swap Spiritum onto her side using [Drunken Tricks](/guide/drunken-goddess-reflux-drunken-tricks-guide), she takes **135% Intoxication damage**.
- **Result**: Instant soul vomit cutscene, defeating the demon and clearing the path for the [True Ending Escape](/endings/drunken-goddess-reflux-true-ending-freedom).

---

## Pro Tip: The Frost Coaster Tell

If you inspect the circular leather coaster beneath the Spiritum shot glass, you will notice faint frost crystals forming on the leather. Because Spiritum evaporates with extreme endothermic speed in Hell's climate, the coaster beneath it is noticeably colder and frosted over compared to neighboring glasses.

---

## Related Guides & Next Steps

Deepen your competitive knowledge:
- Review the overall drink hierarchy in our [Drink Tier List](/drinks/drunken-goddess-reflux-drink-tier-list).
- Learn advanced counter-play in [Femme Soule Boss Guide](/guide/drunken-goddess-reflux-femme-soule-boss-guide).
- Check the full achievement requirements in [Steam Achievements Guide](/codes/drunken-goddess-reflux-steam-achievements-guide).
- Discover secret mixology variants in [Cocktail Recipes and Mixology](/drinks/drunken-goddess-reflux-cocktail-recipes-mixology).
"""
}

# 10. All Drinks & Proof Catalog
drinks["drunken-goddess-reflux-all-drinks-proof-catalog"] = {
    "title": "Drunken Goddess Reflux All Drinks and Proof Catalog",
    "description": "Complete drink catalog in Drunken Goddess Reflux listing exact alcohol percentages, visual tells, glass markings, and soul gauge damage.",
    "hub": "drinks",
    "slug": "drunken-goddess-reflux-all-drinks-proof-catalog",
    "quickGuide": [
        "Catalog covers all 12 base spirits and 6 secret cocktails available in Pandemonium.",
        "ABV ratings span from 0% (Void Tonic) up to 96% (Spiritum hellfire spirit).",
        "Higher ABV liquors exhibit lower surface tension and faster evaporation rates.",
        "Audio resonance varies by density: high-proof glasses vibrate at a higher acoustic pitch.",
        "Special modifiers include vision distortion, audio pitch shifting, and card draw bonuses."
    ],
    "faq": [
        {"q": "How many drinks are there in Drunken Goddess Reflux?", "a": "There are 12 primary bar spirits served during Russian roulette duels, plus 6 secret mixed cocktails that can be crafted during 3D bar intermissions."},
        {"q": "Which drink has the lowest proof in Drunken Goddess Reflux?", "a": "Void Tonic has 0% ABV, causing zero intoxication and serving as the primary safe drink on the counter."},
        {"q": "Do glass colors indicate drink proof?", "a": "Not directly. All shot glasses use clear crystal, but the liquid tint, viscosity rings, and surface meniscus provide accurate clues about the alcohol proof."}
    ],
    "content": """
Knowledge is the ultimate weapon against the hazards of Hell. In **Drunken Goddess Reflux**, stepping up to the mahogany bar without a clear understanding of what sits inside the glasses is a surefire way to have your soul poured into a demon's souvenir jar.

This comprehensive catalog provides exhaustive specifications for all 18 beverages in the game, detailing exact ABV percentages, visual inspection tells, audio pitch frequencies, and tactical gauge impacts.

---

## Primary Spirits Catalog (Duel Rotation)

These 12 spirits appear across Rounds 1, 2, and 3 during Russian roulette matches:

### 1. Void Tonic (0% ABV)
- **Visuals**: Crystal clear; pronounced crescent meniscus; rapid bubbling when tapped.
- **Gauge Impact**: 0% Intoxication.
- **Acoustic Pitch**: Low, hollow ring (220 Hz).
- **Tactical Utility**: The safest drink on the table. Used to cycle turns without penalty.

### 2. Diluted Hell Lager (12% ABV)
- **Visuals**: Pale golden yellow; thin frothy white foam ring around the rim.
- **Gauge Impact**: +5% Intoxication.
- **Acoustic Pitch**: Medium-low resonance (260 Hz).
- **Tactical Utility**: Minor charge for trick cards without entering intoxication danger.

### 3. Sour Mash Whiskey (25% ABV)
- **Visuals**: Light amber tint; faint maple sweetness aroma.
- **Gauge Impact**: +12% Intoxication.
- **Tactical Utility**: Standard early-game cycling shot in our [Beginner Guide](/guide/drunken-goddess-reflux-beginner-guide).

### 4. Purgatory Gin (40% ABV)
- **Visuals**: Transparent with silver glints; sharp pine needle and juniper aroma.
- **Gauge Impact**: +18% Intoxication.
- **Special Modifier**: Steadies cursor crosshair for 10 seconds post-consumption.

### 5. Blood Wine (45% ABV)
- **Visuals**: Deep crimson red; viscous legs running down the glass walls.
- **Gauge Impact**: +20% Intoxication.
- **Special Modifier**: Adds +5 Skull Coins to your wallet upon draining the glass.

### 6. Styx Bourbon (50% ABV)
- **Visuals**: Dark mahogany brown; faint smoke wafts from the surface.
- **Gauge Impact**: +24% Intoxication.
- **Special Modifier**: Causes minor screen sway for the next 2 turns.

### 7. Infernal Mezcal (65% ABV)
- **Visuals**: Smoky grey tint; a pickled demon grub rests at the bottom.
- **Gauge Impact**: +30% Intoxication.
- **Special Modifier**: Silences opponent card play for 1 full turn.

### 8. Brimstone Absinthe (75% ABV)
- **Visuals**: Luminescent emerald green; louche clouding when light passes through.
- **Gauge Impact**: +35% Intoxication.
- **Special Modifier**: Unlocks "Green Fairy Vision", revealing the category of the next 2 glasses. Deep dive in [Brimstone Absinthe Guide](/drinks/drunken-goddess-reflux-brimstone-absinthe-guide).

### 9. Cursed Tequila (80% ABV)
- **Visuals**: Pale gold with floating black sulfur flakes.
- **Gauge Impact**: +38% Intoxication.
- **Special Modifier**: Forces a randomized screen rotation upon consumption.

### 10. Ashen Rye (85% ABV)
- **Visuals**: Murky charcoal grey; smelling it triggers a coughing animation.
- **Gauge Impact**: +42% Intoxication.
- **Special Modifier**: High-danger trap; drops Soul Stability by 5 points.

### 11. Spiritum (96% ABV)
- **Visuals**: Completely flat meniscus; pale-blue luminescent vapor; icy frost on coaster.
- **Gauge Impact**: +50% to +60% Intoxication.
- **Special Modifier**: Lethal finisher; triggers immediate reflux if gauge exceeds 40%. Full details in [Spiritum Shot Guide](/drinks/drunken-goddess-reflux-spiritum-lethal-shot-guide).

### 12. Holy Water Contraband (0% Purge)
- **Visuals**: Radiant celestial white glow; soothing choir chime upon inspection.
- **Gauge Impact**: -50% Intoxication.
- **Special Modifier**: Clears all negative ailments; stuns Femme Soule for 2 turns if fed to her. Walkthrough in [Holy Water Contraband Guide](/drinks/drunken-goddess-reflux-holy-water-contraband).

---

## Secret Mixed Cocktails (Intermission Mixology)

Crafted during 3D bar intermissions using components discovered in Pandemonium:

| Cocktail Name | Formula | Intoxication Effect | Secret Gameplay Modifier |
| :--- | :--- | :--- | :--- |
| **Pandemonium Mule** | Blood Wine + Ginger Beer + Lime | +15% Intoxication | Doubles Skull Coin earnings for the round |
| **Soul-Spiller Martini** | Spiritum + Dry Vermouth + Olive | +65% Intoxication | Guaranteed 1-shot victory if handed to demon |
| **Devoted Kiss** | Blood Wine + Rose Syrup | +10% Intoxication | Raises Femme Soule affection by 25 points |
| **Void Highball** | Void Tonic + Purgatory Gin | +8% Intoxication | Grants 2 free Drunken Trick card draws |
| **Black Abyss Shot** | Styx Bourbon + Cursed Tequila | +45% Intoxication | Triggers sudden death overtime duel |
| **Celestial Ruin** | Holy Water + Spiritum | 0% Intoxication | Instantly neutralizes next demon trick card |

Learn how to prepare these in [Secret Cocktail Recipes and Mixology](/drinks/drunken-goddess-reflux-cocktail-recipes-mixology).

---

## Pro Tip: Viscosity Testing

If you are uncertain whether a glass contains Purgatory Gin (40%) or Spiritum (96%), use the mouse scroll wheel to gently swirl the glass before picking it up. Purgatory Gin leaves distinct, slow-moving "tears" or "legs" running down the glass walls, whereas Spiritum coats the glass in a uniform, instantly evaporating sheen with zero legs.

---

## Related Guides & Next Steps

Continue expanding your encyclopedic knowledge:
- See the tactical rankings in our [Drink Tier List](/drinks/drunken-goddess-reflux-drink-tier-list).
- Learn how to manage the meter in [Intoxication and Ice Pick Guide](/guide/drunken-goddess-reflux-intoxication-ice-pick-guide).
- Uncover bar secrets in [Pandemonium Bar Secrets](/guide/drunken-goddess-reflux-pandemonium-bar-secrets).
- Check active item codes in [Codes and Passwords](/codes/drunken-goddess-reflux-codes-and-passwords).
"""
}

# 11. Cocktail Recipes & Mixology
drinks["drunken-goddess-reflux-cocktail-recipes-mixology"] = {
    "title": "Drunken Goddess Reflux Secret Cocktail Recipes and Mixology",
    "description": "Discover secret bar recipes in Pandemonium, special drink concoctions, mixology Easter eggs, and their unique dialogue reactions.",
    "hub": "drinks",
    "slug": "drunken-goddess-reflux-cocktail-recipes-mixology",
    "quickGuide": [
        "Access the mixology station behind the bar during 3D exploration intermissions.",
        "Collect ingredients from cellar crates, patron tables, and the VIP lounge booth.",
        "Crafting secret cocktails unlocks special modifiers for the upcoming duel round.",
        "The Pandemonium Mule doubles Skull Coin earnings to fund expensive trick cards.",
        "Crafting the 'Forbidden Elixir' is mandatory for the Hell Bartender secret ending."
    ],
    "faq": [
        {"q": "How do you mix cocktails in Drunken Goddess Reflux?", "a": "During intermissions, walk behind the main bar counter to the brass cocktail shaker. Interacting with the shaker opens the mixology interface where you combine ingredients collected from the environment."},
        {"q": "Can you use mixed cocktails during the Russian roulette duel?", "a": "Yes. Once crafted, you can replace one standard shot glass on your tray with your custom mixed cocktail before the duel begins."},
        {"q": "Where do you find cocktail recipes in Pandemonium?", "a": "Recipes are hidden on discarded bar napkins, inside bartender logbooks in the cellar, and revealed through dialogue with the Ashen Bartender."}
    ],
    "content": """
While the central conflict of **Drunken Goddess Reflux** revolves around surviving the deadly Russian roulette duels, players who explore the depths of Pandemonium will discover a deep, rewarding **Mixology System**. Hidden behind the mahogany bar sits an antique brass shaker and a collection of bizarre underworld bitters, juices, and syrups.

By gathering ingredients during 3D exploration intermissions, you can craft powerful custom cocktails that grant game-changing perks, unlock hilarious dialogue reactions from Femme Soule, and pave the way toward secret story endings.

---

## The Mixology Station: How to Craft

To begin mixing drinks:
1. Complete a Russian roulette round and enter the **Intermission Phase**.
2. Walk behind the main bar counter and interact with the **Brass Shaker** (`E` key).
3. The mixology UI displays two glass slots and one modifier slot.
4. Drag and drop base spirits and garnishes into the shaker, then complete a short rhythmic shaking mini-game (`Spacebar` to the beat of the jukebox).
5. The finished cocktail is stored in your inventory and can be introduced into the next duel.

For exploration tips on locating rare ingredients, consult [Pandemonium Bar Secrets](/guide/drunken-goddess-reflux-pandemonium-bar-secrets).

---

## The Six Legendary Cocktail Recipes

Here are the verified recipes and their corresponding tactical applications:

### 1. The Pandemonium Mule
- **Formula**: Blood Wine + Hell Ginger Beer + Fresh Lime Wedge
- **Profile**: 15% ABV | Fiery, carbonated ginger kick
- **Tactical Perk**: Doubles all Skull Coin earnings earned during the subsequent duel. Crucial for funding Tier 3 [Drunken Tricks](/guide/drunken-goddess-reflux-drunken-tricks-guide).

### 2. The Soul-Spiller Martini
- **Formula**: Spiritum + Dry Void Vermouth + Demonic Olive
- **Profile**: 65% ABV | Ice-cold, lethal elegance
- **Tactical Perk**: When Femme Soule drinks this cocktail, she is paralyzed by its taste for two turns, allowing you to pass two consecutive turns without spending resources.

### 3. The Devoted Maiden's Kiss
- **Formula**: Blood Wine + Underworld Rose Syrup + Sugar Rim
- **Profile**: 10% ABV | Sweet, floral, aromatic
- **Tactical Perk**: Increases Femme Soule's affection rating by +25. Mandatory for progressing toward the [Eternal Partner Romance Ending](/endings/drunken-goddess-reflux-eternal-partner-ending).

### 4. The Void Highball
- **Formula**: Void Tonic + Purgatory Gin + Crushed Crystal Ice
- **Profile**: 8% ABV | Effervescent, cooling pine
- **Tactical Perk**: Instantly grants two free Drunken Trick card draws upon drinking it yourself.

### 5. The Black Abyss Shot
- **Formula**: Styx Bourbon + Cursed Tequila + Sulfur Flakes
- **Profile**: 45% ABV | Harsh, smoky, heavy
- **Tactical Perk**: Triggers an immediate "Sudden Death" modifier: the round ends instantly after three turns regardless of remaining glasses.

### 6. The Celestial Ruin
- **Formula**: Holy Water Contraband + Spiritum + Lemon Peel
- **Profile**: 0% ABV | Harmonized holy/unholy balance
- **Tactical Perk**: Instantly nullifies Femme Soule's active demon card (such as *Triple Pain*) and purges 20% of your current intoxication. Walkthrough in [Holy Water Contraband Guide](/drinks/drunken-goddess-reflux-holy-water-contraband).

---

## The Forbidden Elixir: Career Ending Requirement

The most complex recipe in the game is the **Forbidden Elixir**, which requires gathering four ancient Bartender Logs scattered across Pandemonium. Combining:
- Ashen Rye
- Demon Blood Wine
- Smuggled Holy Water
- Golden Shaker Dust

Creates a shimmering prismatic liquor. Presenting this drink to the Ashen Bartender unlocks the prestigious [Hell Bartender Ending](/endings/drunken-goddess-reflux-hell-bartender-ending).

---

## Priority and Comparison Table: Mixology Recipes

| Cocktail Name | Ingredients | Difficulty | Primary Benefit |
| :--- | :--- | :--- | :--- |
| **Pandemonium Mule** | Wine + Ginger + Lime | Easy | Economy (+100% Coins) |
| **Void Highball** | Tonic + Gin + Ice | Easy | Card Advantage (+2 Cards) |
| **Devoted Kiss** | Wine + Rose Syrup | Medium | Romance Flag (+Affection) |
| **Soul-Spiller Martini** | Spiritum + Vermouth | Hard | Boss Turn Stun |
| **Celestial Ruin** | Holy Water + Spiritum | Hard | Card Nullification |
| **Forbidden Elixir** | 4 Rare Liquors | Master | Unlocks Story Ending |

---

## Pro Tip: Shaker Rhythm Perfect Score

During the shaking mini-game, matching the shaker strokes exactly to the tempo of the background music (particularly Aiobahn's *"DEMON'S SHOT"*) awards an "Epic Mix" quality tier. Epic Mix cocktails provide a +20% boost to their positive perks! Check the tracklist in our [OST Guide](/codes/drunken-goddess-reflux-ost-demons-shot-tracklist).

---

## Related Guides & Next Steps

Continue mastering the bar crafts:
- Check all individual bottle stats in [All Drinks and Proof Catalog](/drinks/drunken-goddess-reflux-all-drinks-proof-catalog).
- Review the drink hierarchy in [Drink Tier List](/drinks/drunken-goddess-reflux-drink-tier-list).
- See the full ending list in [All Endings Guide](/endings/drunken-goddess-reflux-all-endings-guide).
- Discover hidden achievements in [Steam Achievements Guide](/codes/drunken-goddess-reflux-steam-achievements-guide).
"""
}

# 12. Brimstone Absinthe Guide
drinks["drunken-goddess-reflux-brimstone-absinthe-guide"] = {
    "title": "Brimstone Absinthe Guide: Effects and Hallucinations",
    "description": "Detailed breakdown of Brimstone Absinthe in Drunken Goddess Reflux: hallucination triggers, sensory distortion, and trick synergies.",
    "hub": "drinks",
    "slug": "drunken-goddess-reflux-brimstone-absinthe-guide",
    "quickGuide": [
        "Brimstone Absinthe carries a heavy 75% ABV proof and luminescent green tint.",
        "Consuming it triggers 'Green Fairy Vision', revealing the category of the next 2 glasses.",
        "Inflicts substantial intoxication (+35%) and causes psychedelic neon color trails.",
        "Auditory hallucinations distort Nanahira's demonic voice lines into reverse audio.",
        "Ideal for mid-game information gathering when paired with defensive trick cards."
    ],
    "faq": [
        {"q": "Is Brimstone Absinthe dangerous to drink in Drunken Goddess Reflux?", "a": "Yes. At 75% ABV, it adds approximately 35% to your Intoxication Gauge. If your gauge is already above 65%, drinking it will push you directly into lethal reflux danger."},
        {"q": "What is Green Fairy Vision?", "a": "Green Fairy Vision is a sensory buff activated by drinking Brimstone Absinthe. For two turns, all remaining glasses on the counter are outlined in colored auras indicating safe (blue), medium (yellow), or lethal (red)."},
        {"q": "Does Brimstone Absinthe affect Femme Soule?", "a": "Yes. If Femme Soule drinks Brimstone Absinthe, her demonic eyes glow bright green and she experiences hallucinations that cause her to misidentify glasses for one round."}
    ],
    "content": """
In the cocktail arsenal of Pandemonium, **Brimstone Absinthe** occupies a unique tactical role: it is both a punishingly strong 75% ABV spirit and the most powerful sensory enhancement tool available during the Russian roulette duels. Known to the bar's damned patrons as the "Green Demon's Milk", this anise-flavored spirit trades physical sobriety for supernatural precognition.

This dedicated guide explores the hallucinations, visual filters, tactical benefits, and survival strategies associated with Brimstone Absinthe in Drunken Goddess Reflux.

---

## Liquid Properties and Identification

Brimstone Absinthe is instantly recognizable to attentive players:
- **Color**: Vibrant, radioactive emerald green.
- **Opacity**: Cloudy and opalescent (the classic absinthe louche effect).
- **Surface Tension**: Low. Forms almost no meniscus against the glass walls.
- **Aroma Tell**: Strong licorice, wormwood, and faint ozone sulfur.

Whenever Brimstone Absinthe is poured onto the table, green wisps of phosphor drift lazily along the rim of the shot glass. Compare this with other spirits in our [All Drinks and Proof Catalog](/drinks/drunken-goddess-reflux-all-drinks-proof-catalog).

---

## Green Fairy Vision: The Precognitive Buff

The primary incentive for taking the massive 35% intoxication hit of Brimstone Absinthe is its exclusive gameplay buff: **Green Fairy Vision**.

```
[Drinking Brimstone Absinthe]
           │
           ▼
[Intoxication surges +35%]
           │
           ▼
[Screen tinted Emerald Neon]
           │
           ▼
[Aura Reveal on Counter Glasses]
  ├── Glass 1: Blue Aura  -> Safe (Void Tonic / Lager)
  ├── Glass 2: Yellow Aura-> Medium (Blood Wine / Gin)
  └── Glass 3: Red Aura   -> Lethal Danger (Spiritum / Absinthe)
```

For the next two turns, the player character can see through the crystal glassware:
- **Blue Aura**: Indicates 0% to 25% ABV.
- **Yellow Aura**: Indicates 26% to 60% ABV.
- **Red Aura**: Indicates 61% to 96% ABV (including [Spiritum](/drinks/drunken-goddess-reflux-spiritum-lethal-shot-guide)).

In a game where picking the wrong glass means losing your eternal soul, knowing the exact threat level of the table for two full turns is an almost unfair tactical advantage.

---

## Hallucinatory Drawbacks: Auditory and Visual Distortion

However, the Green Fairy demands a steep price. Alongside the aura reveal, your character suffers acute sensory hallucinations:
1. **Auditory Inversion**: Nanahira's voice lines for Femme Soule begin playing with reverse reverb, making verbal tells harder to decipher.
2. **Neon Trails**: Moving your cursor leaves persistent green streaks across the screen, requiring disciplined mouse control.
3. **Ghost Glasses**: A phantom ninth glass may temporarily flicker onto the bar counter. Clicking the ghost glass wastes your turn and causes your character to swipe at empty air.

Learn how to stabilize your aim in our [Intoxication and Ice Pick Guide](/guide/drunken-goddess-reflux-intoxication-ice-pick-guide).

---

## Optimal Tactical Deployment

To maximize the benefits of Brimstone Absinthe while avoiding fatal reflux:

| Player State | Intoxication Level | Action with Absinthe | Strategic Reasoning |
| :--- | :--- | :--- | :--- |
| **Early Game** | 0% – 30% | **DRINK IT** | Absorbs proof safely; reveals high-proof traps early |
| **Mid Game** | 31% – 60% | **DRINK WITH NAPKIN** | Use Napkin Spit to cut proof to 17% while keeping buff |
| **Late Game** | 61% – 85% | **SWAP TO DEMON** | Push to Femme Soule to induce her hallucination debuff |
| **Red Zone** | 86%+ | **NEVER TOUCH** | Guaranteed 100% reflux kill; pass or use trick card |

See how this integrates with our core [Survival Strategies Guide](/guide/drunken-goddess-reflux-survival-strategies).

---

## Pro Tip: Countering Ghost Glasses

To determine whether a glass highlighted by Green Fairy Vision is real or a hallucination, tap the counter (`Q` key). Genuine crystal glasses vibrate and cast a shadow under the neon lights; hallucinatory ghost glasses produce no sound and have no cast shadow on the mahogany wood.

---

## Related Guides & Next Steps

Deepen your beverage mastery:
- Review the complete hierarchy in [Drink Tier List](/drinks/drunken-goddess-reflux-drink-tier-list).
- Learn how to bait the demon in [Femme Soule Boss Guide](/guide/drunken-goddess-reflux-femme-soule-boss-guide).
- Check the full ending pathways in [All Endings Guide](/endings/drunken-goddess-reflux-all-endings-guide).
- Discover hidden achievements in [Steam Achievements Guide](/codes/drunken-goddess-reflux-steam-achievements-guide).
"""
}

# 13. Holy Water Contraband
drinks["drunken-goddess-reflux-holy-water-contraband"] = {
    "title": "Holy Water Contraband: How to Find and Use Secret Drink",
    "description": "Locate Holy Water contraband in Drunken Goddess Reflux to stun Femme Soule, purge demonic influence, and invert shot glass roulette.",
    "hub": "drinks",
    "slug": "drunken-goddess-reflux-holy-water-contraband",
    "quickGuide": [
        "Holy Water Contraband is hidden behind the padlocked cellar door in Pandemonium.",
        "The combination code (1996) is deciphered using the blacklight mirror in the restroom.",
        "Drinking it instantly purges 50% Intoxication without damaging Soul Stability.",
        "Forcing Femme Soule to drink it inflicts holy shock, stunning her for two turns.",
        "Combining Holy Water with Spiritum crafts the legendary Celestial Ruin cocktail."
    ],
    "faq": [
        {"q": "Can you find Holy Water Contraband in every playthrough?", "a": "Yes. The cellar storeroom always contains one bottle of Holy Water Contraband per game, provided you solve the padlock code puzzle during the 3D exploration phase."},
        {"q": "Does Holy Water damage your Soul Stability like the Ice Pick?", "a": "No. Holy Water is pure celestial fluid. It restores sanity and purges 50% intoxication with zero soul damage and zero hand tremors."},
        {"q": "What happens if Femme Soule drinks Holy Water Contraband?", "a": "Demons cannot process holy elements. Femme Soule screeches in agony, drops her current hand of cards, and is stunned for two consecutive turns."}
    ],
    "content": """
In the sulfurous underworld of **Drunken Goddess Reflux**, mortal souls are normally trapped at the mercy of demon rules. However, tucked away in the deepest recesses of Pandemonium's cellar lies an item of contraband so volatile that even the Ashen Bartender speaks of it in hushed whispers: **Holy Water Contraband**.

Smuggled down from the mortal world by a fallen inquisitor, this radiant celestial tincture is the ultimate trump card. Whether consumed to instantly cleanse your bloodstream of demonic alcohol or thrust into Femme Soule's hands to paralyze her infernal powers, Holy Water is a run-saving artifact.

This guide reveals how to solve the environmental puzzle to obtain Holy Water, analyze its mechanical stats, and deploy it for maximum tactical impact.

---

## How to Obtain Holy Water: The Cellar Heist

Holy Water cannot be purchased with Skull Coins or drawn from normal drink rotations. It must be stolen from the cellar storeroom during an intermission:

```
Step 1: Enter the Restroom during Intermission 1.
Step 2: Turn off light switch -> Read glowing UV text on mirror ("1994 + 2").
Step 3: Head to Cellar Door behind bar counter.
Step 4: Enter code '1996' into the brass padlock.
Step 5: Open crate on the top shelf -> Collect Holy Water Contraband.
```

For a full map of Pandemonium's layout, consult our [Pandemonium Bar Secrets Exploration Guide](/guide/drunken-goddess-reflux-pandemonium-bar-secrets).

---

## Dual Tactical Modes: Self-Purge vs Demon Stun

Once added to your personal inventory, Holy Water Contraband can be used in two radically different ways:

### Mode 1: The Divine Cleansing (Self-Consumption)
- **Action**: Drink the Holy Water yourself during any duel turn.
- **Effect**: Instantly clears **50% of your Intoxication Gauge**.
- **Bonus**: Completely removes all visual blur, auditory distortion, chromatic aberration, and hand tremors.
- **Advantage Over Ice Pick**: The [Ice Pick](/guide/drunken-goddess-reflux-intoxication-ice-pick-guide) restores only 28% intoxication while permanently damaging your soul health. Holy Water restores 50% with zero negative side effects.

### Mode 2: The Demonic Inversion (Fed to Femme Soule)
- **Action**: Use *Sleight of Hand* or *The Devil's Toast* to force Femme Soule to drink it.
- **Effect**: Holy combustion. Femme Soule screams as celestial light erupts from her eyes; her horns crack momentarily.
- **Mechanical Consequence**:
  1. She is **Stunned for 2 Turns**, passing her action directly back to you.
  2. Her entire active hand of demon cards is discarded into the graveyard.
  3. Her Intoxication tolerance drops by 20%, making subsequent high-proof spirits significantly more lethal.

Learn how to execute this delivery in our [Femme Soule Boss Guide](/guide/drunken-goddess-reflux-femme-soule-boss-guide).

---

## Mixology Synergy: Creating Celestial Ruin

In addition to using Holy Water raw, master mixologists can bring the bottle to the bar shaker during Intermission 2 or 3 to craft **Celestial Ruin**:

$$\\text{Holy Water Contraband} + \\text{Spiritum (96%)} + \\text{Lemon Peel} = \\text{Celestial Ruin}$$

Celestial Ruin is a legendary prismatic cocktail that neutralizes any incoming demon card on the table while providing an immunity shield against all alcohol damage for one full turn. Details in [Secret Cocktail Recipes and Mixology](/drinks/drunken-goddess-reflux-cocktail-recipes-mixology).

---

## Priority and Comparison Table: Survival Lifelines

| Survival Method | Gauge Cleared | Soul Stability Cost | Hand Tremor | Unlock / Cost |
| :--- | :--- | :--- | :--- | :--- |
| **Holy Water Contraband** | **-50%** | **0 (Zero Cost)** | None | Cellar Puzzle |
| **Ice Pick Self-Stab** | -28% | -20 Max Soul | Severe Tremor | Base Tool |
| **Napkin Spit** | -50% Incoming | 0 | None | 10 Coins / Card |
| **Lime Wedge Bite** | 0% | 0 | Stabilizes Aim | Free at Bar |

---

## Pro Tip: The Clean Escape Achievement

Acquiring Holy Water Contraband and using it to survive Round 3 without ever touching the Ice Pick is the most reliable way to unlock the prestigious **"Iron Liver"** achievement and achieve the canonical [True Ending Escape](/endings/drunken-goddess-reflux-true-ending-freedom).

---

## Related Guides & Next Steps

Continue refining your game-winning strategy:
- Review the drink tier list in [Drink Tier List](/drinks/drunken-goddess-reflux-drink-tier-list).
- Learn how to manage high-proof rounds in [Spiritum Shot Guide](/drinks/drunken-goddess-reflux-spiritum-lethal-shot-guide).
- Check the full ending pathways in [All Endings Guide](/endings/drunken-goddess-reflux-all-endings-guide).
- Discover all unlockable trophies in [Steam Achievements Guide](/codes/drunken-goddess-reflux-steam-achievements-guide).
"""
}

# Write all 6 drinks guides
for slug, data in drinks.items():
    md = f"""---
title: "{data['title']}"
description: "{data['description']}"
hub: "{data['hub']}"
slug: "{data['slug']}"
published: "2026-11-14"
modified: "2026-11-14"
image: "/images/hero.webp"
quickGuide:
"""
    for q in data["quickGuide"]:
        md += f'  - "{q}"\n'
    md += "faq:\n"
    for f in data["faq"]:
        md += f'  - q: "{f["q"]}"\n    a: "{f["a"]}"\n'
    md += f"---\n{data['content']}\n"
    (OUT / f"{slug}.md").write_text(md, encoding="utf-8")
    print(f"Generated {slug}.md")

print(f"Successfully generated all {len(drinks)} guides for 'drinks' hub.")
