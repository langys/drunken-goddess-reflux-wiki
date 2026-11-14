---
name: wb-new-article
description: Write a single wiki guide from user-provided source material. Triggers: 写一篇攻略, 新增文章, write a guide, new article, 根据素材写页面, add a page.
---

# wb-new-article — Single Article Authoring

Produces one build-passing markdown guide in `content/<locale>/`. Content only — never touches framework code.

## Red Lines (read first, never cross)

1. **Never invent game facts** (stats, dates, prices, codes, names). If the source material doesn't say it, write `TBD` and ask the user. One fabricated fact destroys site trust.
2. Source material from videos/forums is **fact reference only** — never copy phrasing; rewrite from understanding.
3. Internal links must point to pages that **actually exist** (same locale). `npm run check:content` E5/E6 enforces this.
4. Don't create a new hub. Hubs live in `config/site.config.ts` and changing them is a config-layer decision — ask the user.

## Workflow

### Step 0 — Read the contracts (mandatory, in order)

1. `AGENTS.md` — especially constraints #1–#9, #11, #15.
2. `config/site.config.ts` — hubs, locales, `external.store` for the CTA.
3. `config/pages.ts` — check whether this slug is already in the manifest; if the article is new, it must be added there too.
4. **One existing article of the same hub** for structure and tone.

### Step 1 — Confirm the brief with the user

- Target keyword / slug (format: `<GameName>-<intent-phrase>`, matching the existing files' convention).
- Hub (one of the keys in `siteConfig.hubs`).
- Locale (default `en`; translations are a separate step).
- Source material the user is providing. If none, stop and ask — see Red Line 1.

### Step 2 — Write `content/<locale>/<slug>.md`

Frontmatter (all required unless noted):

```yaml
---
title: "<Game> <Topic>: <Benefit>"            # <= 80 chars incl. the rendered " - <Site Name>" suffix
description: "<verb-first, 40-165 chars, one concrete detail>"
hub: "<hub key from siteConfig.hubs>"
slug: "<must equal file name>"
published: "YYYY-MM-DD"                        # quoted — YAML would make it a Date
modified: "YYYY-MM-DD"
quickGuide:                                    # 5 one-line bullets: "<phrase>: <detail>"
  - "..."
cards:                                         # optional, 2-4 scannable cards
  - title: "..."
    body: "..."
faq:                                           # 3-5 Q&A, real searcher questions
  - q: "..."
    a: "..."
image: "<optional absolute https cover URL>"
---
```

Body rules:

- First heading is `##` — **never `#`** (H1 comes from `title`; constraint #1).
- Prefer question-shaped H2s ("How do I...?") with a 40–60 word direct answer right after — this is the AI-Overviews/featured-snippet pattern.
- **≥3 inline internal links** to existing same-locale pages, same hub preferred. Non-English bodies prefix every internal link with `/<locale>/`.
- Use comparison data as real markdown tables (GFM), not ASCII art.
- Keyword appears in title, first 100 words, one H2 — natural density, no stuffing.

### Step 3 — Register the page

- Add the slug to `config/pages.ts` (the listing manifest) in the right hub section, or the hub listing won't show it.

### Step 4 — Verify (both must pass, no exceptions)

```bash
npm run check:content   # 0 errors for your file
npm run build           # must end green
```

If either fails, fix and rerun. Do not report success without both green.

### Step 5 — Report

One short summary: file created, hub, internal links used, gates status. Flag every fact you marked TBD.
