---
name: wb-batch-articles
description: Turn a keyword list into a batch of wiki draft articles without doorway-page patterns. Triggers: 批量写文章, batch articles, 关键词列表生成页面, 批量生产内容, bulk posts.
---

# wb-batch-articles — Batch Content Production

Produces N draft articles from a keyword list. Single-article rules come from `wb-new-article` — this skill only adds batch discipline.

## Red Lines

1. Everything in `wb-new-article` Red Lines applies (especially: never invent facts).
2. **No doorway pages.** Within one batch, do NOT reuse: the same intro sentence pattern, the same H2 section names in the same order, the same table headers, or boilerplate paragraphs with only the keyword swapped. Google penalizes this and it is the #1 batch-production failure mode.
3. Every batch article is published as a **draft-quality page**: it must still pass all gates, but report it as needing a human fact-check pass.
4. Max ~10 articles per batch — beyond that, quality and differentiation collapse. Split bigger lists into multiple runs.

## Workflow

### Step 0 — Intake

Get from the user: keyword list (or CSV with `locale,hub,slug,title`), and the shared source material. Classify each keyword by intent:

- **Informational** ("how to", "guide") → standard guide structure
- **List/comparison** ("best", "tier", "all X", "codes") → table-heavy structure
- **Navigational/transactional** ("release date", "price", "download") → direct-answer-first structure

Mixed intents in one batch are good — they force structural variety.

### Step 1 — Plan differentiation BEFORE writing

Write a one-line angle per article: what does this page answer that no other page in the batch (or on the site) does? If two keywords share an angle, merge them or ask the user — do not write both.

### Step 2 — Write each article

Follow `wb-new-article` Step 2/3 per article (frontmatter contract, body rules, `config/pages.ts` registration). Vary section names, intro patterns, and card/FAQ mixes across the batch. Cross-link batch siblings where genuinely relevant (this also satisfies the ≥3 internal-links rule).

### Step 3 — Batch-level checks

1. Grep the batch for repeated sentence openers and repeated H2 titles — any collision gets rewritten.
2. Confirm every title/description is unique (`check:content` W12 also catches duplicates).

### Step 4 — Verify

```bash
npm run check:content && npm run build
```

Both green = done. Then report: table of slug / hub / angle / internal-links-count, plus the fact-check TODO list.
