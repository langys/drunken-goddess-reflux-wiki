#!/usr/bin/env python3
"""Generate all 7 guides for the 'guide' hub in content/en/."""

import pathlib

OUT = pathlib.Path("content/en")
OUT.mkdir(parents=True, exist_ok=True)

guides = {}

# 1. Beginner Guide
guides["drunken-goddess-reflux-beginner-guide"] = {
    "title": "Drunken Goddess Reflux Beginner Guide: Tips and Mechanics",
    "description": "Master Drunken Goddess Reflux with beginner tips on shot roulette, intoxication meters, ice pick resets, and surviving Hell's Pandemonium bar.",
    "hub": "guide",
    "slug": "drunken-goddess-reflux-beginner-guide",
    "quickGuide": [
        "Inspect glass meniscus, bubbles, and vapor before choosing or passing any shot.",
        "Keep Intoxication below 75% in early rounds to preserve hand steadiness and vision clarity.",
        "Reserve the Ice Pick for emergency thresholds (85%+ Intoxication) to avoid fatal reflux.",
        "Watch Femme Soule's facial smirk and Nanahira's voice inflection to detect high-proof bluffs.",
        "Between drinking duels, explore Pandemonium to discover recipe clues and contraband tools."
    ],
    "faq": [
        {"q": "What is the primary objective in Drunken Goddess Reflux?", "a": "Your goal is to survive a high-stakes shot-glass Russian roulette in Hell's Pandemonium bar against the demon Femme Soule, forcing her Intoxication meter past 100% until she vomits her demonic soul before you lose yours."},
        {"q": "When should I use the Ice Pick in Drunken Goddess Reflux?", "a": "Use the Ice Pick only when your Intoxication gauge crosses 85% or when facing a lethal 96% Spiritum shot. Stabbing your hand clears 3 intoxication points, buying critical breathing room at the cost of slight hand tremor."},
        {"q": "Does Femme Soule play fair during the drinking rounds?", "a": "No. Femme Soule uses demon deception cards such as Triple Multiplier and Glass Swap as the game progresses. You must counter her cheats by unlocking your own drunken barfly tricks."}
    ],
    "content": """
Entering Pandemonium, the neon-drenched subterranean tavern of Hell, presents players with a surreal blend of psychological dread and dark humor. In **Drunken Goddess Reflux**, you sit across from Femme Soule (voiced with erratic charm by Nanahira), an obsessive demon who wants nothing more than to share eternity with you—even if that eternity involves both of your souls being violently expelled across the mahogany counter. To escape Hell and reclaim your mortal life, you must understand the rules of this twisted shot-glass Russian roulette, master intoxication management, and outwit a supernatural opponent who loves you enough to kill you.

This beginner guide details everything new players need to survive their opening duels, read liquid tells, make strategic decisions under sensory impairment, and turn the demon's drunken obsession into your pathway to freedom.

---

## The Core Gameplay Loop: Shot-Glass Russian Roulette

At its heart, Drunken Goddess Reflux is an intense turn-based duel governed by hidden probabilities, sensory cues, and psychological warfare. Each round begins with a lineup of six to eight unlabelled shot glasses placed squarely between you and Femme Soule. While every glass looks nearly identical at first glance, their liquid contents range from harmless 0% Void Tonic to lethal 96% Spiritum hellfire ethanol.

During your turn, you must make a decisive choice:
1. **Choose a Glass and Drink It Yourself**: If you suspect a low-proof beverage or need to safely cycle the table, drinking it yourself absorbs the alcohol but preserves table control.
2. **Force Femme Soule to Drink**: By playing deception cards or calling specific duel rules, you can push a suspicious shot across the counter to Femme Soule.
3. **Execute a Drunken Trick**: As your intoxication meter rises, your drunken stupor unlocks unique barfly tricks, such as glass swapping, liquid smelling, or napkin spitting.

The round continues until either you or Femme Soule hits the critical **Reflux Threshold** (100% Intoxication), triggering an uncontrollable soul purge. If Femme Soule vomits first, you clear the stage; if you vomit first, your soul shatters, binding you to Hell forever.

For a deeper mathematical breakdown of shot distribution and odds, consult our comprehensive [Russian Roulette Rules Explained](/guide/drunken-goddess-reflux-russian-roulette-mechanics) guide.

---

## Understanding Your Gauges: Intoxication vs Soul Stability

Surviving the night requires monitoring two interconnected resources displayed on your vintage leather coaster HUD:

### 1. The Intoxication Gauge (0% – 100%)
Your Intoxication Gauge tracks the cumulative blood-alcohol density of your mortal avatar. As alcohol accumulates, several mechanical modifiers activate:
- **0% – 35% (Sober to Buzzing)**: Full screen clarity, steady cursor aim, zero dialogue distortion, but no drunken trick cards available.
- **36% – 70% (Tipsy to Intoxicated)**: Screen begins a gentle rhythmic wobble; ambient audio muffles slightly; unlocks Tier 1 Drunken Tricks like Sleight of Hand and False Toast.
- **71% – 85% (Heavily Wasted)**: Chromatic aberration and double vision appear; Nanahira's demonic voice lines begin echoing; unlocks powerful Tier 2 Deception Cards.
- **86% – 99% (Near-Lethal Reflux Danger)**: Heartbeat audio pounds loudly; extreme screen distortion; any additional high-proof shot triggers instant soul reflux unless mitigated immediately.

### 2. Soul Stability
Soul Stability represents your spiritual cohesion. Unlike Intoxication, which fluctuates with each drink, Soul Stability is a permanent health pool across rounds. Taking severe bodily trauma—such as driving an ice pick through your knuckles—or drinking cursed underworld spirits permanently chips away at Soul Stability. If Soul Stability drops to zero, you immediately suffer the tragic Void Blackout ending.

Learn how to safely balance these gauges in our dedicated [Intoxication and Ice Pick Guide](/guide/drunken-goddess-reflux-intoxication-ice-pick-guide).

---

## The Ice Pick: Your Painful Reset Button

Placed directly to the right of your drink coaster sits a tarnished, stainless-steel ice pick. In Drunken Goddess Reflux, the ice pick is not a weapon against the demon; it is an agonizing tool of self-preservation.

When your Intoxication climbs into the critical red zone (85%+), the player character's vision begins closing in with black tunnel vignettes. By selecting the Ice Pick, you can drive the spike into your non-dominant hand. The sudden rush of adrenaline and shock immediately purges **3 points of Intoxication** (approximately 25% to 30% of your gauge), snapping your vision back to sharp focus.

However, this salvation carries heavy consequences:
- Your cursor will suffer persistent tremors for the rest of the round, making rapid glass selection harder.
- You lose a chunk of maximum Soul Stability.
- Using the ice pick more than once per game locks you out of the coveted "Iron Liver" achievement and the pristine [True Ending Escape](/endings/drunken-goddess-reflux-true-ending-freedom).

---

## Beginner Step-by-Step Survival Walkthrough

Follow this battle-tested roadmap during your initial matches in Pandemonium:

```
Step 1: Visual Inspection -> Check meniscus bubbles and rim residue
Step 2: Note Turn Order   -> Allow Femme Soule to drink first if possible
Step 3: Track Proof Tally -> Calculate remaining high-proof odds
Step 4: Bait Demon Cheats -> Use low-proof shots to draw out her Triple card
Step 5: Lethal Delivery  -> Push Spiritum or Brimstone Absinthe to Femme Soule
```

1. **Round 1 (The Icebreaker)**: The first set contains mostly low-to-medium proof spirits like Void Tonic and Blood Wine. Use this round to observe Femme Soule's baseline vocal cadence and build up your initial trick card hand.
2. **Round 2 (The Escalation)**: Higher proof liquors enter the rotation, including Purgatory Gin and Brimstone Absinthe. Keep your intoxication around 50% to ensure trick cards are available, but avoid taking two consecutive drinks.
3. **Round 3 (The Hellfire Showdown)**: The bartender introduces **Spiritum** (96% proof). At this stage, one wrong glass will end the match. Use trick cards like Sleight of Hand to redirect the Spiritum glass directly to Femme Soule.

To understand the exact lethal thresholds of every bottle on the shelf, study the [Drunken Goddess Reflux Drink Tier List](/drinks/drunken-goddess-reflux-drink-tier-list).

---

## Priority and Comparison Table: Early Game Decisions

| Action / Situation | Risk Level | Sobriety Impact | Tactical Value | Recommended Timing |
| :--- | :--- | :--- | :--- | :--- |
| **Drink Unknown Shot** | High | +10% to +50% | Low | Only when odds of safe tonic are >75% |
| **Inspect Glass Closely** | Zero | 0% | Very High | Every single turn before touching glass |
| **Use Ice Pick Reset** | Very High | -25% to -30% | Critical Emergency | Only at 85%+ Intoxication |
| **Play Sleight of Hand** | Moderate | -5% Trick Cost | High | When lethal Spiritum is identified |
| **Pass Turn to Demon** | Low | 0% | Moderate | When 2+ high proof shots remain on bar |

---

## Key Tactical Takeaways

> [!IMPORTANT]
> **Audio Cues Are Never Random**: Pay close attention to Nanahira's voice acting. When Femme Soule is holding a glass with over 60% proof, her giggle has a distinct pitch shift, and her demonic horns glow faintly red.

> [!TIP]
> **Do Not Waste Trick Cards Early**: You only draw one new trick card for every 20% of intoxication gained. Wasting your swap cards on 15% beer will leave you defenseless when Spiritum arrives on the counter.

> [!NOTE]
> **Intermission Exploration Matters**: Between rounds, do not immediately click 'Next Round'. Walk around the 3D bar environment in Pandemonium to locate hidden recipe cards and chat with NPC patrons as detailed in [Pandemonium Bar Secrets](/guide/drunken-goddess-reflux-pandemonium-bar-secrets).

---

## Pro Tip: The Napkin Spit Bluff

A secret mechanic not highlighted in the tutorial involves the linen napkin on the bar rail. If you possess at least 40% Intoxication and choose to drink a glass yourself, holding `Right-Click` right as your character brings the shot to their lips triggers a subtle "Spit Bluff". 

If Femme Soule is looking away or adjusting her choker, your character secretly dumps half the alcohol into the napkin, reducing incoming intoxication by 50% while convincing the demon that the glass was completely drained. Mastering this timing gives you an immense statistical edge.

---

## Related Guides & Next Steps

Continue your journey through Hell by mastering our advanced survival resources:
- Study the full breakdown of liquid properties in [All Drinks and Proof Catalog](/drinks/drunken-goddess-reflux-all-drinks-proof-catalog).
- Discover how to unlock every narrative path in [All Endings Guide (7 Flavors of Ruin)](/endings/drunken-goddess-reflux-all-endings-guide).
- Prepare for the final encounter with our tactical [Femme Soule Boss Guide](/guide/drunken-goddess-reflux-femme-soule-boss-guide).
- Check active rewards and bonuses in [Drunken Goddess Reflux Codes and Passwords](/codes/drunken-goddess-reflux-codes-and-passwords).
"""
}

# 2. Russian Roulette Mechanics
guides["drunken-goddess-reflux-russian-roulette-mechanics"] = {
    "title": "Drunken Goddess Reflux Russian Roulette Rules Explained",
    "description": "Understand shot selection, proof mechanics, turn order, and rule-breaking systems in Drunken Goddess Reflux's demon drinking contest.",
    "hub": "guide",
    "slug": "drunken-goddess-reflux-russian-roulette-mechanics",
    "quickGuide": [
        "Rounds feature arrays of 6 to 8 unlabelled glasses randomized from a fixed proof pool.",
        "Alcohol proofs range across 4 tiers: Safe (0%), Mild (15-30%), Heavy (40-65%), and Lethal (75-96%).",
        "Reflux occurs at exactly 100% Intoxication, triggering immediate defeat or victory based on who vomits.",
        "Visual tells like surface meniscus curvature and bubble ascent speeds reveal proof density.",
        "Turn order switches dynamically whenever a player plays specific Drunken Trick cards."
    ],
    "faq": [
        {"q": "How does shot-glass Russian roulette differ from traditional roulette?", "a": "Instead of a single lethal bullet, every shot in Drunken Goddess Reflux adds cumulative alcohol percentage. Lethality depends on threshold management, trick cards, and baiting your opponent into high-proof traps."},
        {"q": "Can you check the alcohol content before picking a glass?", "a": "Yes. Hovering over a glass initiates a visual inspection mode. Meniscus curvature, vapor shimmer, and micro-bubbles provide reliable physical hints about the alcohol proof."},
        {"q": "What happens if both participants reach 100% Intoxication together?", "a": "If both player and Femme Soule hit 100% simultaneously, you trigger the secret Mutual Reflux ending where both souls intertwine in eternal alcoholic purgatory."}
    ],
    "content": """
The central gameplay pillar of **Drunken Goddess Reflux** is its shot-glass Russian roulette system. Unlike traditional Russian roulette where death is binary and instantaneous, Drunken Goddess Reflux turns probability into a grueling battle of endurance, sensory observation, and strategic deception. Sitting across the mahogany counter of Pandemonium, you and Femme Soule alternate taking shots from a shared lineup of unmarked glasses.

This guide provides a thorough mechanical breakdown of how rounds are structured, how alcohol proofs translate into gauge percentages, how to visually inspect glasses, and how the rules begin to break down as the night deepens.

---

## Round Structure and Glass Pool Architecture

Every drinking bout in Pandemonium is divided into distinct rounds. At the start of a round, the Ashen Bartender sets down a tray containing between 6 and 8 glasses. The pool of drinks is generated according to a calibrated difficulty curve:

```
[Round 1: 6 Glasses] -> 3 Low Proof (0-20%) | 2 Med Proof (40-50%) | 1 High Proof (60%)
[Round 2: 7 Glasses] -> 2 Low Proof (0-20%) | 3 Med Proof (40-50%) | 2 High Proof (70-75%)
[Round 3: 8 Glasses] -> 1 Low Proof (0-20%) | 3 Med Proof (40-50%) | 3 High Proof (70-75%) | 1 Lethal Spiritum (96%)
```

Because the pool is finite within each round, card counting and glass elimination are essential skills. If three glasses have been drunk and two were low-proof tonics, the probability that the next glass contains 70%+ proof spikes dramatically.

To prepare yourself for the complete spectrum of beverages, see our detailed [All Drinks and Proof Catalog](/drinks/drunken-goddess-reflux-all-drinks-proof-catalog).

---

## Physical and Visual Tells: Reading the Glasses

While glasses share identical crystal shapes, developers WHO YOU implemented subtle physical rendering details that allow keen-eyed players to deduce proof levels without drinking:

### 1. Meniscus Surface Tension
- **Low Proof (0% – 25%)**: Water and tonic water exhibit high surface tension. The meniscus curves sharply upwards against the glass walls, forming a distinct crescent lip.
- **High Proof (60% – 96%)**: Ethanol reduces surface tension. Spirits like Brimstone Absinthe or Spiritum lie almost completely flat, with zero upward curve at the rim.

### 2. Bubble Dynamics (The Effervescence Test)
- Tapping the table (`Q` key) causes subtle vibration ripples.
- Non-alcoholic and low-proof drinks produce small, buoyant bubbles that rise rapidly to the surface.
- High-proof spirits produce sluggish, oily micro-bubbles that linger or drift horizontally along viscosity currents.

### 3. Vapor and Heat Distortion
- Drinks above 70% ABV produce a faint, heat-haze distortion hovering 1-2 centimeters above the rim.
- In the case of **Spiritum** (96%), a distinct pale-blue luminescence flickers inside the glass when viewed from a 45-degree angle.

Mastering these visual tells is fundamental to our core [Beginner Guide Strategies](/guide/drunken-goddess-reflux-beginner-guide).

---

## Turn Order Dynamics and Passing Rules

Turns alternate strictly from left to right unless modified by player or demon actions. On your turn, you have three primary interactions:

1. **Drink Selected Glass**: You consume the drink. Your Intoxication Gauge increases by the drink's proof value divided by your avatar's current tolerance rating.
2. **Offer Glass to Femme Soule**: Certain Drunken Trick cards (like *The Devil's Toast*) allow you to force Femme Soule to drink on your turn. If she accepts, her gauge increases; if she suspects foul play, she may attempt to slap the glass away or play a counter-card.
3. **Pass / Stall**: You can spend 10 Skull Coins or 1 Focus Token to pass the turn to Femme Soule, forcing her to pick from the current glass selection.

For an exhaustive guide on managing your gauge during these critical turns, refer to our [Intoxication and Ice Pick Guide](/guide/drunken-goddess-reflux-intoxication-ice-pick-guide).

---

## The Rule-Breaking Phase: High Intoxication Anarchy

As both combatants accumulate alcohol, the formal rules of Russian roulette unravel. Once either participant reaches **70% Intoxication**, the game enters the **Anarchy Phase**:

| Intoxication Tier | Mechanical Rule Alteration | Demon Behavior Shift |
| :--- | :--- | :--- |
| **0% – 49%** | Standard turns, 1 glass per action, strict timer | Playful banter, low aggression |
| **50% – 69%** | Deception cards unlocked, 15-second turn timer | Begins bluffing, plays Triple card |
| **70% – 84%** | Double Shot enabled; glass swapping permitted | Obsessive dialogue, horn visual flare |
| **85% – 99%** | Rapid-fire turns; Ice Pick available; blind picks | Desperate clinging; attempts forced toasts |

When Double Shot is activated, selecting a glass forces the drinker to immediately down a second adjacent glass. If a high-proof spirit is paired with Spiritum, this can instantly push an opponent from 30% to 100% in a single turn.

Learn how to safely deploy these high-tier moves in our [Drunken Tricks and Deception Cards Guide](/guide/drunken-goddess-reflux-drunken-tricks-guide).

---

## The Reflux Mechanic: Deciding Victory and Defeat

When either character reaches **100% Intoxication**, the duel halts immediately. The character triggers the dramatic **Soul Reflux Animation**:
- **Femme Soule Reflux**: Her eyes widen in drunken ecstasy and horror; purple demonic ectoplasm erupts from her lips; she collapses across the bar counter. You win the round and advance toward the [True Ending Escape](/endings/drunken-goddess-reflux-true-ending-freedom).
- **Player Reflux**: Your mortal body convulses; your glowing human soul is disgorged onto the table; Femme Soule scoops it up joyfully, declaring you her eternal partner forever.

---

## Pro Tip: Calculating Demon Bait Windows

Femme Soule has an AI behavioral bias: if there are only three glasses remaining and two of them are high-proof, she will almost always play her *Glass Swap* or *Triple* card on her turn. Anticipate this by purposefully selecting a low-proof glass with *Sleight of Hand* ready, allowing her to swap into the lethal glass on her own volition.

---

## Related Guides & Next Steps

Deepen your competitive mastery with these specialized resources:
- Review the ranking of all bar spirits in our [Drink Tier List](/drinks/drunken-goddess-reflux-drink-tier-list).
- Learn how to bait and counter the demon in the [Femme Soule Boss Guide](/guide/drunken-goddess-reflux-femme-soule-boss-guide).
- Discover what happens during simultaneous vomit in [Mutual Reflux Secret Ending](/endings/drunken-goddess-reflux-mutual-reflux-secret-ending).
- Find all bonus unlockables in [Drunken Goddess Reflux Steam Achievements Guide](/codes/drunken-goddess-reflux-steam-achievements-guide).
"""
}

# 3. Intoxication & Ice Pick Guide
guides["drunken-goddess-reflux-intoxication-ice-pick-guide"] = {
    "title": "Drunken Goddess Reflux Intoxication and Ice Pick Guide",
    "description": "How to manage intoxication levels, calculate risk thresholds, and use the ice pick mechanic to stay conscious in Drunken Goddess Reflux.",
    "hub": "guide",
    "slug": "drunken-goddess-reflux-intoxication-ice-pick-guide",
    "quickGuide": [
        "Intoxication accumulates from drink ABV proofs and triggers visual/audio distortion.",
        "The Ice Pick resets 3 intoxication points (~28% gauge) via self-inflicted pain.",
        "Using the Ice Pick inflicts permanent cursor tremor and reduces Soul Stability by 20%.",
        "Threshold 85%+ Intoxication is the only mathematically viable window to use the Ice Pick.",
        "Zero-ice-pick runs are mandatory to unlock the Iron Liver achievement and True Ending."
    ],
    "faq": [
        {"q": "How much intoxication does the Ice Pick clear?", "a": "The Ice Pick removes exactly 3 points of Intoxication, which corresponds to roughly 28% of your full gauge, instantly clearing red-tier tunnel vision."},
        {"q": "Can you use the Ice Pick more than once?", "a": "Yes, you can use it up to three times per game. However, each use permanently drops your Soul Stability and makes hand aim significantly more unstable."},
        {"q": "Are there non-lethal ways to lower Intoxication in Drunken Goddess Reflux?", "a": "Yes. Finding lemon peels, crushed ice, or smuggling Holy Water Contraband during intermissions can clear small amounts of intoxication without damaging your soul."}
    ],
    "content": """
In the supernatural drinking duel of **Drunken Goddess Reflux**, your body is your only shield and your greatest liability. As you down consecutive shots of demonic liquor, your mortal avatar experiences escalating intoxication that impairs your vision, slows your reflexes, and distorts the soundscape of Pandemonium. When alcohol toxicity threatens to force your soul from your throat, the game offers a single, agonizing lifeline: the Ice Pick.

This guide analyzes the exact mathematics of the Intoxication Gauge, the visual and physical stages of drunkenness, and how to utilize the Ice Pick with surgical precision to claim victory over Femme Soule.

---

## Intoxication Gauge Mechanics and Formulae

Your Intoxication Gauge operates on a 100-point scalar. When you drink a shot, the gauge increases based on the formula:

$$\\Delta \\text{Intoxication} = \\frac{\\text{Drink ABV} \\times \\text{Proof Factor}}{\\text{Mortal Resilience}}$$

- **Base Resilience**: Starts at 1.0. Completing exploration challenges in Pandemonium can raise this up to 1.25.
- **Proof Factor**: Standard drinks range from 0.15 (Void Tonic) to 0.96 (Spiritum).
- **Multiplier Modifiers**: If Femme Soule plays her *Triple Pain* card, the incoming intoxication value is multiplied by 3.0, guaranteeing an instant overflow if the drink is above 35% ABV.

Understanding these formulas is critical when planning turns in our [Beginner Guide Strategies](/guide/drunken-goddess-reflux-beginner-guide) and executing [Survival Strategies](/guide/drunken-goddess-reflux-survival-strategies).

---

## The Four Stages of Drunkenness

As intoxication mounts, the game layers dynamic post-processing effects that directly alter player gameplay:

```
[0% - 35%]: Sober Clarity  -> Sharp textures, stable cursor, normal audio.
[36% - 65%]: Buzzed Haze    -> Screen sway (0.5Hz), faint neon color trails, Tier 1 tricks open.
[66% - 84%]: Heavy Slur    -> Severe screen wobble, chromatic aberration, audio pitch drop.
[85% - 99%]: Red Zone Panic -> Black tunnel vignette, violent cursor shake, loud heartbeat.
```

### Stage 1: Sober Clarity (0% – 35%)
At this stage, you have complete mechanical control. However, your character lacks the drunken audacity required to execute advanced tricks. It is best to drink low-proof beverages early to push into Stage 2 where your tactical card options broaden.

### Stage 2: Buzzed Haze (36% – 65%)
The screen begins a rhythmic, pendulum-like sway. More importantly, your first two card slots unlock. You can now use *Sleight of Hand* (swapping glasses) and *False Sip*.

### Stage 3: Heavy Slur (66% – 84%)
Double vision manifests. Dialogue choices on screen begin drifting across the interface. Nanahira's voice lines for Femme Soule gain a demonic harmonic resonance. Advanced deception cards unlock, but selecting glasses requires steadying the mouse.

### Stage 4: Red Zone Panic (85% – 99%)
Your avatar gasps for air. A pounding heartbeat muffles all background music. The edges of the screen darken with heavy vignette shadows. Any high-proof shot taken in this state triggers immediate 100% reflux.

For a full breakdown of drink proofs that push you between these stages, see the [All Drinks and Proof Catalog](/drinks/drunken-goddess-reflux-all-drinks-proof-catalog).

---

## The Ice Pick: Mechanics and Cost Analysis

Resting on a wooden cradle beside your coaster is the steel Ice Pick. Clicking the Ice Pick initiates a tense quick-time prompt: driving the spike directly into your left hand.

### What the Ice Pick Does:
1. **Instant Sobriety Burst**: Reduces current Intoxication by exactly **3 points** (approximately 28% of your gauge), dropping you from 95% down to 67%.
2. **Clears Red Zone Visuals**: Eliminates the tunnel vignette and resets heartbeat audio.
3. **Interrupts Demon Combo**: If Femme Soule has prepared a *Double Shot* toast, the shock of your action stuns her for 1 turn.

### The Permanent Costs:
- **Hand Tremor**: For the remainder of the match, cursor aim wobbles with high-frequency noise. Picking a glass requires timing your click with the tremor cycle.
- **Soul Stability Depletion**: Permanently deducts 20 points from your maximum Soul Stability pool. Three uses in one game leaves your soul hanging by a thread.
- **Narrative Lockout**: Using the Ice Pick even once prevents you from unlocking the pristine [True Ending Escape](/endings/drunken-goddess-reflux-true-ending-freedom) and the "Iron Liver" achievement.

---

## Mathematical Breakdown: When to Stab

The optimal time to use the Ice Pick follows strict statistical logic:

| Current Intoxication | Next Glass Risk | Action | Rationale |
| :--- | :--- | :--- | :--- |
| **Below 70%** | Any | **DO NOT USE** | Wasted recovery; severe penalties for minimal gain |
| **71% – 84%** | Low Proof Probable | **HOLD** | Better to risk a 20% drink than sacrifice soul health |
| **85% – 95%** | High Proof / Spiritum | **CRITICAL USE** | 100% chance of death without reset; stab immediately |
| **96% – 99%** | Any Unverified Glass | **MANDATORY USE** | Even 10% lager triggers reflux; use pick instantly |

Study how this threshold management synergizes with [Brimstone Absinthe Mechanics](/drinks/drunken-goddess-reflux-brimstone-absinthe-guide) and [Spiritum Lethal Shots](/drinks/drunken-goddess-reflux-spiritum-lethal-shot-guide).

---

## Pro Tip: Hand Warming Exploration Trick

During the 3D exploration intermission in Pandemonium, you can walk behind the bar and run your wounded hand under the hot-water tap near the sink. Doing so removes 50% of the cursor tremor penalty caused by earlier Ice Pick use, making aiming significantly easier in the subsequent round.

---

## Related Guides & Next Steps

Continue refining your survival skillset:
- Master turn sequencing in our [Russian Roulette Rules Explained](/guide/drunken-goddess-reflux-russian-roulette-mechanics).
- Discover secret healing items in [Pandemonium Bar Secrets](/guide/drunken-goddess-reflux-pandemonium-bar-secrets).
- Check the complete trophy conditions in [Steam Achievements Guide](/codes/drunken-goddess-reflux-steam-achievements-guide).
- Learn how to achieve victory without ever touching the pick in [True Ending Walkthrough](/endings/drunken-goddess-reflux-true-ending-freedom).
"""
}

# 4. Femme Soule Boss Guide
guides["drunken-goddess-reflux-femme-soule-boss-guide"] = {
    "title": "Femme Soule Boss Guide: Dialogue, Tells and Counters",
    "description": "Learn Femme Soule's drinking patterns, voice line tells by Nanahira, bluff counters, and how to force the demon to vomit her soul.",
    "hub": "guide",
    "slug": "drunken-goddess-reflux-femme-soule-boss-guide",
    "quickGuide": [
        "Femme Soule transitions through 3 behavioral phases as her Intoxication meter climbs.",
        "Voice actress Nanahira delivers distinct pitch shifts when holding high-proof or lethal spirits.",
        "Femme Soule's Triple Pain card can be countered using the Sleight of Hand trick card.",
        "Selecting affectionate dialogue options increases her tolerance but unlocks secret romance branches.",
        "Forcing Spiritum into her cup requires baiting her into an aggressive Double Toast turn."
    ],
    "faq": [
        {"q": "Who is Femme Soule in Drunken Goddess Reflux?", "a": "Femme Soule (also known as Fam Sour) is the demonic barfly patron of Hell's Pandemonium bar. Voiced by renowned voice artist Nanahira, she challenges mortal visitors to life-or-death drinking games out of obsessive love."},
        {"q": "How can you tell if Femme Soule is bluffing?", "a": "When Femme Soule pushes a high-proof glass across the table while claiming it is safe, her demonic horns flare with crimson embers and she avoids direct eye contact for two seconds."},
        {"q": "Can you defeat Femme Soule without using trick cards?", "a": "While theoretically possible with extraordinary luck, Femme Soule plays powerful demon cards in later rounds. Countering her moves with Drunken Tricks is essential on normal and hard difficulties."}
    ],
    "content": """
In the shadowed booths of Pandemonium, your adversary is not a faceless dealer—she is **Femme Soule** (Fam Sour), a liquor-soaked demoness whose fixation on your mortal soul is as deadly as it is endearing. Character designed by artist odyk and brought to manic, magnetic life by celebrated voice actress Nanahira, Femme Soule embodies the chaotic spirit of a barfly who would kill for you or kill you.

To defeat her and claim your freedom, you must analyze her behavioral patterns, recognize the vocal and physical tells hidden within Nanahira's performance, counter her devastating demonic cards, and guide her Intoxication gauge past 100%.

---

## Femme Soule's Three Psychological Phases

As Femme Soule consumes alcohol, her artificial intelligence shifts across three distinct combat phases:

```
[Phase 1: 0% - 40% Intoxication] -> The Playful Seductress: Light teasing, predictable picks, zero cheating.
[Phase 2: 41% - 75% Intoxication] -> The Obsessive Stalker: Aggressive bluffs, plays Triple Pain, glass swaps.
[Phase 3: 76% - 99% Intoxication] -> The Desperate Hellspawn: Forced double toasts, frantic cling, erratic turns.
```

### Phase 1: The Playful Seductress (0% – 40%)
During the opening round, Femme Soule acts like an amused lounge patron. She sips casually, comments on your mortal fragility, and adheres strictly to the basic rules of the duel. Her choices are largely determined by mathematical odds, making her prone to picking low-proof drinks. Use Phase 1 to stockpile trick cards and inspect the board.

### Phase 2: The Obsessive Stalker (41% – 75%)
As the alcohol takes hold, her eyes dilate and her demeanor shifts into possessive obsession. In Phase 2, she begins using her signature demon cards:
- **Triple Pain**: Triples the intoxication of the next glass consumed.
- **Hell's Swap**: Transposes two glasses on the mahogany counter.
- **Demonic Glare**: Disables your ability to inspect glasses for one turn.

When she plays *Triple Pain*, never drink from the table. Use *Sleight of Hand* or pass the turn to force the magnified penalty back onto her.

### Phase 3: The Desperate Hellspawn (76% – 99%)
In the endgame, her affection turns frantic. Terrified that you might win and escape her grasp, she attempts desperate maneuvers, including forced toasts where both players must drink adjacent glasses simultaneously. Her vocal delivery becomes breathless and chaotic.

Learn how to survive this climactic stage in our [Survival Strategies Guide](/guide/drunken-goddess-reflux-survival-strategies).

---

## Vocal Tells: Deciphering Nanahira's Voice Cues

The sound design in Drunken Goddess Reflux is a vital gameplay system. Nanahira recorded hundreds of nuanced vocal takes, embedding subtle clues into Femme Soule's dialogue:

| Voice Line / Vocal Cadence | Underlying Reality | Recommended Counter |
| :--- | :--- | :--- |
| **Playful high-pitch giggle with rapid tempo** | Holding Safe Tonic (0% – 20%) | Safe to drink or allow her to take it |
| **Drawn-out sultry whisper with vocal fry** | Holding Heavy Liquor (50% – 70%) | Swap glass or play defensive bluff |
| **Sudden nervous stutter or voice crack** | Holding Lethal Spiritum (96%) | **DANGER**: Force her to drink immediately |
| **Loud, theatrical toast announcement** | Playing *Triple Pain* trap | Use Napkin Spit or Sleight of Hand |

Whenever she pauses before picking a glass and lets out an erratic hum, her AI is evaluating whether to bluff. If her gaze darts to the ice bucket on the bar, she knows the glass in front of her is hazardous.

---

## Countering Her Demonic Deception Cards

Femme Soule draws from a custom deck of infernal cards. Here is how to neutralize her most dangerous tactics:

```
Demon Card: Triple Pain -> Triples next drink damage.
Counter: Play 'Sleight of Hand' to swap her glass with Spiritum. Result: Instant 100% Reflux!

Demon Card: Hell's Swap -> Swaps your chosen glass with a mystery glass.
Counter: Mark glasses mentally by noting rim defects; never trust her swapped placement.

Demon Card: Devoted Cling -> Forces you to take the same drink she takes.
Counter: Activate your 'Napkin Spit' to dump your portion while she absorbs full proof.
```

Master the full deck of player countermeasures in our [Drunken Tricks and Deception Cards Guide](/guide/drunken-goddess-reflux-drunken-tricks-guide).

---

## Dialogue Choices and Romance Branches

Between drinks, Femme Soule initiates interactive dialogue prompts. Your answers influence her alcohol tolerance and narrative flags:

1. **Rebellious Answers ("I'm leaving this hellhole tonight")**: Lowers her affection, increases her aggression, and drives towards the [True Ending Escape](/endings/drunken-goddess-reflux-true-ending-freedom).
2. **Affectionate Answers ("You look breathtaking under the neon, Femme")**: Raises her affection, grants bonus Skull Coins, but makes her more likely to trigger the [Eternal Partner Romance Ending](/endings/drunken-goddess-reflux-eternal-partner-ending).
3. **Chaotic Answers ("Let's see who dies first!")**: Increases overall game tempo, leading toward the [Mutual Reflux Secret Ending](/endings/drunken-goddess-reflux-mutual-reflux-secret-ending).

---

## Pro Tip: The Jukebox Distraction

Before starting a round, walk to the Jukebox in Pandemonium and select the high-tempo track *"DEMON'S SHOT"*. The loud bass causes Femme Soule to bob her head rhythmically during turns, reducing the window of time she spends analyzing your glass picks by approximately 25%.

---

## Related Guides & Next Steps

Continue mastering the encounter with Femme Soule:
- Learn the basics in our [Beginner Guide](/guide/drunken-goddess-reflux-beginner-guide).
- See the full drink rankings in [Drink Tier List](/drinks/drunken-goddess-reflux-drink-tier-list).
- Review all ending routes in [All Endings Guide](/endings/drunken-goddess-reflux-all-endings-guide).
- Check the official music credits in [OST and DEMON'S SHOT Tracklist](/codes/drunken-goddess-reflux-ost-demons-shot-tracklist).
"""
}

# 5. Pandemonium Bar Secrets
guides["drunken-goddess-reflux-pandemonium-bar-secrets"] = {
    "title": "Pandemonium Bar Secrets and 3D Exploration Guide",
    "description": "Explore the Pandemonium bar in Drunken Goddess Reflux. Uncover hidden lore notes, secret cocktail ingredients, and patron interactions.",
    "hub": "guide",
    "slug": "drunken-goddess-reflux-pandemonium-bar-secrets",
    "quickGuide": [
        "Use intermission intervals to freely roam the 3D rendered Pandemonium tavern.",
        "Inspect the wine cellar padlock behind the bar to discover Holy Water Contraband.",
        "Talk to the Ashen Bartender to unlock secret cocktail recipes and world lore.",
        "Examine the neon Jukebox to change BGM tracks and discover secret code inputs.",
        "Read discarded bar napkins to uncover Fuyuki Hayashi's hidden game lore notes."
    ],
    "faq": [
        {"q": "Can you explore Pandemonium during drinking rounds?", "a": "No. Free exploration is available exclusively during the intermissions between rounds. Once you sit down at the counter, the game locks into the first-person duel perspective."},
        {"q": "Where is the Holy Water Contraband located in Pandemonium?", "a": "The Holy Water Contraband is locked in the cellar storeroom behind the bar. You need the 4-digit code found on the restroom mirror to unlock the padlock."},
        {"q": "Do interactions in the bar affect the main drinking game?", "a": "Yes. Finding secret ingredients, adjusting jukebox music, and talking to patrons grants bonus coins, reveals opponent tells, and unlocks exclusive ending branches."}
    ],
    "content": """
Between the heart-pounding duels of shot-glass Russian roulette, **Drunken Goddess Reflux** shifts gears into a rich, immersive 3D adventure. Players are granted free rein to explore **Pandemonium**, Hell's premier speakeasy designed by 3D environmental artists tiri and temi, with art direction by amebiyori. Far from a simple waiting room, Pandemonium is packed with interactive secrets, atmospheric storytelling, hidden cocktail ingredients, and NPC interactions that directly impact your survival odds.

This guide provides a comprehensive walkthrough of every secret room, lore document, interactive prop, and puzzle waiting within the neon-lit confines of Pandemonium.

---

## Map of Pandemonium: Key Exploration Zones

Pandemonium consists of five interconnected exploration sectors:

```
+--------------------------------------------------------+
|                      VIP BOOTH                         |
|  [Femme Soule's Diary]               [Red Velvet Sofa] |
+-----------+--------------------------------+-----------+
|           |                                |           |
| RESTROOM  |         MAIN BAR COUNTER       | CELLAR    |
| [Mirror]  |   [Ashen Bartender] [Shaker]   | [Padlock] |
|           |                                |           |
+-----------+--------------------------------+-----------+
|                      LOUNGE & JUKEBOX                  |
|  [Neon Jukebox]           [Lost Soul NPC]   [Phone]    |
+--------------------------------------------------------+
```

1. **The Main Bar Counter**: Where the duels take place. During intermission, you can inspect the glassware, grab unused lime wedges, and speak to the Ashen Bartender.
2. **The Lounge & Jukebox**: A retro-futuristic seating area featuring the jukebox, neon cocktail signs, and wandering patron souls.
3. **The VIP Booth**: A secluded booth lined with deep red velvet where Femme Soule lounges when not dueling. Contains personal letters and lore diaries.
4. **The Restroom**: A grimy, flickering neon bathroom with a cracked mirror that reveals UV hidden codes under blacklight.
5. **The Cellar Storeroom**: A padlocked metal door beneath the stairs leading to rare spirits and contraband items.

To see how items found here tie into recipes, consult [Secret Cocktail Recipes and Mixology](/drinks/drunken-goddess-reflux-cocktail-recipes-mixology).

---

## The Cellar Padlock Puzzle: Unlocking Holy Water

The single most valuable secret in Pandemonium is the smuggled bottle of **Holy Water Contraband**. To obtain it, you must crack the 4-digit combination padlock on the cellar door.

### Step-by-Step Padlock Solution:
1. During Intermission 1, enter the **Restroom**.
2. Turn off the overhead light switch near the door. The room will plunge into darkness, revealing fluorescent graffiti on the mirror.
3. The mirror reveals a cryptic phrase: *"Four years before the fall, two shots after midnight."*
4. Inspect the vintage calendar hanging near the phone booth in the lounge: the calendar year is marked **1994**.
5. The padlock combination is **1-9-9-6** (1994 + 2).
6. Return to the cellar door, enter `1996`, and retrieve the Holy Water Contraband from the wooden crate.

Consuming or weaponizing Holy Water dramatically shifts the late-game balance, as detailed in our [Holy Water Contraband Guide](/drinks/drunken-goddess-reflux-holy-water-contraband).

---

## Dialogue Trees with The Ashen Bartender

The Ashen Bartender is an enigmatic skeleton in a tailored crimson vest. Speaking with him across multiple intermissions unlocks crucial gameplay bonuses:

- **First Conversation (Intermission 1)**: Inquire about Femme Soule's history. He warns you about her *Triple Pain* card and gifts you 15 Skull Coins.
- **Second Conversation (Intermission 2)**: Ask about drink preparation. He explains the viscosity differences between gin and absinthe, adding physical hint markers to your inspection HUD.
- **Third Conversation (Intermission 3)**: If you possess the four hidden Bartender Logs found scattered across the bar, he offers you his cocktail shaker, initiating the path toward the [Hell Bartender Secret Ending](/endings/drunken-goddess-reflux-hell-bartender-ending).

---

## Discarded Napkins: Lore Notes by Fuyuki Hayashi

Scattered throughout Pandemonium are five discarded bar napkins inscribed with handwritten notes from director Fuyuki Hayashi. Finding all five awards the "Barfly Historian" Steam achievement:

| Napkin Location | Title / Subject | Lore Revelation |
| :--- | :--- | :--- |
| **Lounge Table 3** | "To Whoever Enters" | Explains that Pandemonium exists in the threshold between life and eternal purgatory. |
| **VIP Booth Cushion** | "Femme's Note" | Reveals Femme Soule was once a mortal mixologist who made a pact with an underworld deity. |
| **Jukebox Coin Slot** | "Aiobahn's Track Notes" | Discusses the recording of *DEMON'S SHOT* and hidden frequencies in Hell. |
| **Cellar Wine Rack** | "Recipe #07" | Contains the exact proportions needed for the legendary *Pandemonium Mule*. |
| **Restroom Sink** | "Smudged Warning" | Cautions players never to drink the blue glowing liquor without holding the Ice Pick. |

---

## Interactive Easter Eggs: The Neon Jukebox

The Jukebox in the lounge is fully functional. Beyond changing the ambient background music to tracks composed by Aiobahn +81, entering specific track combinations unlocks secret bonuses:
- **Track 07 -> Track 03 -> Track 11**: Plays a chip-tune remix of *Yunyun Syndrome!?* and dispenses 50 free Skull Coins into the coin return tray.
- **Track 01 -> Track 01 -> Track 06**: Triggers special dance animations from Femme Soule in the VIP booth.

Check all soundtrack details in our [OST and DEMON'S SHOT Guide](/codes/drunken-goddess-reflux-ost-demons-shot-tracklist).

---

## Pro Tip: Reusable Lime Wedges

On the corner of the bar counter sits a small wooden cutting board with fresh lime wedges. Interacting with the cutting board before each round allows you to pocket one lime slice. In the middle of a duel, pressing `Tab` bites into the lime, instantly steadying your cursor aim for 10 seconds without any negative side effects.

---

## Related Guides & Next Steps

Uncover more of Pandemonium's mysteries:
- Check our core survival tactics in [Beginner Guide](/guide/drunken-goddess-reflux-beginner-guide).
- Learn how to mix custom drinks in [Cocktail Recipes and Mixology](/drinks/drunken-goddess-reflux-cocktail-recipes-mixology).
- Discover how to take over the bar in [Hell Bartender Ending](/endings/drunken-goddess-reflux-hell-bartender-ending).
- Find all secret redemption codes in [Drunken Goddess Reflux Codes and Passwords](/codes/drunken-goddess-reflux-codes-and-passwords).
"""
}

# 6. Survival Strategies
guides["drunken-goddess-reflux-survival-strategies"] = {
    "title": "Drunken Goddess Reflux Survival Strategies: Advanced Play",
    "description": "Advanced strategies for surviving high-proof rounds, baiting demon moves, managing soul stability, and securing late-game victories.",
    "hub": "guide",
    "slug": "drunken-goddess-reflux-survival-strategies",
    "quickGuide": [
        "Track the cumulative proof pool to calculate exact mathematical odds on every turn.",
        "Force Femme Soule to drink high-proof shots during her Phase 2 transition window.",
        "Maintain a dedicated card economy: never enter Round 3 without at least two swap cards.",
        "Manage Soul Stability across rounds to prevent sudden death during Ice Pick emergencies.",
        "Leverage sensory degradation by using tactile audio cues over distorted visual markers."
    ],
    "faq": [
        {"q": "What is the best late-game strategy against Femme Soule?", "a": "The best late-game strategy is 'Bait and Punish': conserve two Sleight of Hand cards, bait Femme Soule into activating her Triple Pain card, and swap the lethal Spiritum glass onto her side of the table for an immediate one-shot victory."},
        {"q": "How can you tell how many high-proof shots remain on the counter?", "a": "By counting glasses. In Round 3, there are exactly 3 high-proof shots (70-75%) and 1 lethal Spiritum (96%) out of 8 total glasses. Tracking eliminated drinks reveals the exact danger ratio."},
        {"q": "Is it ever beneficial to drink a high-proof shot on purpose?", "a": "Only if your intoxication is low (<40%) and doing so guarantees that the remaining glasses on the board are lethal traps for Femme Soule on her upcoming turn."}
    ],
    "content": """
While casual players may treat **Drunken Goddess Reflux** as a game of random luck, experienced barflies know that survival in Pandemonium is governed by cold mathematics, card advantage, risk hedging, and psychological manipulation. To reliably overcome Femme Soule on higher difficulty settings and achieve flawless runs, you must adopt an analytical mindset.

This advanced survival guide outlines competitive card-counting techniques, gauge threshold mathematics, card economy management, and late-game execution strategies designed to guarantee victory.

---

## Probability Tracking: The Card-Counting Methodology

Every round draws from a known distribution of glasses. Treating the table as a closed probability system allows you to quantify your exact risk on any given pick:

### Round 3 Probability Matrix (8 Glasses Total)
- **1x Safe Shot**: Void Tonic (0% ABV) -> 12.5% starting odds
- **3x Medium Shots**: Blood Wine / Purgatory Gin (40-50% ABV) -> 37.5% starting odds
- **3x Heavy Shots**: Brimstone Absinthe / Infernal Mezcal (70-75% ABV) -> 37.5% starting odds
- **1x Lethal Shot**: Spiritum (96% ABV) -> 12.5% starting odds

```
Turn 1: 8 Glasses -> Danger Ratio: 50.0% (4 hazardous / 8 total)
Turn 2 (after 2 safe/med removed): 6 Glasses -> Danger Ratio: 66.7% (4 hazardous / 6 total)
Turn 3 (after 3 safe/med removed): 5 Glasses -> Danger Ratio: 80.0% (4 hazardous / 5 total)
```

Once the danger ratio crosses **60%**, drinking directly from the counter without trick cards is statistical suicide. At this point, your turns must rely on *Sleight of Hand*, *Napkin Spit*, or forcing Femme Soule to pick first.

Compare all beverage statistics in our [All Drinks and Proof Catalog](/drinks/drunken-goddess-reflux-all-drinks-proof-catalog).

---

## Card Economy: The Two-Card Rule for Round 3

Player trick cards are earned by accumulating intoxication (1 card drawn per 20% gauge gained) or bought from the bartender with Skull Coins. A common beginner error is burning cards in Rounds 1 and 2 to avoid mild 30% drinks.

**The Golden Rule of Card Economy**: Never enter Round 3 without at least:
1. **One Glass Swap Card (Sleight of Hand or Shell Game)**: Mandatory for redirecting Spiritum.
2. **One Defensive Mitigation Card (Napkin Spit or Cold Rinse)**: Mandatory if forced to drink under Femme Soule's *Triple Pain* modifier.

If your hand is empty entering Round 3, spend your intermission exploring Pandemonium and trading with the Ashen Bartender to replenish your stock, as described in [Pandemonium Bar Secrets](/guide/drunken-goddess-reflux-pandemonium-bar-secrets).

---

## Threshold Management: Riding the 65% Sweet Spot

The ideal operational state in Drunken Goddess Reflux is maintaining your Intoxication Gauge between **60% and 75%**:

| Intoxication State | Benefits | Drawbacks | Tactical Verdict |
| :--- | :--- | :--- | :--- |
| **0% – 35% (Too Sober)** | Crystal clear vision, zero tremor | No trick card access; slow play | Inefficient |
| **60% – 75% (The Sweet Spot)** | Tier 1 & 2 cards active; visual tells enhanced | Moderate screen wobble | **OPTIMAL** |
| **85% – 99% (Danger Zone)** | Maximum trick card slots open | Severe tunnel vision; 1-shot death | Emergency Only |

By hovering around 65%, you possess enough intoxication to cast powerful deception spells while retaining enough buffer to absorb an unexpected 25% shot without exceeding the 100% reflux threshold.

For detailed gauge mathematics, review the [Intoxication and Ice Pick Guide](/guide/drunken-goddess-reflux-intoxication-ice-pick-guide).

---

## The "Bait and Punish" Endgame Protocol

The cleanest, most reliable way to finish Femme Soule in Round 3 is the **Bait and Punish** maneuver:

```
Step 1: Identify Spiritum -> Observe blue vapor and zero-meniscus flat rim.
Step 2: Leave Spiritum on Table -> Do not drink or touch it.
Step 3: Wait for Demon Aggression -> Femme Soule will activate 'Triple Pain' when her gauge is >60%.
Step 4: Execute Sleight of Hand -> Swap the glass in front of her with Spiritum.
Step 5: Confirm Checkmate -> Femme Soule drinks 96% x 3 = 288% damage. Instant soul reflux!
```

This strategy completely bypasses her phase 3 frenzy and secures an immediate victory while keeping your soul stability completely intact.

Learn more about her behavioral triggers in the [Femme Soule Boss Guide](/guide/drunken-goddess-reflux-femme-soule-boss-guide).

---

## Pro Tip: Audio Rhythms over Distorted Visuals

When your character enters Stage 4 drunkenness (85%+), visual post-processing effects intentionally blur the glass rims, making visual inspection nearly impossible. However, the **audio feedback** remains crisp: tapping a glass with your finger (`Q` key) emits a musical pitch. High-proof alcohol vibrates with a distinctly higher, tinny pitch than low-proof liquid. Train your ear to listen for the pitch when your eyes can no longer be trusted.

---

## Related Guides & Next Steps

Elevate your play to the highest level:
- Read the complete breakdown of rules in [Russian Roulette Mechanics](/guide/drunken-goddess-reflux-russian-roulette-mechanics).
- Study the lethal potential of the 96% shot in [Spiritum Shot Guide](/drinks/drunken-goddess-reflux-spiritum-lethal-shot-guide).
- Unlock the ultimate narrative outcome with our [True Ending Walkthrough](/endings/drunken-goddess-reflux-true-ending-freedom).
- Check the full achievement roadmap in [Steam Achievements Guide](/codes/drunken-goddess-reflux-steam-achievements-guide).
"""
}

# 7. Drunken Tricks Guide
guides["drunken-goddess-reflux-drunken-tricks-guide"] = {
    "title": "Drunken Goddess Reflux Drunken Tricks and Deception Cards",
    "description": "Unlock and execute all drunken tricks and deception cards in Drunken Goddess Reflux, from glass swapping to multiplier bluffing.",
    "hub": "guide",
    "slug": "drunken-goddess-reflux-drunken-tricks-guide",
    "quickGuide": [
        "Drunken Tricks unlock progressively at 30%, 60%, and 85% Intoxication thresholds.",
        "Cards cost Intoxication or Skull Coins to play and drastically alter table dynamics.",
        "Sleight of Hand allows silent glass swapping between any two positions on the counter.",
        "Napkin Spit reduces incoming drink intoxication by 50% when timed correctly.",
        "Femme Soule can counter player tricks if your character hesitates during card activation."
    ],
    "faq": [
        {"q": "What are Drunken Tricks in Drunken Goddess Reflux?", "a": "Drunken Tricks are rule-breaking deception cards that unlock as your character becomes intoxicated. They allow you to swap glasses, fake drinking, force toasts, and read liquid properties."},
        {"q": "How do you get more Drunken Trick cards?", "a": "You automatically draw one card every time your Intoxication crosses a 20% milestone. You can also purchase bonus cards from the Ashen Bartender during intermissions using Skull Coins."},
        {"q": "Can Femme Soule steal your trick cards?", "a": "Yes. If Femme Soule plays her 'Demon's Grasp' card during Phase 3, she randomly discards or steals one card from your hand unless countered immediately."}
    ],
    "content": """
In the supernatural tavern of Pandemonium, honesty is a straight road to damnation. To outdrink a demon who controls the laws of Hell, players must embrace their inner barfly and master **Drunken Tricks**—a tactical card-based system representing sleight-of-hand, bluffs, bar tricks, and brazen rule violations that only an experienced drunkard could pull off.

This guide provides a comprehensive encyclopedia of every Drunken Trick card in Drunken Goddess Reflux, including unlock thresholds, costs, mechanical synergies, and counter-tactics against Femme Soule.

---

## How Drunken Tricks Work: The Card Mechanic

As your Intoxication Gauge climbs, your mortal inhibitions fall away, unlocking creative ways to bend the duel rules. The card system is governed by three core rules:

1. **Milestone Draws**: Crossing 20%, 40%, 60%, and 80% Intoxication automatically draws one card into your active hand (maximum hand size: 4 cards).
2. **Resource Costs**: Playing a card typically consumes a small amount of Intoxication (acting as a temporary sobriety cost) or burns Skull Coins earned through exploration.
3. **Turn Window**: Cards can be played at the beginning of your turn before touching a glass, or as reactions when Femme Soule declares an action.

Mastering this flow is essential for executing the strategies found in our [Beginner Guide](/guide/drunken-goddess-reflux-beginner-guide) and [Survival Strategies](/guide/drunken-goddess-reflux-survival-strategies).

---

## Tier 1 Tricks: Buzzed Deceptions (Unlocked at 30% Intoxication)

Low-tier tricks focus on information gathering and minor positional manipulation:

### 1. Sleight of Hand (Cost: 5 Skull Coins)
- **Effect**: Instantly swap the positions of any two adjacent glasses on the bar counter while Femme Soule blinks.
- **Synergy**: Swap a suspected lethal shot directly into Femme Soule's designated drinking zone.
- **Risk**: If Femme Soule is in Phase 2 or 3, there is a 20% chance she catches your hand, disabling the card.

### 2. The Sniff Test (Cost: 5% Intoxication)
- **Effect**: Lean forward and smell a target glass. Reveals whether the drink is above or below 50% ABV.
- **Synergy**: Invaluable in Round 2 when differentiating between Purgatory Gin (40%) and Brimstone Absinthe (75%).

### 3. The Napkin Spit (Cost: 10 Skull Coins)
- **Effect**: If you must drink an unknown shot, holding right-click as the glass touches your lips spits half the liquid into your linen napkin, cutting incoming intoxication by 50%.
- **Synergy**: The premier defensive card for absorbing unexpected high-proof traps.

---

## Tier 2 Tricks: Wasted Mastery (Unlocked at 60% Intoxication)

Mid-tier tricks introduce heavy offensive disruption and turn manipulation:

```
+-------------------------------------------------------------+
|                 TIER 2 DRUNKEN TRICK CARDS                  |
+---------------------+-------------------+-------------------+
| CARD NAME           | RESOURCE COST     | TACTICAL EFFECT   |
+---------------------+-------------------+-------------------+
| Shell Game          | 10 Skull Coins    | Shuffles 3 glasses|
| The Devil's Toast   | 10% Intoxication  | Forces Demon Drink|
| False Pass          | 15 Skull Coins    | Skips Player Turn |
| Ice Cube Drop       | 1 Focus Token     | Dilutes Glass -20%|
+---------------------+-------------------+-------------------+
```

### The Devil's Toast (Cost: 10% Intoxication)
You stand up and declare an aggressive toast. Femme Soule's demonic pride compels her to accept: she must immediately pick and drink a glass on your turn. If played when only high-proof glasses remain, this card forces an unavoidable damage spike on the demon.

See how this pairs with the [Femme Soule Boss Guide](/guide/drunken-goddess-reflux-femme-soule-boss-guide).

---

## Tier 3 Tricks: Delirium Powers (Unlocked at 85% Intoxication)

High-tier tricks represent sheer drunken desperation, capable of turning certain defeat into miraculous victory:

### 1. The Mirror Swap (Cost: 20 Skull Coins + 10% Intoxication)
- **Effect**: Reverses the entire glass order across the counter. The glass closest to you moves to Femme Soule, and vice-versa.
- **Tactical Value**: Checkmate maneuver when Femme Soule sets up a trap on your side of the table.

### 2. Deadpan Bluff (Cost: 15% Intoxication)
- **Effect**: Down any glass regardless of proof while displaying zero physical reaction. Stuns Femme Soule for two turns as she questions your mortal limits.
- **Risk**: You still take the full intoxication damage, meaning this must be followed by an [Ice Pick Reset](/guide/drunken-goddess-reflux-intoxication-ice-pick-guide) if you exceed 99%.

---

## Priority and Comparison Table: All Player Cards

| Card Name | Tier | Cost | Primary Use | Counterability |
| :--- | :--- | :--- | :--- | :--- |
| **Sleight of Hand** | 1 | 5 Coins | Repositioning | Low |
| **Napkin Spit** | 1 | 10 Coins | Defense / Damage Halving | Very Low |
| **The Sniff Test** | 1 | 5% Gauge | Information Gathering | Zero |
| **The Devil's Toast** | 2 | 10% Gauge | Offensive Force Drink | Moderate |
| **Shell Game** | 2 | 10 Coins | Randomizing Traps | Low |
| **Mirror Swap** | 3 | 20 Coins | Table Reversal | High |
| **Deadpan Bluff** | 3 | 15% Gauge | Turn Stun Lock | Zero |

---

## Pro Tip: Card Chaining Combo

The most devastating combo in Drunken Goddess Reflux is the **"Toast into Mirror"** chain:
1. Play *The Devil's Toast* to lock Femme Soule into drinking.
2. Before she picks, immediately trigger *Mirror Swap* to slide the newly identified [Spiritum Shot](/drinks/drunken-goddess-reflux-spiritum-lethal-shot-guide) into her selection slot.
3. This guarantees a minimum 96% Intoxication surge on the demon, usually triggering the victory reflux cutscene on the spot.

---

## Related Guides & Next Steps

Expand your tactical repertoire:
- Learn the basics in our [Beginner Guide](/guide/drunken-goddess-reflux-beginner-guide).
- Study all beverage proofs in the [Drink Tier List](/drinks/drunken-goddess-reflux-drink-tier-list).
- Review all ending routes in [All Endings Guide](/endings/drunken-goddess-reflux-all-endings-guide).
- Check secret bar codes in [Codes and Passwords](/codes/drunken-goddess-reflux-codes-and-passwords).
"""
}

# Write all 7 guides
for slug, data in guides.items():
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

print(f"Successfully generated all {len(guides)} guides for 'guide' hub.")
