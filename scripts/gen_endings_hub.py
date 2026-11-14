#!/usr/bin/env python3
"""Generate all 6 guides for the 'endings' hub in content/en/."""

import pathlib

OUT = pathlib.Path("content/en")
OUT.mkdir(parents=True, exist_ok=True)

endings = {}

# 14. All Endings Guide
endings["drunken-goddess-reflux-all-endings-guide"] = {
    "title": "Drunken Goddess Reflux All Endings Guide (7 Flavors)",
    "description": "Complete guide to unlocking all seven endings in Drunken Goddess Reflux, including choice trees, soul conditions, and achievement flags.",
    "hub": "endings",
    "slug": "drunken-goddess-reflux-all-endings-guide",
    "quickGuide": [
        "The narrative branches into 7 distinct endings known as the 'Seven Flavors of Ruin'.",
        "Ending 1 (Reclaimed Dawn) is the sole canonical victory where you escape Hell alive.",
        "Endings 2 through 4 represent tragic or romantic loss conditions with Femme Soule.",
        "Ending 5 (The New Bartender) is a secret career branch unlocked via intermission mixology.",
        "Ending 6 (Void Blackout) and Ending 7 (Bottled Essence) stem from complete soul depletion."
    ],
    "faq": [
        {"q": "How many endings are in Drunken Goddess Reflux?", "a": "There are exactly seven endings, described by director Fuyuki Hayashi as the 'Seven Flavors of Ruin'. Only one ending results in your mortal escape, while the others explore various forms of eternal damnation."},
        {"q": "Does getting a loss ending delete your save file?", "a": "No. When an ending is reached, the game records the achievement and ending card in your gallery, allowing you to instantly start a new run with unlocked shortcut tokens."},
        {"q": "Which ending is the hardest to unlock in Drunken Goddess Reflux?", "a": "The secret 'Mutual Reflux' ending is the hardest, requiring both the player and Femme Soule to reach exactly 100% Intoxication on the very same turn."}
    ],
    "content": """
The tagline of **Drunken Goddess Reflux** promises players the chance to *"Survive the night, and savor seven flavors of ruin."* True to director Fuyuki Hayashi's signature dark, psychological writing style, the narrative is not a simple binary win-or-lose affair. Depending on your drinking choices, dialogue responses to Femme Soule, exploration discoveries, and how your mortal soul is expelled, the story splinters into **seven distinct endings**.

This master guide provides a full overview of all seven endings, including their narrative themes, mechanical prerequisites, key decision points, and associated Steam achievements.

---

## The Seven Flavors of Ruin: Overview Matrix

```
+========================================================================================+
| ENDING | TITLE                  | ROUTE TYPE       | CORE CONDITION                     |
+--------+------------------------+------------------+------------------------------------+
| 1      | Reclaimed Dawn         | True Victory     | Outdrink Femme Soule + Zero Reflux |
| 2      | Eternal Pour           | Romance / Bad    | High Affection + Drink with Demon  |
| 3      | Soul-Spilled Husk      | Standard Bad     | Player Reflux in Round 1 or 2      |
| 4      | Mutual Reflux          | Secret Comic/Bad | Both reach 100% Intoxication same turn|
| 5      | New Hell Bartender     | Secret Career    | Mix Forbidden Elixir + 4 Logs      |
| 6      | Void Blackout          | Tragedy Bad      | Soul Stability drops to 0 via Ice Pick|
| 7      | Demon's Cocktail       | Dark Horror      | Consume Cursed Mezcal at 95%+ meter|
+========================================================================================+
```

---

## Ending 1: Reclaimed Dawn (The True Escape)
- **The Outcome**: You force Femme Soule to vomit her demonic soul in Round 3. As she collapses across the bar counter weeping and smiling in defeat, the iron elevator behind the jukebox unlocks, carrying your mortal body back up to the morning streets of the living world.
- **Key Requirements**:
  - Keep your Soul Stability above 20%.
  - Feed Femme Soule high-proof spirits like [Spiritum](/drinks/drunken-goddess-reflux-spiritum-lethal-shot-guide).
  - Select defiant dialogue choices during all intermissions.
- **Achievement Unlocked**: *"Morning Sunlight"* (Gold).
- Step-by-step walkthrough in [True Ending Freedom Walkthrough](/endings/drunken-goddess-reflux-true-ending-freedom).

---

## Ending 2: Eternal Pour (Bound by Devotion)
- **The Outcome**: Rather than fighting Femme Soule, you embrace her obsessive declarations. You share a final celebratory toast, permanently giving up your mortal life to sit beside her at Pandemonium for eternity as her cherished drinking companion.
- **Key Requirements**:
  - Maximize her affection rating (>80) through flirty dialogue choices.
  - Mix and gift her the [Devoted Maiden's Kiss Cocktail](/drinks/drunken-goddess-reflux-cocktail-recipes-mixology).
  - Refuse the elevator escape prompt when offered at the end of Round 3.
- **Achievement Unlocked**: *"Till Death Do Us Part"* (Silver).
- Detailed guide in [Eternal Drinking Partner Ending](/endings/drunken-goddess-reflux-eternal-partner-ending).

---

## Ending 3: Soul-Spilled Husk (Standard Loss)
- **The Outcome**: Your mortal body cannot endure the demonic alcohol. You hit 100% Intoxication during Round 1 or 2, disgorging your glowing blue human soul across the table. Femme Soule affectionately scoops up the puddle of ectoplasm, placing it in an antique glass jar on her bedside table.
- **Key Requirements**: Reach 100% Intoxication before Femme Soule.
- **Achievement Unlocked**: *"A Light Drinker"* (Bronze).

---

## Ending 4: Mutual Reflux (Double Oblivion)
- **The Outcome**: The ultimate dark-comedy ending. Both you and Femme Soule down high-proof shots simultaneously, hitting 100% Intoxication on the exact same frame. Both characters erupt into simultaneous soul reflux, sending both of your spirits careening into an astral limbo where you spend eternity arguing over who won.
- **Key Requirements**:
  - Set both gauges to 75%+ in Round 3.
  - Play the *Tied Souls* trick card followed by a double Spiritum toast.
- **Achievement Unlocked**: *"Soul Twins"* (Gold).
- Secret guide in [Mutual Reflux Secret Ending](/endings/drunken-goddess-reflux-mutual-reflux-secret-ending).

---

## Ending 5: The Master of Pandemonium (New Hell Bartender)
- **The Outcome**: Disillusioned with mortal life and unimpressed by demon royalty, you uncover the ancient secrets of the bar. You craft the Forbidden Elixir, impress the Ashen Bartender, don the crimson vest, and become the supreme barkeep of Hell, with Femme Soule as your eternal regular patron.
- **Key Requirements**:
  - Discover all 4 Bartender Logs in the cellar.
  - Craft the Forbidden Elixir at the mixology station.
  - Present the cocktail during Intermission 3.
- **Achievement Unlocked**: *"Under New Management"* (Gold).
- Full walkthrough in [Hell Bartender Ending](/endings/drunken-goddess-reflux-hell-bartender-ending).

---

## Endings 6 & 7: The Grim Fates
- **Ending 6 (Void Blackout)**: Caused by overusing the [Ice Pick](/guide/drunken-goddess-reflux-intoxication-ice-pick-guide). Three consecutive knuckle stabs deplete your Soul Stability to zero. You bleed out in your chair before the duel can conclude. Achievement: *"Blunt Instrument"*.
- **Ending 7 (Demon's Cocktail)**: Drinking Infernal Mezcal while your Intoxication is above 95% dissolves your avatar from within. The Ashen Bartender sweeps your ashes into an empty decanter to serve future patrons. Achievement: *"House Special"*.

Read the full philosophical breakdown in [Seven Flavors of Ruin Explained](/endings/drunken-goddess-reflux-seven-flavors-of-ruin-breakdown).

---

## Pro Tip: Minimal Playthrough Route for 100% Endings

To collect all seven ending cards in just three playthroughs:
1. **Playthrough 1**: Defiant run aiming for the [True Ending Escape](/endings/drunken-goddess-reflux-true-ending-freedom) while using zero ice picks.
2. **Playthrough 2**: Flirty exploration run aiming for [Eternal Partner](/endings/drunken-goddess-reflux-eternal-partner-ending), branching into [Hell Bartender](/endings/drunken-goddess-reflux-hell-bartender-ending) by keeping a backup save before Intermission 3.
3. **Playthrough 3**: High-risk trick run targeting [Mutual Reflux](/endings/drunken-goddess-reflux-mutual-reflux-secret-ending) and the two quick bad endings.

---

## Related Guides & Next Steps

Explore the individual ending walkthroughs:
- Step-by-step escape guide: [True Ending Freedom Walkthrough](/endings/drunken-goddess-reflux-true-ending-freedom).
- Romance route guide: [Eternal Partner Romance Ending](/endings/drunken-goddess-reflux-eternal-partner-ending).
- Secret bar route: [Hell Bartender Secret Ending](/endings/drunken-goddess-reflux-hell-bartender-ending).
- Trophy completionist guide: [Steam Achievements Guide](/codes/drunken-goddess-reflux-steam-achievements-guide).
"""
}

# 15. True Ending Freedom
endings["drunken-goddess-reflux-true-ending-freedom"] = {
    "title": "How to Get True Ending in Drunken Goddess Reflux: Escape Hell",
    "description": "Step-by-step walkthrough to achieve the True Ending in Drunken Goddess Reflux, reclaiming your mortal soul and escaping Pandemonium alive.",
    "hub": "endings",
    "slug": "drunken-goddess-reflux-true-ending-freedom",
    "quickGuide": [
        "Defeat Femme Soule in Round 3 by forcing her Intoxication past 100% without vomiting.",
        "Never use the Ice Pick more than once; zero uses is required for pristine rank.",
        "Select strictly defiant and resistant dialogue options during all bar conversations.",
        "Smuggle Holy Water Contraband from the cellar to safely purge emergency intoxication.",
        "Take the elevator behind the neon jukebox to trigger the morning dawn cutscene."
    ],
    "faq": [
        {"q": "What is the True Ending called in Drunken Goddess Reflux?", "a": "The True Ending is titled 'Reclaimed Dawn' (Ending 1). It is the only canonical narrative branch where your mortal character successfully leaves Pandemonium alive."},
        {"q": "Can you get the True Ending if you used the Ice Pick?", "a": "Yes, but you can only use it at most once. Using the Ice Pick two or more times permanently degrades your soul stability, locking you out of the pristine elevator escape cutscene."},
        {"q": "What does Femme Soule say when you win?", "a": "Femme Soule collapses with a tearful, affectionate smile, whispering through her drunken stupor: 'No one's ever done this to me before... Ahh, you're incredible, darling. Go... before I change my mind.'"}
    ],
    "content": """
In **Drunken Goddess Reflux**, your soul is on the line. While six of the game's endings plunge you deeper into the intoxicating damnation of Hell, **Ending 1: Reclaimed Dawn** is the hard-fought canonical victory. Achieving it proves you have mastered the mathematics of shot-glass Russian roulette, resisted Femme Soule's seductive manipulations, and preserved your mortal sanity.

This comprehensive walkthrough details every dialogue choice, drink strategy, resource requirement, and final encounter protocol necessary to reclaim your soul and walk out of Pandemonium into the morning sun.

---

## True Ending Prerequisites Checklist

Before launching your True Ending attempt, ensure you understand the mandatory constraints:

```
[Prerequisite 1]: Zero or One Ice Pick Use (Zero uses required for pristine 'Iron Liver' rank).
[Prerequisite 2]: Defiant Dialogue Flags (Never agree to stay or flatter the demon).
[Prerequisite 3]: Soul Stability >= 50% upon reaching Round 3.
[Prerequisite 4]: Acquire Holy Water Contraband during Intermission 1.
[Prerequisite 5]: Successfully feed Spiritum (96%) to Femme Soule in Round 3.
```

Review our foundational tactics in the [Beginner Guide](/guide/drunken-goddess-reflux-beginner-guide) and [Survival Strategies Guide](/guide/drunken-goddess-reflux-survival-strategies).

---

## Intermission 1: Setting the Defiant Flags

When you awaken at the counter and survive Round 1, Femme Soule initiates her first dialogue exchange. To stay on the Reclaimed Dawn path:

1. **Dialogue Prompt 1**: Femme asks what brought you to Hell.
   - **Correct Pick**: *"An accident. And I'm leaving the second this bottle is empty."* (Defiant Flag +1)
   - *Avoid*: Any flirtatious responses about liking her horns or staying for a drink.
2. **Exploration Task**: Head straight to the restroom, turn off the light, note the mirror clue (`1994 + 2`), and unlock the cellar door with code `1996` to collect the [Holy Water Contraband](/drinks/drunken-goddess-reflux-holy-water-contraband). Having Holy Water guarantees you can survive Round 2 without touching the Ice Pick.

Full cellar puzzle walkthrough in [Pandemonium Bar Secrets](/guide/drunken-goddess-reflux-pandemonium-bar-secrets).

---

## Round 2 Execution: Preserving Soul Stability

Round 2 introduces 70%+ proof spirits like Brimstone Absinthe. To maintain pristine soul health:
- Cycle early turns with low-proof [Void Tonic](/drinks/drunken-goddess-reflux-all-drinks-proof-catalog) or Blood Wine.
- If forced into a dangerous 75% absinthe shot, consume your **Holy Water Contraband** to instantly wipe away 50% intoxication.
- End Round 2 by baiting Femme Soule into drinking Infernal Mezcal, bringing her gauge to ~60% entering the final duel.

---

## Intermission 2: The Final Rejection

Femme Soule waits for you near the VIP booth. She appears slightly unsteady, her horns glowing faintly violet:
- **Dialogue Prompt 2**: Femme asks if you feel the warmth of eternity calling to you.
- **Correct Pick**: *"I feel a headache, demon. Nothing more."* (Defiant Flag +2)
- She pouts, her eyes narrowing in fierce determination. This locks in her aggressive Phase 3 AI, which is required for the final checkmate maneuver.

Study her combat phases in the [Femme Soule Boss Guide](/guide/drunken-goddess-reflux-femme-soule-boss-guide).

---

## Round 3: The Spiritum Checkmate

Round 3 is the climax. The Ashen Bartender places 8 glasses on the table, including the lethal 96% **Spiritum**.

```
Step 1: Inspect glasses -> Identify Spiritum (flat meniscus + pale-blue vapor).
Step 2: Conserve Trick Card -> Hold one 'Sleight of Hand' or 'Mirror Swap'.
Step 3: Wait for Demon Aggression -> Femme Soule will activate her 'Triple Pain' card.
Step 4: Execute Swap -> Swap her chosen glass with Spiritum.
Step 5: Checkmate -> Femme Soule drinks 96% x 3. Her Intoxication hits 288%!
```

Femme Soule gasps in shock. Demonic purple ectoplasm erupts from her lips as she undergoes violent soul reflux. The match ends with your gauge safely below 80%!

Review the full mechanics of the lethal shot in the [Spiritum Shot Guide](/drinks/drunken-goddess-reflux-spiritum-lethal-shot-guide).

---

## The Escape Cutscene: Reclaimed Dawn

With Femme Soule slumped across the counter, the ambient lights in Pandemonium flicker off. Behind the jukebox, the heavy iron elevator gates slide open with a metallic groan:
1. Walk past the bar counter to the elevator.
2. Step inside and pull the brass floor lever.
3. The elevator ascends through darkness while DEMONDICE's closing vocal ballad plays.
4. The doors open onto a rain-slicked city alleyway at sunrise. Your character inhales fresh morning air, checking their watch. You are alive, human, and free.

Unlocks the prestigious **"Morning Sunlight"** Steam achievement! See all achievements in [Steam Achievements Guide](/codes/drunken-goddess-reflux-steam-achievements-guide).

---

## Pro Tip: The Clean Hand Trophy

If you complete this entire walkthrough without using the Ice Pick even once, you earn both the "Morning Sunlight" True Ending trophy and the elusive "Iron Liver" achievement simultaneously, shaving hours off your platinum completion time!

---

## Related Guides & Next Steps

Explore alternate narrative branches:
- Review all endings in [All Endings Guide (7 Flavors of Ruin)](/endings/drunken-goddess-reflux-all-endings-guide).
- See the romance alternative in [Eternal Partner Romance Ending](/endings/drunken-goddess-reflux-eternal-partner-ending).
- Learn how to become the barkeep in [Hell Bartender Ending](/endings/drunken-goddess-reflux-hell-bartender-ending).
- Check active codes and rewards in [Codes and Passwords](/codes/drunken-goddess-reflux-codes-and-passwords).
"""
}

# 16. Eternal Partner Ending
endings["drunken-goddess-reflux-eternal-partner-ending"] = {
    "title": "Eternal Drinking Partner Ending Walkthrough (Bound by Love)",
    "description": "How to unlock the Eternal Partner romance ending with Femme Soule in Drunken Goddess Reflux through devoted dialogue and mutual drinking.",
    "hub": "endings",
    "slug": "drunken-goddess-reflux-eternal-partner-ending",
    "quickGuide": [
        "Select strictly affectionate and flirty dialogue choices across all intermissions.",
        "Craft and gift the 'Devoted Maiden's Kiss' cocktail during Intermission 2.",
        "Raise Femme Soule's Affection Gauge above 85 before the end of Round 3.",
        "Refuse the elevator escape prompt when offered after defeating her in the duel.",
        "Take a seat beside her on the bar stool to initiate the eternal romance cutscene."
    ],
    "faq": [
        {"q": "Is the Eternal Partner ending considered a good ending?", "a": "It is a dark-romance ending. While your mortal life on Earth is forfeited, Femme Soule treats you as her beloved eternal companion rather than a damned victim, creating a bittersweet happily-ever-after in Hell."},
        {"q": "What happens if you drink the Devoted Maiden's Kiss yourself?", "a": "Drinking it yourself grants only a minor intoxication boost (+10%). You must hand it to Femme Soule during intermission to earn the crucial +25 Affection bonus."},
        {"q": "Does Nanahira sing during the Eternal Partner ending?", "a": "Yes! The ending credits feature an exclusive acoustic vocal ballad performed by voice actress Nanahira, lamenting eternal love in the underworld."}
    ],
    "content": """
Not every soul who tumbles into Pandemonium wants to return to the cold, mundane mortal world. For players captivated by the chaotic charm and possessive devotion of **Femme Soule**, **Ending 2: Eternal Pour (Bound by Devotion)** offers a seductive alternative to escaping Hell. Character designer odyk and writer Fuyuki Hayashi crafted this romance route as a darkly comedic tribute to yandere devotion, where losing your mortal life is a small price to pay for eternity with a demon who loves you enough to kill you.

This complete walkthrough details how to build Femme Soule's affection, craft her favorite drink, navigate the crucial dialogue trees, and seal your eternal drinking partnership.

---

## Affection Mechanics: Building the Demon's Favor

Femme Soule possesses an internal **Affection Gauge (0 to 100)** hidden during gameplay. Reaching **85+ Affection** before the conclusion of Round 3 is mandatory to trigger the romance finale:

```
[Starting Affection: 10]
        │
        ├── Intermission 1 Flirtatious Choice: +20 Affection
        ├── Gift 'Devoted Maiden's Kiss':     +25 Affection
        ├── Intermission 2 Devoted Response:   +20 Affection
        └── In-Duel Complimentary Toasts:      +15 Affection
        │
        ▼
[Final Affection: 90 / 100] -> Romance Route Unlocked!
```

---

## Step 1: Flirting Through Intermission 1

After completing Round 1, do not rush to the cellar or restroom. Instead, walk directly to the **VIP Booth** where Femme Soule is curled up on the red velvet sofa:
1. Speak with her. She playfully asks if mortal souls always tremble this much.
2. **Select Response**: *"I'm only trembling because you're stunning under these neon lights."*
3. Femme Soule's eyes flash crimson with flustered delight (+20 Affection). She offers you a special VIP coaster that grants 10 free Skull Coins.

Review the VIP booth layout in our [Pandemonium Bar Secrets Guide](/guide/drunken-goddess-reflux-pandemonium-bar-secrets).

---

## Step 2: Crafting The Devoted Maiden's Kiss

During Intermission 2, head behind the bar to the brass cocktail shaker. You must craft her favorite cocktail:
- **Base Spirit**: [Blood Wine (45%)](/drinks/drunken-goddess-reflux-all-drinks-proof-catalog) (found in the wine rack).
- **Sweetener**: Underworld Rose Syrup (collected from the bar counter garnish tray).
- **Garnish**: Sugar Rim.

Shake the ingredients and return to Femme Soule in the lounge. Hand her the cocktail (`E` key prompt). She sips it delicately, blushing as she murmurs: *"Sweet... like a promise we haven't made yet."* (+25 Affection).

Full recipe details in [Secret Cocktail Recipes and Mixology](/drinks/drunken-goddess-reflux-cocktail-recipes-mixology).

---

## Step 3: Complimentary Toasts in Round 3

During the climactic third round, utilize your [Drunken Tricks](/guide/drunken-goddess-reflux-drunken-tricks-guide) defensively. Rather than playing aggressive force-drink cards, activate *The Gentle Toast*. Whenever you raise a glass to drink, your character nods respectfully to Femme Soule. Her vocal lines delivered by Nanahira become noticeably softer and more affectionate.

Defeat her by letting her drink high-proof liquor naturally until she hits 100% Intoxication and collapses.

Study her reactions in the [Femme Soule Boss Guide](/guide/drunken-goddess-reflux-femme-soule-boss-guide).

---

## The Decision at the Elevator: Staying in Hell

Once Femme Soule collapses and the iron elevator opens behind the jukebox, the critical decision appears:
1. Walk toward the open elevator doors.
2. The game prompts: *"Step inside and return to the living world?"*
3. **Choose: [NO - Turn Back]**.
4. Walk back to the counter and sit on the bar stool directly beside the slumped demoness.
5. Interact with her hand. Your character gently shakes her awake.

---

## The Romance Cutscene: Till Death Do Us Part

Femme Soule blinks awake, tears of drunken joy streaming down her cheeks:
> *"You stayed...? For me? Ahh... darling, you really are the most foolish, incredible creature in the cosmos."*

She slides a matching glass of Blood Wine across the counter. You clink glasses under the warm neon glow. The camera slowly pans out through the smoke of Pandemonium as the credits roll to an acoustic ballad sung by Nanahira.

Unlocks the **"Till Death Do Us Part"** Steam achievement! Full trophy roadmap in [Steam Achievements Guide](/codes/drunken-goddess-reflux-steam-achievements-guide).

---

## Pro Tip: Unlocking the Secret Jukebox Track

Achieving this ending permanently unlocks Track 13 on the Pandemonium Jukebox: *"Femme's Lullaby (Acoustic)"*. Listen to it anytime on subsequent playthroughs! Check details in [OST and DEMON'S SHOT Guide](/codes/drunken-goddess-reflux-ost-demons-shot-tracklist).

---

## Related Guides & Next Steps

Compare with other narrative endings:
- Escape back to mortal life: [True Ending Freedom Walkthrough](/endings/drunken-goddess-reflux-true-ending-freedom).
- Take over the establishment: [Hell Bartender Ending](/endings/drunken-goddess-reflux-hell-bartender-ending).
- Master the cocktail crafts: [Cocktail Recipes and Mixology](/drinks/drunken-goddess-reflux-cocktail-recipes-mixology).
- See the full ending list: [All Endings Guide](/endings/drunken-goddess-reflux-all-endings-guide).
"""
}

# 17. Hell Bartender Ending
endings["drunken-goddess-reflux-hell-bartender-ending"] = {
    "title": "Hell Bartender Ending: Taking Over Pandemonium Bar",
    "description": "Detailed walkthrough for the secret Hell Bartender ending in Drunken Goddess Reflux, seizing the shaker and claiming Pandemonium.",
    "hub": "endings",
    "slug": "drunken-goddess-reflux-hell-bartender-ending",
    "quickGuide": [
        "Uncover all 4 hidden Bartender Logbooks hidden across Pandemonium's zones.",
        "Craft the legendary 'Forbidden Elixir' during Intermission 3 using rare spirits.",
        "Present the elixir to the Ashen Bartender before sitting down for the final duel.",
        "Win Round 3 by draining the final glass yourself to prove bartending mastery.",
        "Receive the Crimson Vest and antique shaker to become Hell's new bar owner."
    ],
    "faq": [
        {"q": "What is the Hell Bartender ending in Drunken Goddess Reflux?", "a": "Ending 5: The Master of Pandemonium is a secret career ending where the player rejects both mortal escape and demon romance, choosing instead to succeed the Ashen Bartender as the new owner and mixologist of Hell's tavern."},
        {"q": "Where are the four Bartender Logbooks located?", "a": "The logbooks are found in: 1) Behind the cellar wine rack, 2) Inside the jukebox coin compartment, 3) Under the restroom sink pipes, and 4) Tucked inside the cash register drawer."},
        {"q": "Does this ending unlock any new gameplay modes?", "a": "Yes! Unlocking the Hell Bartender ending opens 'Bartender Mode' in the main menu, where you serve drinks to underworld patrons in a fast-paced time-management mini-game."}
    ],
    "content": """
While most mortals trapped in Hell think only of flight or submission, true connoisseurs of mixology see an unprecedented career opportunity. In **Ending 5: The Master of Pandemonium (Under New Management)**, you neither flee back to Earth nor surrender as Femme Soule's pet. Instead, you out-mix, out-think, and out-drink everyone in the underworld, earning the respect of the ancient Ashen Bartender and inheriting Pandemonium itself.

This guide provides the complete step-by-step walkthrough to find all four hidden bartender logs, craft the mythical Forbidden Elixir, and seize the crimson vest.

---

## Prerequisites: Finding the 4 Bartender Logbooks

To initiate the Bartender succession storyline, you must locate four journal fragments penned by the tavern's original mortal founder:

```
[Logbook 1: The Foundation] -> Cellar storeroom, wedged behind bottom wine rack.
[Logbook 2: The Acoustic]   -> Lounge Jukebox, inside the coin mechanism panel.
[Logbook 3: The Plumbing]   -> Restroom, strapped to the copper pipes beneath the sink.
[Logbook 4: The Ledger]     -> Main bar, tucked under the false bottom of cash register.
```

1. **Log 1 (Cellar)**: Unlocked during Intermission 1 after opening the padlock (`1996`). Read notes on balancing demon ethanol.
2. **Log 2 (Jukebox)**: During Intermission 2, use the brass key found on the bartender's stool to open the jukebox maintenance hatch.
3. **Log 3 (Restroom)**: Crouch (`Ctrl` key) in the restroom to inspect the drain plumbing.
4. **Log 4 (Cash Register)**: While the Ashen Bartender is wiping glasses during Intermission 3, click the register drawer to retrieve the final entry.

Review room locations in [Pandemonium Bar Secrets](/guide/drunken-goddess-reflux-pandemonium-bar-secrets).

---

## Crafting The Forbidden Elixir

With all four logbooks in your inventory, interact with the brass shaker behind the bar counter. A golden prompt will announce: *"Secret Formula Deciphered: The Forbidden Elixir"*.

### Ingredients Required:
- **1x Ashen Rye (85% ABV)**: From the high-shelf spirits rack.
- **1x Blood Wine (45% ABV)**: From the counter supply.
- **1x [Holy Water Contraband](/drinks/drunken-goddess-reflux-holy-water-contraband)**: From your cellar loot.
- **1x Shaker Dust**: Automatically scraped from the antique brass shaker.

Complete the shaking rhythm with a **Perfect 100% score** to brew the shimmering, color-shifting elixir.

Detailed mixology mechanics in [Secret Cocktail Recipes and Mixology](/drinks/drunken-goddess-reflux-cocktail-recipes-mixology).

---

## Presenting the Drink to the Ashen Bartender

Before sitting down for Round 3, speak to the Ashen Bartender directly:
1. Select the new dialogue choice: *"I made something you haven't tasted in three centuries."*
2. Place the Forbidden Elixir on his bar mat.
3. The skeleton raises the glass to his empty eye sockets, downing it in one swift motion.
4. A faint golden flame ignites within his ribcage. He chuckles warmly:
   > *"Superb... the exact balance of mortal defiance and divine grace. The bar is yours, kid. Finish this duel, and take the shaker."*

---

## The Duel Requirement: The Master's Pour

In Round 3, you must finish the duel with absolute style:
- Do not let Femme Soule win through cheap trick spam.
- When the final two glasses remain, drink the second-to-last glass yourself to prove your tolerance.
- Offer the final high-proof glass to Femme Soule with a professional bow.
- She drinks it, gasps in admiration, and collapses onto the counter in blissful defeat.

See boss tactics in the [Femme Soule Boss Guide](/guide/drunken-goddess-reflux-femme-soule-boss-guide).

---

## The Coronation Cutscene: Under New Management

As Femme Soule slumps over, the Ashen Bartender unties his tailored crimson vest and lays it across the bar counter alongside the antique silver shaker. He tips his bowler hat:
> *"My shift ended two hundred years ago. Keep the beer cold and don't let the hellhounds chew the stools."*

His bones dissolve into sparkling white dust. Your character picks up the vest, slips it on, rolls up their sleeves, and grabs the shaker. Femme Soule stirs awake, resting her chin on her hands with starry eyes: *"Well, well, bartender... what's on the house tonight?"*

Unlocks the **"Under New Management"** Steam achievement and the bonus **Bartender Mode**! Full details in [Steam Achievements Guide](/codes/drunken-goddess-reflux-steam-achievements-guide).

---

## Pro Tip: Bartender Mode Fast Cash

In the newly unlocked Bartender Mode, serving patrons their requested cocktails within 5 seconds grants multiplier tips that translate directly into Skull Coins for your main campaign save!

---

## Related Guides & Next Steps

Continue exploring Pandemonium's lore:
- See all other endings in [All Endings Guide](/endings/drunken-goddess-reflux-all-endings-guide).
- Learn about the narrative themes in [Seven Flavors of Ruin Breakdown](/endings/drunken-goddess-reflux-seven-flavors-of-ruin-breakdown).
- Master all recipes in [Cocktail Recipes and Mixology](/drinks/drunken-goddess-reflux-cocktail-recipes-mixology).
- Discover active redeem codes in [Codes and Passwords](/codes/drunken-goddess-reflux-codes-and-passwords).
"""
}

# 18. Mutual Reflux Secret Ending
endings["drunken-goddess-reflux-mutual-reflux-secret-ending"] = {
    "title": "Mutual Reflux Secret Ending Guide: Double Oblivion",
    "description": "Unlock the hidden Mutual Reflux ending in Drunken Goddess Reflux by simultaneously tipping both soul gauges past the breaking point.",
    "hub": "endings",
    "slug": "drunken-goddess-reflux-mutual-reflux-secret-ending",
    "quickGuide": [
        "Both player and Femme Soule must reach exactly 100% Intoxication on the same turn.",
        "Requires the rare 'Tied Souls' Drunken Trick card drawn at 80% Intoxication.",
        "Set up the counter with two adjacent high-proof or lethal Spiritum glasses.",
        "Initiate a forced mutual toast to trigger simultaneous dual soul reflux.",
        "Unlocks the hidden 'Soul Twins' gold trophy and secret cosmic purgatory cutscene."
    ],
    "faq": [
        {"q": "What is the Mutual Reflux ending in Drunken Goddess Reflux?", "a": "Ending 4: Mutual Reflux (Double Oblivion) is a hidden dark-comedy ending where both participants drink themselves past their absolute limits at the exact same moment, expelling both of their souls simultaneously into a shared purgatory."},
        {"q": "How do you ensure both gauges hit 100% together?", "a": "By using the 'Tied Souls' card when both player and demon are around 75-80% Intoxication, and then sharing a Double Shot of Spiritum or Brimstone Absinthe."},
        {"q": "Does Mutual Reflux count as a victory or a defeat?", "a": "Neither! The game considers it a draw/special tie condition, awarding the exclusive 'Soul Twins' achievement and unlocking secret dialogue in future runs."}
    ],
    "content": """
Among the seven narrative pathways woven into **Drunken Goddess Reflux**, none is as mechanically demanding or delightfully chaotic as **Ending 4: Mutual Reflux (Double Oblivion)**. While standard gameplay pits you against Femme Soule in a duel where one must outlast the other, Mutual Reflux asks: *What happens if both mortal and demon push past their mortal and immortal limits at the exact same instant?*

The answer is a spectacular, screen-shattering double-reflux cutscene that hurls both characters into an ethereal cosmic purgatory. This guide breaks down the precise mathematical setup, card combo, and timing required to pull off this legendary secret ending.

---

## The Core Trigger Condition: Simultaneous 100%

To trigger Ending 4, both you and Femme Soule must transition from <100% Intoxication to **>=100% Intoxication during the resolution of the same turn action**.

```
[Player Gauge: 80%]        [Femme Soule Gauge: 82%]
         │                            │
         └───[Tied Souls Card Active]─┘
                      │
                      ▼
         [Mutual Toast: Spiritum 96%]
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
[Player: 130% Reflux]     [Demon: 132% Reflux]
        └─────────────┬─────────────┘
                      ▼
        [SIMULTANEOUS SOUL PURGE!]
```

If one character hits 100% even a single frame before the other, the game will default to either Ending 1 (Player Win) or Ending 3 (Player Loss). Precision is mandatory.

---

## Required Deck Setup: The "Tied Souls" Card

The linchpin of this ending is the rare Tier 3 trick card: **Tied Souls**.
- **How to Get It**: You have a 25% chance to draw *Tied Souls* upon crossing the 80% Intoxication milestone, or you can purchase it from the Ashen Bartender for 30 Skull Coins during Intermission 2.
- **Card Effect**: Links the player's glass to the demon's glass. When you take a drink, Femme Soule must immediately consume the glass placed opposite yours.

Review the full card roster in [Drunken Tricks and Deception Cards Guide](/guide/drunken-goddess-reflux-drunken-tricks-guide).

---

## Step-by-Step Execution Protocol in Round 3

Follow these exact steps in Round 3 to guarantee synchronized reflux:

1. **Step 1: Balance the Meters (Rounds 1 & 2)**
   - Enter Round 3 with your Intoxication around **60% – 70%** and Femme Soule's Intoxication around **65% – 75%**.
2. **Step 2: Isolate the Lethal Spirits**
   - Identify [Spiritum (96%)](/drinks/drunken-goddess-reflux-spiritum-lethal-shot-guide) and [Brimstone Absinthe (75%)](/drinks/drunken-goddess-reflux-brimstone-absinthe-guide). Use *Sleight of Hand* to position them side-by-side on the counter.
3. **Step 3: Pop the Tied Souls Card**
   - On your turn, play *Tied Souls*. Crimson chains of spectral energy will bind your wrist to Femme Soule's wrist.
4. **Step 4: The Fatal Clink**
   - Select Spiritum. The chains will force Femme Soule to pick up Brimstone Absinthe.
   - Raise your glasses and drink together.
   - You absorb +50% (reaching 120%+). Femme Soule absorbs +35% (reaching 110%+).

---

## The Double Reflux Cutscene: Cosmic Purgatory

The moment both glasses hit the wood, both characters freeze. A double-split screen appears:
- On the left, your mortal soul erupts into glowing azure starlight.
- On the right, Femme Soule's demonic essence explodes in violet hellfire.

Both souls collide above the counter, fusing together into a swirling nebular vortex. The tavern of Pandemonium dissolves, leaving you and Femme Soule floating in a serene, neon-lit void of outer space. Floating side-by-side like two comatose spirits, she turns her spectral head toward you and laughs with pure, unfiltered delight:
> *"Pfft... ahaha! Look at us, darling! We broke the whole damn universe! Now who buys the next round?!"*

Unlocks the ultra-rare **"Soul Twins"** Steam achievement! Check all trophy descriptions in [Steam Achievements Guide](/codes/drunken-goddess-reflux-steam-achievements-guide).

---

## Priority and Comparison Table: Ending Difficulty

| Ending Name | Setup Complexity | Required Cards | Skill Ceiling |
| :--- | :--- | :--- | :--- |
| **Reclaimed Dawn (True)** | Moderate | 1 Swap + Holy Water | High |
| **Eternal Partner (Romance)** | Low | Garnish / Dialogue | Easy |
| **Mutual Reflux (Double)** | **Extremely High** | **Tied Souls + Dual High Proof** | **Master** |
| **Hell Bartender (Career)** | High | 4 Logs + Elixir | Hard |

---

## Pro Tip: Skull Coin Insurance

If you reach Round 3 without the *Tied Souls* card in your hand, you can bribe the Ashen Bartender with 25 Skull Coins (`B` key prompt at counter) to instantly redraw your hand, guaranteeing *Tied Souls* if your meter is currently above 75%.

---

## Related Guides & Next Steps

Continue exploring the boundaries of Drunken Goddess Reflux:
- Review the complete narrative hierarchy in [All Endings Guide](/endings/drunken-goddess-reflux-all-endings-guide).
- Analyze the philosophical themes in [Seven Flavors of Ruin Breakdown](/endings/drunken-goddess-reflux-seven-flavors-of-ruin-breakdown).
- Check the complete drink specs in [Drink Tier List](/drinks/drunken-goddess-reflux-drink-tier-list).
- See full achievement unlock requirements in [Steam Achievements Guide](/codes/drunken-goddess-reflux-steam-achievements-guide).
"""
}

# 19. Seven Flavors of Ruin Breakdown
endings["drunken-goddess-reflux-seven-flavors-of-ruin-breakdown"] = {
    "title": "Seven Flavors of Ruin Explained: Lore and Themes",
    "description": "Deep dive into the narrative and thematic significance of the seven endings in Drunken Goddess Reflux, written by Fuyuki Hayashi.",
    "hub": "endings",
    "slug": "drunken-goddess-reflux-seven-flavors-of-ruin-breakdown",
    "quickGuide": [
        "Written by director Fuyuki Hayashi (creator of Yunyun Syndrome!?).",
        "The seven endings metaphorically represent seven psychological stages of addiction.",
        "Character design by odyk subtly changes in each ending cutscene.",
        "The soundtrack by Aiobahn +81 dynamically adapts to each ending outcome.",
        "Themes explore codependency, mortality, surrender, and existential freedom."
    ],
    "faq": [
        {"q": "Who wrote the story for Drunken Goddess Reflux?", "a": "The narrative, worldbuilding, and dialogue were conceived and written by producer and director Fuyuki Hayashi (WHO YOU), known for psychological indie hits like Yunyun Syndrome!? Rhythm Psychosis and Crystar."},
        {"q": "What do the 'Seven Flavors of Ruin' symbolize?", "a": "Each flavor of ruin corresponds to an emotional and psychological response to overwhelming desire and mortality: Freedom, Devotion, Resignation, Nihilism, Ambition, Physical Decay, and Soul Dissolution."},
        {"q": "Is Drunken Goddess Reflux connected to other WHO YOU games?", "a": "While set in its own distinct underworld universe, the game contains subtle Easter eggs, recurring musical motifs, and thematic parallels to Fuyuki Hayashi's previous works."}
    ],
    "content": """
Behind the flashy neon aesthetic, infectious electronic beats by Aiobahn +81, and darkly comedic premise of shot-glass Russian roulette lies a profoundly poignant narrative crafted by director **Fuyuki Hayashi** (WHO YOU). In **Drunken Goddess Reflux**, Hell is not a fiery torture chamber of brimstone and pitchforks; it is a cozy, suffocating speakeasy where the damned willingly drink themselves into oblivion to escape their mortal burdens.

The game's seven conclusions—canonically dubbed the **Seven Flavors of Ruin**—serve as an allegorical exploration of addiction, codependency, the fear of mortality, and the terrifying beauty of surrender.

This thematic deep dive analyzes the literary and artistic elements behind each ending, examining odyk's expressive character designs, Nanahira's vocal nuances, and Hayashi's philosophical intentions.

---

## The Thematic Spectrum of Pandemonium

Director Fuyuki Hayashi structured the seven endings along a philosophical axis ranging from **Radical Autonomy** to **Complete Dissolution**:

```
RADICAL AUTONOMY                                        COMPLETE DISSOLUTION
     │                                                           │
[Ending 1] ──── [Ending 5] ──── [Ending 2] ──── [Ending 4] ──── [Ending 3 / 6 / 7]
  Escape          Career          Romance         Absurdism         Destruction
 (Dawn)         (Bartender)      (Devotion)       (Mutual)           (Husk)
```

1. **Flavor 1: The Bitter Clarity of Dawn (Ending 1: Reclaimed Dawn)**
   - The mortal rejects the intoxicating comfort of Hell. Escaping Pandemonium is not presented as an easy triumph, but as a grueling, bitter survival test. Walking out into the morning cold means facing mortal pain, bills, and loneliness—yet it is real freedom.
   - Walkthrough: [True Ending Freedom Walkthrough](/endings/drunken-goddess-reflux-true-ending-freedom).

2. **Flavor 2: The Sweet Poison of Devotion (Ending 2: Eternal Pour)**
   - The ultimate representation of codependency. Femme Soule's yandere obsession mirrors the allure of escapism: staying in a warm bar where an all-powerful being worships you forever. It is an intoxicating, voluntary damnation.
   - Walkthrough: [Eternal Drinking Partner Romance Ending](/endings/drunken-goddess-reflux-eternal-partner-ending).

3. **Flavor 3: The Flat Dregs of Defeat (Ending 3: Soul-Spilled Husk)**
   - The tragedy of being consumed. Your soul becomes a trinket on a demon's shelf. It represents the loss of self-determination when one is overwhelmed by forces greater than oneself.

4. **Flavor 4: The Effervescent Absurdity (Ending 4: Mutual Reflux)**
   - Hayashi's signature existential humor. When both participants collapse simultaneously, the rules of Hell collapse with them. It suggests that when life is taken to its most extreme absurdity, connection is found in shared failure.
   - Walkthrough: [Mutual Reflux Secret Ending](/endings/drunken-goddess-reflux-mutual-reflux-secret-ending).

5. **Flavor 5: The Smoky Ambition of the Craft (Ending 5: Hell Bartender)**
   - Rather than suffering under the system or running from it, you take ownership of it. Putting on the crimson vest symbolizes finding purpose within darkness.
   - Walkthrough: [Hell Bartender Ending](/endings/drunken-goddess-reflux-hell-bartender-ending).

6. **Flavors 6 & 7: The Sharp Agony of Decay (Endings 6 & 7)**
   - Biological and spiritual breakdown. Ending 6 (bleeding out from Ice Pick overuse) and Ending 7 (dissolving in acidic mezcal) serve as stark reminders that the physical body has finite limits.

Compare all ending conditions in our [All Endings Guide](/endings/drunken-goddess-reflux-all-endings-guide).

---

## Character Design Analysis: odyk's Visual Storytelling

Lead artist odyk designed Femme Soule with deliberate visual contradictions:
- **Her Outfit**: A sharp black evening cocktail dress paired with oversized demon horns that glow like heated neon glass.
- **Her Eyes**: Dilate progressively as her Intoxication meter rises, shifting from sharp amber slits to swirling violet spirals during Phase 3.
- **Her Expression in Defeat**: In the True Ending, she does not look angry; she looks in awe. For a demon accustomed to mortals cowering or succumbing, meeting someone with the fortitude to refuse her love leaves an indelible mark.

---

## Audio Integration: Aiobahn +81 and DEMONDICE

The soundtrack is an active storytelling agent in Drunken Goddess Reflux. Composed by electronic producer Aiobahn +81 with lyrics and vocals by DEMONDICE, the theme song *"DEMON'S SHOT"* evolves based on the ending you pursue:
- During the **True Ending**, the aggressive synth bass gives way to a triumphant, stripped-down piano outro.
- During the **Eternal Partner Ending**, Nanahira records an exclusive acoustic harmony that replaces DEMONDICE's verse, reflecting Femme Soule's victory.

Explore the full tracklist in [OST and DEMON'S SHOT Guide](/codes/drunken-goddess-reflux-ost-demons-shot-tracklist).

---

## Pro Tip: Viewing the Epilogue Gallery

After completing any ending, visit the **Jukebox Gallery** in the main menu. Each completed ending unlocks high-resolution concept art sketches by odyk accompanied by director's commentary tracks recorded by Fuyuki Hayashi!

---

## Related Guides & Next Steps

Continue your exploration of Drunken Goddess Reflux:
- Check all ending walkthroughs in [All Endings Guide](/endings/drunken-goddess-reflux-all-endings-guide).
- Learn how to master the duel in [Survival Strategies Guide](/guide/drunken-goddess-reflux-survival-strategies).
- See all drink properties in [Drink Tier List](/drinks/drunken-goddess-reflux-drink-tier-list).
- Review all game achievements in [Steam Achievements Guide](/codes/drunken-goddess-reflux-steam-achievements-guide).
"""
}

# Write all 6 endings guides
for slug, data in endings.items():
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

print(f"Successfully generated all {len(endings)} guides for 'endings' hub.")
