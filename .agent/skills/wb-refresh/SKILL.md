---
name: wb-refresh
description: Read-only content freshness audit producing a prioritized update plan. Triggers: 内容保鲜, 过期内容, freshness audit, 哪些文章该更新了, refresh stale content, codes 过期.
---

# wb-refresh — Freshness Audit (READ-ONLY)

**This skill modifies nothing.** It produces a prioritized list of what to update and why. Rewriting is a separate, user-approved step.

## Workflow

### Step 1 — Run the deterministic audit

```bash
npm run audit:freshness
```

This reports per article: P0 (time-sensitive hubs like release/news >30d, or any page >180d), P1 (>90d), P2 (>60d), TR (translation lagging the English source >14d).

### Step 2 — Enrich with external signals (when available)

For the top P0/P1 items, check what actually changed in the game since `modified`:

- Official channels: Steam news page, developer blog/X, official Discord announcements.
- If the game shipped an update/patch/hotfix since the article was touched, the article is a real P0 regardless of calendar age. For games with codes pages: codes older than 7 days are effectively P0 even when the calendar rule has not fired yet.

If the user has GSC export data, note which stale pages still get impressions — those are the revenue-critical ones.

### Step 3 — Produce the plan

A markdown table, sorted by priority:

| Priority | Page | Why stale | What to update | Effort |
|----------|------|-----------|----------------|--------|

Rules for the plan:

- Each row names the **concrete sections** that need new facts (not "refresh the page").
- Batch related pages (same hub, same game update) into one work item.
- Translations (TR rows) always list which English sections changed, so the translator doesn't re-read the whole article.
- End with a recommendation: which 3 pages to do this week, and which can wait.

### Step 4 — Hand off

Present the plan and ask the user which items to execute. Only then switch to writing (using `wb-new-article` rules for each rewrite: gates `npm run check:content && npm run build`, and bump `modified` to today's date).

**Do not bump `modified` without substantive content changes** — fake freshness is a known spam signal and erodes trust with both Google and readers. Expired codes are **kept, marked expired, never deleted** — "is X still working" is valuable long-tail traffic.
