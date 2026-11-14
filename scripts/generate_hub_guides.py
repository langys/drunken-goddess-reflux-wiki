#!/usr/bin/env python3
"""Generate the 7 guides for the 'guide' hub in content/en/."""

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

# Write out first 2 guides
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
    print(f"Wrote {slug}.md")
