---
name: wb-seo-audit
description: Pre-publish or pre-ad-application SEO audit with four-state verdicts. Triggers: SEO 体检, SEO audit, 发布前检查, AdSense 申请前检查, pre-publish checklist.
---

# wb-seo-audit — Four-State SEO Audit

Item-by-item audit. Every item gets exactly one verdict: **Pass / Fail / Unknown / N/A**, plus a severity (Blocker / High / Medium) for Fail items.

## Completion gates (meta-rules)

1. If the final report has fewer items than the checklist below, **the audit is not done** — go back.
2. If any **Blocker** is unresolved, do NOT recommend publishing or applying for ads.
3. No item may be silently skipped: use N/A with a one-line reason.

## Checklist

### A. Technical foundation (run commands, don't guess)

- A1 `npm run typecheck` passes — 0 errors (Blocker)
- A2 `npm run check:content` passes — 0 errors (Blocker)
- A3 `npm run build` passes, `out/` generated (Blocker)
- A4 `npm run check:links` on the fresh `out/` — 0 dead links AND no missing header nav links (Blocker)
- A5 `app/sitemap.ts` lists only real pages (spot-check 3 URLs against `out/`) (High)
- A6 `app/robots.ts` allows crawling and references the sitemap (High)
- A7 `public/_headers` present for Cloudflare Pages caching rules (Medium)

### B. On-page contracts (sample ≥5 articles across hubs)

- B1 Exactly one H1 per page, from frontmatter title; body starts at H2 (High)
- B2 title ≤80 chars (incl. the ` - <Site Name>` suffix), description 40–165 chars (High)
- B3 Canonical + hreflang cluster present, x-default points at English (High)
- B4 og:image is an absolute URL (Blocker if relative)
- B5 JSON-LD renders: Article + Breadcrumb on guides, site schema on home (High)
- B6 ≥3 inline internal links per article, same-hub related box present (Medium)
- B7 quickGuide + faq blocks present (AI-answer readiness) (Medium)

### C. Trust & monetization readiness (required before AdSense application)

- C1 /about, /contact, /privacy, /terms reachable from footer on every page (Blocker for ad application)
- C2 Contact email on /contact is a real mailbox (High)
- C3 No placeholder config live: `adsenseClient` is either real or gated off (High)
- C4 ads.txt matches the live ad setup (High)
- C5 Content volume ≥20 substantive pages, no empty hub listings (Blocker for ad application)
- C6 No fabricated/unverifiable claims in sampled articles (Blocker)

### D. Freshness & discovery

- D1 `npm run audit:freshness` — zero P0, P1 items have a plan (High)
- D2 `public/llms.txt` reflects current hubs and page inventory (Medium)
- D3 GSC: sitemap submitted, no coverage errors spike (Unknown if no access — say so)
- D4 GA4 tag fires (check network/console on dev server) (Medium)
- D5 `.indexnow-key` initialized and `/<key>.txt` live on production (Medium)

## Report format

```
| #  | Item | Verdict | Severity | Evidence / note |
```

Then: Blockers first, one-line fix per Fail, and a final verdict — "ready to publish", "ready to apply for ads", or "not ready because: ...".
