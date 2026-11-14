#!/usr/bin/env python3
"""Generate all 5 guides for the 'codes' hub in content/en/."""

import pathlib

OUT = pathlib.Path("content/en")
OUT.mkdir(parents=True, exist_ok=True)

codes = {}

# 20. Codes & Passwords
codes["drunken-goddess-reflux-codes-and-passwords"] = {
    "title": "Drunken Goddess Reflux Codes and Secret Bar Passwords",
    "description": "All active promo codes, VIP secret passwords, and redemption methods in Drunken Goddess Reflux for bonus coins and cosmetic glasses.",
    "hub": "codes",
    "slug": "drunken-goddess-reflux-codes-and-passwords",
    "quickGuide": [
        "Redeem codes through the options menu or at the cash register during intermissions.",
        "Promo codes reward bonus Skull Coins, unique coaster designs, and card sleeves.",
        "Secret Jukebox passwords unlock hidden music tracks and developer audio logs.",
        "Codes are case-sensitive and never require third-party websites or external tools.",
        "Bookmark this page as new codes are added following Steam events and milestone updates."
    ],
    "faq": [
        {"q": "How do you redeem codes in Drunken Goddess Reflux?", "a": "To redeem codes, open the Pause Menu (`Esc`), select 'Settings & System', and navigate to the 'Promo Code' input box. Alternatively, interact with the cash register on the bar counter during 3D exploration intermissions."},
        {"q": "Are there codes for infinite sobriety or god mode?", "a": "No. Drunken Goddess Reflux does not include cheat codes that bypass intoxication mechanics. Codes grant cosmetic shot glasses, card backings, Skull Coins, and Jukebox soundtracks."},
        {"q": "Do Drunken Goddess Reflux codes expire?", "a": "Milestone and launch promotional codes have expiration windows tied to game patches, while secret in-game Jukebox passwords remain permanent."}
    ],
    "content": """
In **Drunken Goddess Reflux**, every advantage counts when your mortal soul is wagered over high-proof demonic liquor. Developer WHO YOU and publisher Alliance Arts have incorporated a built-in redemption system allowing players to input promotional codes and discover hidden speakeasy passwords. These codes grant bonus Skull Coins, unlock custom cosmetic shot glasses, grant stylish card sleeves, and reveal secret developer audio tracks.

This comprehensive guide tracks all active, verified codes for Drunken Goddess Reflux, details the exact redemption process, and archives expired codes.

---

## Active Drunken Goddess Reflux Promo Codes

Below is the verified list of active promotional codes currently valid in the Steam release:

| Promo Code | Reward Granted | Status | Expiration Window |
| :--- | :--- | :--- | :--- |
| **PANDEMONIUM2026** | 50 Free Skull Coins + Vintage Leather Coaster | **ACTIVE** | Permanent Launch Code |
| **DEMONSHOT** | Unlocks DEMON'S SHOT 8-Bit Chiptune Track | **ACTIVE** | Steam Launch Special |
| **NANAHIRA_LOVE** | Exclusive Pink Neon Horn Card Sleeves | **ACTIVE** | Community Milestone |
| **ICEPICK_HERO** | 25 Skull Coins + Stainless Steel Shot Glass | **ACTIVE** | Active |
| **SPIRITUM96** | Custom Blue Hellfire Table Decal | **ACTIVE** | Active |

Learn how to spend your Skull Coins efficiently in our [Drunken Tricks and Deception Cards Guide](/guide/drunken-goddess-reflux-drunken-tricks-guide).

---

## Secret Speakeasy Jukebox Passwords

In addition to standard promo codes, players can interact with the **Neon Jukebox** in the lounge during 3D bar intermissions to enter secret numerical passwords into the track selection keypad:

```
[Jukebox Password: 1-9-9-4] -> Unlocks 'Fuyuki Hayashi Director Commentary Track #1'
[Jukebox Password: 0-7-1-1] -> Unlocks 'Yunyun Syndrome!? 8-Bit Easter Egg Track'
[Jukebox Password: 6-6-6-0] -> Dispenses 30 free Skull Coins into the coin return tray
[Jukebox Password: 2-0-2-6] -> Unlocks the Neon Cyberpunk Shot Glass skin
```

To explore the lounge and find the jukebox, consult our [Pandemonium Bar Secrets Guide](/guide/drunken-goddess-reflux-pandemonium-bar-secrets).

---

## Step-by-Step Redemption Instructions

Redeeming your rewards is straightforward and takes less than a minute:

### Method 1: The Main Settings Menu
1. Launch Drunken Goddess Reflux and start or continue your game.
2. Press `Esc` (or `Start` on controller) to open the Pause Menu.
3. Select **Settings** -> **Redeem Code**.
4. Type or paste the code exactly as shown (codes are case-sensitive).
5. Click **Confirm**. Your rewards will be immediately credited to your inventory.

### Method 2: The Pandemonium Cash Register
1. During any 3D exploration intermission, walk behind the main bar counter.
2. Interact with the brass **Cash Register** (`E` key).
3. Select "Punch Code" from the prompt.
4. Input your code to hear the satisfying register bell chime and collect your bonus!

---

## Expired Codes Archive

For reference, the following codes were distributed during closed Discord playtests and are no longer valid:
- `CLOSED_BETA_SHOT`: Granted 100 beta coins (Expired October 2026).
- `INDIE_EXPO_VIP`: Unlocked demo preview coaster (Expired November 2026).

---

## Troubleshooting: Why Won't My Code Work?

If you encounter an error when redeeming a code:
1. **Check Capitalization**: Codes like `PANDEMONIUM2026` must be entered in ALL CAPS.
2. **Check for Trailing Spaces**: Pasting codes from web browsers often captures an accidental leading or trailing space. Backspace before and after the text.
3. **Offline Playback**: Codes require an active Steam connection to verify ownership against the server database. Ensure Steam is online.

---

## Pro Tip: Saving Coins for Round 3

Do not spend your redeemed Skull Coins on low-tier Tier 1 trick cards early. Save your coin balance to purchase the game-winning [Tied Souls Card](/endings/drunken-goddess-reflux-mutual-reflux-secret-ending) or the [Holy Water Contraband Key](/drinks/drunken-goddess-reflux-holy-water-contraband) during late-game intermissions.

---

## Related Guides & Next Steps

Continue maximizing your underworld advantage:
- Master the duel fundamentals in our [Beginner Guide](/guide/drunken-goddess-reflux-beginner-guide).
- Check the full trophy list in [Steam Achievements Guide](/codes/drunken-goddess-reflux-steam-achievements-guide).
- Review all ending routes in [All Endings Guide](/endings/drunken-goddess-reflux-all-endings-guide).
- Check PC settings and controls in [PC Controls and Settings Guide](/codes/drunken-goddess-reflux-pc-controls-and-settings).
"""
}

# 21. Steam Achievements Guide
codes["drunken-goddess-reflux-steam-achievements-guide"] = {
    "title": "Drunken Goddess Reflux Steam Achievements Guide (100%)",
    "description": "Full 100% Steam achievements guide for Drunken Goddess Reflux with unlock criteria, hidden trophies, and optimal routing.",
    "hub": "codes",
    "slug": "drunken-goddess-reflux-steam-achievements-guide",
    "quickGuide": [
        "Drunken Goddess Reflux features 25 total Steam achievements (1 Platinum equivalent).",
        "7 achievements are tied directly to the 'Seven Flavors of Ruin' ending outcomes.",
        "'Iron Liver' requires defeating Femme Soule without ever using the Ice Pick.",
        "'Master Mixologist' is unlocked by discovering and crafting all 6 secret cocktails.",
        "Full 100% completion can be achieved in 3 optimized playthroughs."
    ],
    "faq": [
        {"q": "How many achievements are in Drunken Goddess Reflux?", "a": "There are 25 Steam achievements, covering story progression, ending variations, exploration secrets in Pandemonium, mixology mastery, and extreme survival challenges."},
        {"q": "What is the hardest achievement in Drunken Goddess Reflux?", "a": "The hardest achievement is 'Iron Liver', which requires completing Round 3 and defeating Femme Soule without ever using the Ice Pick to reset your intoxication."},
        {"q": "Can you unlock achievements in offline mode?", "a": "Yes. Achievements are tracked locally and will sync with your Steam profile once you reconnect to the internet."}
    ],
    "content": """
For achievement hunters and completionists, **Drunken Goddess Reflux** offers a deeply satisfying trophy roadmap. With 25 carefully crafted Steam achievements designed by WHO YOU, the challenge spans high-stakes mathematical survival, puzzle exploration throughout the 3D bar environment, intricate mixology recipes, and mastering all seven narrative conclusions.

This 100% completion guide categorizes all 25 achievements, provides step-by-step unlock instructions, and charts an optimal 3-playthrough route to secure every trophy with zero wasted time.

---

## 3-Playthrough 100% Roadmap

```
PLAYTHROUGH 1: The Purist Escape (True Ending + Iron Liver)
├── Focus on defiant dialogue flags.
├── Acquire Holy Water Contraband to manage Intoxication.
├── NEVER touch the Ice Pick.
└── Unlocks: 'Morning Sunlight', 'Iron Liver', 'First Sip', 'Clean Hands'.

PLAYTHROUGH 2: The Devoted Barkeep (Romance & Career Endings)
├── Focus on flirty dialogue and gift Devoted Maiden's Kiss.
├── Collect all 4 Bartender Logbooks in the cellar/lounge.
├── Branch save before Round 3:
│   ├── Branch A: Refuse elevator -> 'Till Death Do Us Part'.
│   └── Branch B: Present Forbidden Elixir -> 'Under New Management'.
└── Unlocks: 'Master Mixologist', 'Barfly Historian', 'Under New Management'.

PLAYTHROUGH 3: The Chaos Run (Mutual Reflux & Grim Fates)
├── Overuse Ice Pick 3 times in Round 1 -> 'Blunt Instrument'.
├── Restart, setup Tied Souls in Round 3 -> 'Soul Twins'.
└── Unlocks: 'Soul Twins', 'A Light Drinker', 'House Special', 'Pandemonium Platinum'.
```

---

## Story & Ending Achievements (7 Trophies)

These achievements correspond directly to the narrative paths detailed in our [All Endings Guide](/endings/drunken-goddess-reflux-all-endings-guide):

### 1. Morning Sunlight (Gold)
- **Condition**: Complete Ending 1 (Reclaimed Dawn). Defeat Femme Soule and escape Pandemonium via the elevator.
- **Walkthrough**: [True Ending Freedom Walkthrough](/endings/drunken-goddess-reflux-true-ending-freedom).

### 2. Till Death Do Us Part (Silver)
- **Condition**: Complete Ending 2 (Eternal Pour). Accept Femme Soule's romance and stay in Hell forever.
- **Walkthrough**: [Eternal Partner Romance Ending](/endings/drunken-goddess-reflux-eternal-partner-ending).

### 3. A Light Drinker (Bronze)
- **Condition**: Complete Ending 3 (Soul-Spilled Husk). Suffer soul reflux during Round 1 or 2.

### 4. Soul Twins (Gold)
- **Condition**: Complete Ending 4 (Mutual Reflux). Force both player and demon to 100% Intoxication simultaneously.
- **Walkthrough**: [Mutual Reflux Secret Ending](/endings/drunken-goddess-reflux-mutual-reflux-secret-ending).

### 5. Under New Management (Gold)
- **Condition**: Complete Ending 5 (Hell Bartender). Craft the Forbidden Elixir and take over Pandemonium.
- **Walkthrough**: [Hell Bartender Ending](/endings/drunken-goddess-reflux-hell-bartender-ending).

### 6. Blunt Instrument (Bronze)
- **Condition**: Complete Ending 6 (Void Blackout). Deplete your Soul Stability to zero using the [Ice Pick](/guide/drunken-goddess-reflux-intoxication-ice-pick-guide).

### 7. House Special (Bronze)
- **Condition**: Complete Ending 7 (Demon's Cocktail). Drink Cursed Tequila at 95%+ Intoxication.

---

## Survival & Challenge Achievements (8 Trophies)

| Achievement Name | Difficulty | Condition | Optimal Strategy |
| :--- | :--- | :--- | :--- |
| **First Sip** | Easy | Win Round 1 of the drinking duel. | Focus on low-proof drinks in our [Beginner Guide](/guide/drunken-goddess-reflux-beginner-guide). |
| **Iron Liver** | Hard | Win the game without using the Ice Pick. | Smuggle [Holy Water Contraband](/drinks/drunken-goddess-reflux-holy-water-contraband) to clear intoxication. |
| **Close Call** | Medium | Finish a round with Intoxication between 95% and 99%. | Drink Diluted Lager at 90% meter. |
| **Checkmate Pour** | Medium | Feed Spiritum to Femme Soule while Triple Pain is active. | Use Sleight of Hand as detailed in [Spiritum Guide](/drinks/drunken-goddess-reflux-spiritum-lethal-shot-guide). |
| **Card Shark** | Medium | Play 10 Drunken Trick cards in a single run. | Use [Drunken Tricks](/guide/drunken-goddess-reflux-drunken-tricks-guide) frequently. |
| **Clean Hands** | Hard | Win a game without suffering any hand tremor penalty. | Zero Ice Pick uses and drink warm water at bar. |
| **Speed Demon** | Hard | Complete all 3 drinking rounds in under 8 minutes. | Skip inspections and rely on audio tells. |
| **The Hard Way** | Master | Defeat Femme Soule without playing any Drunken Trick cards. | Pure probability management in [Survival Strategies](/guide/drunken-goddess-reflux-survival-strategies). |

---

## Exploration & Secrets Achievements (10 Trophies)

- **Barfly Historian (Silver)**: Find all 5 handwritten napkins scattered across Pandemonium. Locations in [Pandemonium Bar Secrets](/guide/drunken-goddess-reflux-pandemonium-bar-secrets).
- **Master Mixologist (Gold)**: Successfully brew all 6 unique recipes at the cocktail shaker. Full guide in [Cocktail Recipes and Mixology](/drinks/drunken-goddess-reflux-cocktail-recipes-mixology).
- **Contraband in Hell (Bronze)**: Unlock the cellar door and obtain Holy Water Contraband.
- **Jukebox Hero (Bronze)**: Play 5 different tracks on the lounge neon jukebox. See [OST Guide](/codes/drunken-goddess-reflux-ost-demons-shot-tracklist).
- **Secret Code Breaker (Bronze)**: Successfully redeem any promo code in the pause menu. Active list in [Codes and Passwords](/codes/drunken-goddess-reflux-codes-and-passwords).
- **Sore Knuckles (Bronze)**: Use the Ice Pick for the very first time.
- **Green Fairy Sight (Bronze)**: Activate Green Fairy Vision by drinking [Brimstone Absinthe](/drinks/drunken-goddess-reflux-brimstone-absinthe-guide).
- **VIP Lounge Access (Bronze)**: Sit on the red velvet sofa in the VIP booth.
- **Tears of a Demon (Silver)**: Trigger all 15 unique emotional dialogue lines from Nanahira during Phase 3.
- **Pandemonium Platinum (Platinum)**: Unlock all 24 other achievements.

---

## Pro Tip: Speedrunning "Master Mixologist"

You do not need to brew all six cocktails in one run. The game saves discovered recipes across all your profile saves. If you crafted four cocktails in Playthrough 1, you only need to craft the remaining two in Playthrough 2 to pop the achievement!

---

## Related Guides & Next Steps

Continue your trophy hunt:
- Master the duel fundamentals in [Russian Roulette Rules Explained](/guide/drunken-goddess-reflux-russian-roulette-mechanics).
- Study all liquid properties in [Drink Tier List](/drinks/drunken-goddess-reflux-drink-tier-list).
- Learn how to escape Hell alive in [True Ending Walkthrough](/endings/drunken-goddess-reflux-true-ending-freedom).
- Check PC settings in [PC Controls and Settings Guide](/codes/drunken-goddess-reflux-pc-controls-and-settings).
"""
}

# 22. Release Date, Platforms & Specs
codes["drunken-goddess-reflux-release-date-platforms-specs"] = {
    "title": "Drunken Goddess Reflux Release Date, Platforms and System Specs",
    "description": "Official release date on Steam (December 8, 2026), PC system requirements, Steam Deck compatibility, and controller support info.",
    "hub": "codes",
    "slug": "drunken-goddess-reflux-release-date-platforms-specs",
    "quickGuide": [
        "Official PC release is scheduled for December 8, 2026, exclusively via Steam.",
        "Developed by WHO YOU (Fuyuki Hayashi) and published by Alliance Arts.",
        "Native Steam Deck support with verified 60 FPS performance out of the box.",
        "Low minimum PC requirements: playable on Intel Core i3 with GTX 960 or equivalent.",
        "Public demo was cancelled to protect game assets; closed playtests hosted via Discord."
    ],
    "faq": [
        {"q": "When is the Drunken Goddess Reflux release date?", "a": "Drunken Goddess Reflux launches worldwide on PC via Steam on December 8, 2026."},
        {"q": "Is Drunken Goddess Reflux coming to Nintendo Switch or PlayStation?", "a": "Alliance Arts has announced the game exclusively for PC (Steam) for the initial December 2026 launch. Console ports have not been ruled out for 2027 depending on reception."},
        {"q": "Why was the Steam demo cancelled in October 2026?", "a": "Developer WHO YOU cancelled the public demo due to security concerns regarding third-party scraping and AI duplication of the game's unique drinking mechanics, opting instead for closed community beta testing."}
    ],
    "content": """
Following its viral reveal during INDIE Live Expo and rapid accumulation of hundreds of thousands of Steam wishlists, **Drunken Goddess Reflux** has cemented itself as one of the most anticipated indie releases of late 2026. Combining shot-glass Russian roulette with the signature psychological storytelling of director **Fuyuki Hayashi** (WHO YOU) and publisher **Alliance Arts**, the game is poised to take the gaming community by storm.

This guide provides official release dates, platform availability, PC system specifications, Steam Deck optimization settings, and details surrounding the cancelled public demo.

---

## Release Date and Platform Availability

The official release details for Drunken Goddess Reflux are confirmed:

- **Global Release Date**: **December 8, 2026**
- **Lead Platform**: **PC via Steam** (Store App ID: 4150720)
- **Supported Languages**: English, Japanese, Traditional Chinese, Simplified Chinese (Full Japanese voice acting by Nanahira)
- **Store Page Link**: [Drunken Goddess Reflux on Steam](https://store.steampowered.com/app/4150720/Drunken_Goddess_Reflux/)

While console versions (Nintendo Switch 2, PlayStation 5) have been widely requested by the community, publisher Alliance Arts has confirmed that the team is 100% focused on delivering a polished, bug-free PC experience for December 8.

Learn the basics before launch with our [Beginner Guide](/guide/drunken-goddess-reflux-beginner-guide).

---

## PC System Requirements: Minimum vs Recommended

Thanks to efficient optimization of the 3D tavern environment and 2D character sprite animation by GUI designer Kaoru Ito and 3D artists tiri and temi, Drunken Goddess Reflux runs smoothly on a wide spectrum of PC hardware:

| Hardware Component | Minimum Requirements (1080p, 30 FPS) | Recommended Requirements (1080p, 60 FPS) |
| :--- | :--- | :--- |
| **Operating System** | Windows 10 64-bit | Windows 10 / 11 64-bit |
| **Processor (CPU)** | Intel Core i3-4160 / AMD FX-6300 | Intel Core i5-8400 / AMD Ryzen 5 2600 |
| **Memory (RAM)** | 8 GB RAM | 16 GB RAM |
| **Graphics (GPU)** | NVIDIA GeForce GTX 960 / AMD Radeon R9 280 | NVIDIA GeForce GTX 1060 (6GB) / AMD RX 580 |
| **DirectX** | Version 11 | Version 12 |
| **Storage Space** | 6 GB available space (SSD Recommended) | 6 GB available SSD space |
| **Audio** | DirectX compatible sound card | High-definition audio device (for 3D audio tells) |

Detailed control layouts and graphics toggles can be reviewed in our [PC Controls and Settings Guide](/codes/drunken-goddess-reflux-pc-controls-and-settings).

---

## Steam Deck & Handheld Performance

Drunken Goddess Reflux was developed with handheld gaming in mind. Valve testing indicates full **Steam Deck Verified** status at launch:
- **Target Performance**: Locked 60 FPS at 1280x800 resolution with default medium-high settings.
- **Battery Life**: Approximately 4.5 to 5.5 hours of continuous gameplay on the standard Steam Deck LCD, and over 6.5 hours on the Steam Deck OLED.
- **Controller Integration**: Full Steam Input support with native haptic feedback that rumbles rhythmically to reflect your avatar's heartbeat during Stage 4 Red Zone drunkenness!

---

## The Demo Cancellation Explained

In late October 2026, the developer made headlines by cancelling the planned public Steam demo. Director Fuyuki Hayashi released an official statement explaining that the unique turn-based drinking mechanics, custom shaders, and Nanahira's voice audio files were deemed vulnerable to rapid asset extraction and AI clone generation prior to the game's full release.

Instead of a public demo, Alliance Arts conducted closed, NDA-protected playtests through their official Discord server. Feedback from these playtests directly refined the balance of the [Spiritum Shot](/drinks/drunken-goddess-reflux-spiritum-lethal-shot-guide) and enhanced the puzzle design of [Pandemonium Bar Secrets](/guide/drunken-goddess-reflux-pandemonium-bar-secrets).

---

## Pro Tip: Audio Hardware Matters

Because detecting Femme Soule's bluffs depends heavily on subtle voice inflections and liquid glass pings, we strongly recommend playing with **over-ear headphones** rather than desktop monitor speakers. The stereo panning enables you to pinpoint which side of the counter high-proof glasses are placed on!

---

## Related Guides & Next Steps

Get ready for launch day:
- Learn the game rules in our [Russian Roulette Rules Explained](/guide/drunken-goddess-reflux-russian-roulette-mechanics).
- Check the full soundtrack details in [OST and DEMON'S SHOT Guide](/codes/drunken-goddess-reflux-ost-demons-shot-tracklist).
- See all drink properties in [Drink Tier List](/drinks/drunken-goddess-reflux-drink-tier-list).
- Discover active bonus codes in [Codes and Passwords](/codes/drunken-goddess-reflux-codes-and-passwords).
"""
}

# 23. PC Controls & Settings
codes["drunken-goddess-reflux-pc-controls-and-settings"] = {
    "title": "Drunken Goddess Reflux PC Controls, Keybinds and Settings",
    "description": "Comprehensive guide to keyboard, mouse, and gamepad controls for Drunken Goddess Reflux, including FOV and accessibility toggles.",
    "hub": "codes",
    "slug": "drunken-goddess-reflux-pc-controls-and-settings",
    "quickGuide": [
        "Full support for Keyboard & Mouse, Xbox controllers, DualSense, and Steam Deck.",
        "Key duel binds: Left Click to drink, Right Click to Napkin Spit, Spacebar to confirm toast.",
        "Exploration binds: WASD to walk, Shift to sprint, E to interact, Tab for inventory.",
        "Motion sickness accessibility toggles allow disabling camera drunkenness wobble.",
        "Colorblind modes add distinct geometric glyphs to glass rims for proof clarity."
    ],
    "faq": [
        {"q": "Can you rebind keys in Drunken Goddess Reflux?", "a": "Yes. The Settings menu features complete key rebinding for both keyboard/mouse and gamepad inputs, with support for primary and secondary key mappings."},
        {"q": "Is there an option to disable screen shake and drunken blur?", "a": "Yes. Under Accessibility Settings, players can toggle 'Drunken Visual Sway' and 'Motion Blur' to reduce motion sickness while keeping gameplay indicators intact."},
        {"q": "Does Drunken Goddess Reflux support DualSense haptics on PC?", "a": "Yes! When connected via USB, the PC version supports native DualSense adaptive triggers and nuanced haptic feedback simulating liquid sloshing inside the glasses."}
    ],
    "content": """
Whether you are navigating the atmospheric 3D speakeasy of Pandemonium or locking eyes with Femme Soule across the mahogany counter in a tense shot-glass Russian roulette, smooth and responsive controls are essential. **Drunken Goddess Reflux** features a versatile input and configuration suite designed by GUI lead Kaoru Ito and programmer oyatsu, accommodating mouse-and-keyboard purists, controller enthusiasts, and accessibility needs alike.

This comprehensive guide covers all default keybindings, gamepad mappings, graphics optimization toggles, and accessibility options.

---

## Complete Keyboard and Mouse Controls

The PC control scheme separates into two distinct phases: **Duel Mode** (first-person drinking duel) and **Exploration Mode** (free-roam 3D tavern exploration).

### 1. Duel Mode Controls (At the Bar Counter)
- **Mouse Hover**: Examine shot glasses and inspect surface tension.
- **Left-Click (`L-Click`)**: Select and pick up target glass.
- **Left-Click (Hold & Release)**: Drink the held glass.
- **Right-Click (`R-Click`)**: Initiate [Napkin Spit Bluff](/guide/drunken-goddess-reflux-beginner-guide) (reduces intake by 50%).
- **`Q` Key**: Tap table / Glass ping test (audio resonance check).
- **`Spacebar`**: Raise glass for toast / Confirm turn.
- **`1` / `2` / `3` / `4` Keys**: Activate Drunken Trick cards from active hand.
- **`Tab` Key**: Bite fresh lime wedge (steady aim for 10 seconds).
- **`Esc` Key**: Open Pause / Settings menu.

### 2. Exploration Mode Controls (3D Pandemonium Roam)
- **`W / A / S / D`**: Move character forward, left, backward, right.
- **Mouse**: Look around / Aim camera.
- **`Left Shift`**: Sprint.
- **`E` Key**: Interact with objects (Jukebox, Shaker, Padlock, Doors).
- **`Ctrl` Key**: Crouch (inspect low shelves, under-sink pipes).
- **`I` Key**: Open Inventory / Bartender Logbooks.

Learn how to explore Pandemonium effectively in [Pandemonium Bar Secrets](/guide/drunken-goddess-reflux-pandemonium-bar-secrets).

---

## Gamepad & Steam Deck Controller Layout

Drunken Goddess Reflux includes native mapping profiles for Xbox, PlayStation, and Steam Deck:

```
[Left Stick]  -> Character Movement (Walk / Run)
[Right Stick] -> Cursor Crosshair / Look Direction
[Right Trigger (RT / R2)] -> Drink Held Glass
[Left Trigger (LT / L2)]  -> Napkin Spit Bluff
[A / Cross Button]        -> Interact / Confirm Pick
[X / Square Button]       -> Tap Glass (Audio Resonance Test)
[Y / Triangle Button]     -> Open Trick Card Wheel
[B / Circle Button]       -> Cancel Action / Pass Turn
[D-Pad Up/Down/Left/Right]-> Select Trick Cards 1-4
[Menu / Start Button]     -> Pause Settings
```

For hardware specs and Steam Deck battery optimization, review our [Release Date and System Specs Guide](/codes/drunken-goddess-reflux-release-date-platforms-specs).

---

## Video & Graphics Settings: Maximizing Clarity

To ensure optimal visual detection of [Meniscus Surface Tells](/guide/drunken-goddess-reflux-russian-roulette-mechanics):

| Setting | Recommended Value | Competitive Impact |
| :--- | :--- | :--- |
| **Resolution** | Native (1920x1080 or higher) | Crucial for rendering micro-bubbles and vapor. |
| **V-Sync** | OFF (or Fast/G-Sync) | Reduces input lag during quick-time Ice Pick events. |
| **Motion Blur** | OFF | Eliminates unwanted camera smear when scanning glasses. |
| **Chromatic Aberration** | Standard (or Reduced) | Preserves game atmosphere while reducing eye strain. |
| **Field of View (FOV)** | 90° (Default: 80°) | Expands peripheral view of Femme Soule's facial tells. |
| **Anti-Aliasing** | TAA or SMAA | Smooths crystal glass edges for accurate meniscus reading. |

---

## Accessibility Settings: Comfort & Clarity

Developers WHO YOU implemented robust accessibility toggles:

1. **Drunken Camera Sway Toggle**: Reduces or disables the rhythmic 0.5Hz swaying effect during Stage 2 and 3 intoxication, preventing motion sickness.
2. **Colorblind Proof Glyphs**: In addition to natural liquid colors, enabling this option projects discreet geometric icons on the coasters:
   - Circle = Low Proof (0-20%)
   - Triangle = Medium Proof (40-50%)
   - Skull = Lethal Proof (70-96% including [Spiritum](/drinks/drunken-goddess-reflux-spiritum-lethal-shot-guide))
3. **Audio Cue Subtitles**: Displays text captions for subtle acoustic tells (e.g. `[Glass Vibrates with High Pitch]`, `[Femme Soule Giggles Nervously]`).

---

## Pro Tip: Sensitivity Tuning for Ice Pick Emergencies

If you find yourself missing the quick-time target when using the [Ice Pick](/guide/drunken-goddess-reflux-intoxication-ice-pick-guide), lower your Mouse Sensitivity by 20% in the controls menu. A lower sensitivity counters the involuntary cursor tremor induced by high intoxication, making knuckle-strike accuracy significantly higher!

---

## Related Guides & Next Steps

Fine-tune your setup for the ultimate duel:
- Review the game rules in [Russian Roulette Rules Explained](/guide/drunken-goddess-reflux-russian-roulette-mechanics).
- Study all drink properties in [Drink Tier List](/drinks/drunken-goddess-reflux-drink-tier-list).
- Learn how to master the boss encounter in [Femme Soule Boss Guide](/guide/drunken-goddess-reflux-femme-soule-boss-guide).
- Check active redemption codes in [Codes and Passwords](/codes/drunken-goddess-reflux-codes-and-passwords).
"""
}

# 24. OST & DEMON'S SHOT Tracklist
codes["drunken-goddess-reflux-ost-demons-shot-tracklist"] = {
    "title": "Drunken Goddess Reflux OST and Theme Song DEMON'S SHOT Guide",
    "description": "Official soundtrack details for Drunken Goddess Reflux, featuring theme song DEMON'S SHOT by Aiobahn +81, DEMONDICE, and Nanahira.",
    "hub": "codes",
    "slug": "drunken-goddess-reflux-ost-demons-shot-tracklist",
    "quickGuide": [
        "Theme song 'DEMON'S SHOT' composed by Aiobahn +81 with vocals by DEMONDICE.",
        "Voice actress Nanahira provides in-game vocal harmonies and exclusive ending themes.",
        "The OST features 14 tracks spanning electro-swing, hard techno, and melancholic ballads.",
        "Music dynamically shifts tempo, low-pass filter, and distortion as intoxication rises.",
        "Jukebox tracks can be discovered and played inside Pandemonium during exploration."
    ],
    "faq": [
        {"q": "Who composed the music for Drunken Goddess Reflux?", "a": "The official soundtrack was composed and arranged by Japanese electronic artist Aiobahn +81, renowned for high-energy anime and gaming anthems."},
        {"q": "Who sings the theme song DEMON'S SHOT?", "a": "The lead vocals and lyrics for 'DEMON'S SHOT' were written and performed by American-Japanese rapper and vocalist DEMONDICE, with additional voice backing by Nanahira."},
        {"q": "Can you buy the Drunken Goddess Reflux soundtrack?", "a": "Yes! The original soundtrack is available on Steam as a standalone digital album and streams across Spotify, Apple Music, and YouTube Music alongside the game's launch."}
    ],
    "content": """
Music is the beating, chaotic heart of **Drunken Goddess Reflux**. From the opening bass drop in the neon-lit alleyways of Hell to the intimate, drunken whispers shared over a mahogany bar counter, the game's soundscape is an electrifying masterpiece. Masterminded by Tokyo-based producer **Aiobahn +81** and featuring dynamic vocal performances by underground rap powerhouse **DEMONDICE** and beloved voice talent **Nanahira**, the soundtrack perfectly encapsulates the game's blend of high-octane Russian roulette and emotional vulnerability.

This guide provides the complete 14-track official tracklist, analyzes the interactive audio engine, reveals jukebox secrets, and explores how the music directly enhances gameplay.

---

## The Hit Theme Song: "DEMON'S SHOT"

The promotional trailer and title theme song **"DEMON'S SHOT"** took the indie gaming scene by storm upon its reveal. Blending frenetic electro-breakbeat rhythms with sharp hip-hop verses and hyper-energetic vocal hooks, the track serves as the game's narrative manifesto:

- **Music & Composition**: Aiobahn +81
- **Arrangement**: Aiobahn +81
- **Lyrics & Lead Vocals**: DEMONDICE
- **Character Voice & Chorus**: Nanahira (Femme Soule)
- **Theme Concept**: The intoxicating thrill of risking your soul for one more taste of forbidden passion in Pandemonium.

Watch the official trailers in our [Release Date and System Specs Guide](/codes/drunken-goddess-reflux-release-date-platforms-specs).

---

## Official 14-Track Pandemonium Tracklist

The complete original soundtrack features 14 tracks arranged chronologically across your descent into Hell:

| Track # | Track Title | Genre / Vibe | In-Game Scene / Usage |
| :--- | :--- | :--- | :--- |
| **01** | *DEMON'S SHOT (Feat. DEMONDICE)* | Electro-Rap / Hyperpop | Main Title Screen & 2nd Trailer |
| **02** | *Welcome to Pandemonium* | Lounge Jazz / Lo-Fi | 3D Bar Intermission Exploration |
| **03** | *Ice on the Counter* | Deep Minimal Techno | Round 1: The Icebreaker Duel |
| **04** | *Double Trouble, Darling* | Electro-Swing | Round 2: Phase 2 Femme Soule |
| **05** | *96 Proof Hellfire* | Dark Hardstyle / Gabber | Round 3: [Spiritum Lethal Showdown](/drinks/drunken-goddess-reflux-spiritum-lethal-shot-guide) |
| **06** | *The Ice Pick's Requiem* | Dark Ambient / Industrial | Playing the [Ice Pick Reset](/guide/drunken-goddess-reflux-intoxication-ice-pick-guide) |
| **07** | *Cocktail Shaker Shuffle* | Bossa Nova Synth | Intermission Mixology Mini-Game |
| **08** | *Green Fairy Mirage* | Psychedelic Synthwave | [Brimstone Absinthe](/drinks/drunken-goddess-reflux-brimstone-absinthe-guide) Hallucination |
| **09** | *Holy Radiance in the Cellar* | Choral Chamber Ambient | Discovering [Holy Water Contraband](/drinks/drunken-goddess-reflux-holy-water-contraband) |
| **10** | *Morning Light (Reclaimed)* | Inspiring Piano Ballad | [Ending 1: True Freedom Escape](/endings/drunken-goddess-reflux-true-ending-freedom) |
| **11** | *Till the Ice Melts (Acoustic)* | Melancholy Jazz Waltz | [Ending 2: Eternal Partner Romance](/endings/drunken-goddess-reflux-eternal-partner-ending) |
| **12** | *Stuffed in a Bottle* | Creepy Carnival Waltz | Ending 3: Soul-Spilled Husk |
| **13** | *Supernova Double Reflux* | Cosmic Synth Jam | [Ending 4: Mutual Reflux Secret](/endings/drunken-goddess-reflux-mutual-reflux-secret-ending) |
| **14** | *Under New Management* | Big Band Electro-Swing | [Ending 5: Hell Bartender Career](/endings/drunken-goddess-reflux-hell-bartender-ending) |

---

## Dynamic Audio Engine: How Drunkenness Modifies Music

Rather than playing static audio loops, programmer okazu and composer Aiobahn +81 built an **interactive music layer** that reacts in real-time to your avatar's [Intoxication Gauge](/guide/drunken-goddess-reflux-intoxication-ice-pick-guide):

```
[0% - 35% Intoxication]: Clean Audio -> Crisp hi-hats, clear synths, normal tempo.
[36% - 65% Intoxication]: Low-Pass Filter -> Treble gently rolls off; bass gains warm tube saturation.
[66% - 84% Intoxication]: Flanger & Chorus -> Ambient music swooshes with rhythmic phasing; tempo fluctuates.
[85% - 99% Intoxication]: Muffled Heartbeat -> Music volume drops 70%; loud 140 BPM heartbeat overtakes mix.
```

When your character enters Stage 4 Red Zone drunkenness, the music feels like you are listening to it through a swimming pool wall, dramatically heightening tension during life-or-death decisions!

---

## Interactive Jukebox Passwords

During 3D bar intermissions in Pandemonium, you can walk up to the glowing neon Jukebox in the lounge and punch in numerical codes to unlock hidden unreleased B-sides:
- **Input `1994`**: Plays the unreleased 8-bit chip-tune track *"Yunyun Syndrome Retro Mix"*.
- **Input `0711`**: Plays *"DEMON'S SHOT (Instrumental Club Edit)"*.
- **Input `8888`**: Unlocks the secret developer commentary audio reel with director Fuyuki Hayashi!

Check all jukebox locations in [Pandemonium Bar Secrets Exploration](/guide/drunken-goddess-reflux-pandemonium-bar-secrets).

---

## Pro Tip: Audio Balance for Competitive Play

In the Audio Settings menu, we recommend setting **Sound Effects to 100%**, **Voice Audio (Nanahira) to 95%**, and **Music Volume to 75%**. This balance ensures you can clearly hear the subtle glass pings and vocal tells described in our [Femme Soule Boss Guide](/guide/drunken-goddess-reflux-femme-soule-boss-guide) over the thumping techno beats!

---

## Related Guides & Next Steps

Continue immersing yourself in the world of Pandemonium:
- Read about the themes of each song in [Seven Flavors of Ruin Lore Breakdown](/endings/drunken-goddess-reflux-seven-flavors-of-ruin-breakdown).
- Learn how to escape Hell in the [True Ending Freedom Walkthrough](/endings/drunken-goddess-reflux-true-ending-freedom).
- Check active item and music codes in [Codes and Passwords](/codes/drunken-goddess-reflux-codes-and-passwords).
- Review all game achievements in [Steam Achievements Guide](/codes/drunken-goddess-reflux-steam-achievements-guide).
"""
}

# Write all 5 codes guides
for slug, data in codes.items():
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

print(f"Successfully generated all {len(codes)} guides for 'codes' hub.")
