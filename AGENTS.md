# AGENTS.md

Workspace instructions for AI agents (Antigravity / Claude Code / Codex / Cursor) working on this site.

## Repository Purpose

This is a **static game wiki site** (Next.js 15 App Router, `output: 'export'`) built from the `game-wiki-site-builder` skill template. It earns search traffic via a hub-and-spoke content silo and monetizes with ads. Deployed as pure static files (`out/`) to Cloudflare Pages.

## Read These First

- `config/site.config.ts` — **single source of truth** for game name, domain, hubs, locales, ads, analytics, media. Read before any change.
- `lib/content.ts` — how markdown becomes routes; the comments document the SEO invariants.

## Tech Stack (pinned)

| Layer     | Choice                                            | Notes                                                                                  |
| --------- | ------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Framework | Next.js 15 App Router, `output: 'export'`         | Pure static. No server runtime, no API routes, no ISR.                                 |
| i18n      | next-intl 3, `localePrefix: 'as-needed'`          | English has no `/en` prefix; other locales are prefixed.                               |
| Content   | markdown + gray-matter frontmatter in `content/`  | File path = URL slug.                                                                  |
| Styles    | Tailwind 3 + HSL CSS vars                         | Theme color lives in `siteConfig.themeColor`; never hardcode hex in components.        |
| Ads       | Adsterra (rendered) + AdSense (declaration only)  | All ad units gated: key `'0'` / placeholder = component renders nothing.               |
| Search    | `scripts/build_search_index.py` → static JSON     | Runs as part of `npm run build`.                                                       |
| Deploy    | Cloudflare Pages via `wrangler pages deploy`      | `out/` + `public/_headers` + `public/_redirects`.                                      |
| Scripts   | Python 3 stdlib only                              | No pip dependencies — keep it that way.                                                |

## Architecture: Code / Config / Content Separation (critical)

```
Code layer    (app/, components/, lib/, i18n/)   — framework, game-agnostic
Config layer  (config/site.config.ts, public/)   — edit once per site
Content layer (content/<locale>/, messages/)     — fully replaced per site
```

- Changing content must not touch framework code.
- The framework layer must contain **zero** game-specific strings; if you add one, it belongs in `site.config.ts`, `messages/*.json`, or `content/`.

## Engineering Constraints (numbered — cite them in reviews)

1. **Body starts at H2.** The H1 is rendered from frontmatter `title`. A `#` heading in markdown body is an error (gate: `check:content` E1).
2. **frontmatter `hub` must exist in `siteConfig.hubs`.** Hub key = nav item = home section = silo. A typo'd hub silently files the article under the first hub.
3. **frontmatter `slug` must equal the file name.** `config/pages.ts` (listing manifest) and sitemap both derive URLs from these.
4. **`title` ≤ 80 chars; `description` 40–165 chars.** Hard gates (E7/E8). Remember the rendered `<title>` appends ` - <Site Name>`.
5. **`published`/`modified` are ISO `YYYY-MM-DD` strings.** YAML parses unquoted dates into `Date` objects which crash React prerender — `lib/content.ts` coerces, but write them quoted anyway.
6. **hreflang/sitemap only advertise locales that have real content** (`localesWithContent()`). Never point an alternate at a URL that 404s — it poisons the whole hreflang cluster.
7. **Sitemap lists only pages that exist.** Never generate sitemap URLs from config arrays alone.
8. **Internal links in markdown must resolve.** Non-default locales must prefix links with `/<locale>/` — a bare `/guide/x` from a translated page serves the English page silently (gate: `check:content` E5/E6).
9. **Every article wants ≥3 inline internal links, same hub preferred.** Cross-hub linking turns the silo into link soup; `getRelatedGuides()` enforces same-hub for the related box. (Lesson learned: a site whose bodies have zero inline links is an orphan-page farm — the gate will catch it.)
10. **UI copy goes in `messages/<locale>.json`**, never hardcoded in components. Adding a UI string means adding it to **every** locale file.
11. **No game facts invented.** Stats, dates, prices, codes: if it isn't in the source material the user gave you, mark it as TBD and ask. One fabricated fact destroys site trust.
12. **Ads stay gated.** `adsenseClient` placeholder `ca-pub-XXXXXXXXXXXXXXXX` must never reach the browser (layout validates `ca-pub-\d+`); Adsterra keys of `'0'` mean "no ad". Keep the default = no-ads contract.
13. **Domain only via `siteConfig.url`.** og:image / canonical / JSON-LD derive from it; no hardcoded domain strings outside config/README.
14. **New markdown fields must be optional.** Old articles must keep building forever.
15. **After any content or config change: `npm run check:content && npm run build` must both pass.** "Verify, don't trust yourself."
16. **IndexNow identity is the repo-root `.indexnow-key` (64 hex).** It is public by design (served at `/<key>.txt`) — commit it, never rotate without reason. Submission must never fail a deploy.
17. **Zero template fingerprints.** No string from the template's demo game, no placeholder domains, no `TEMPLATE PLACEHOLDER` llms.txt may survive into a launched site (gate: `check:rebrand`). When rebranding an existing site, pass the old name: `npm run check:rebrand -- --legacy OldName`. Demo-content articles that don't match the `<GameName>-<intent>` slug convention are flagged too. **This gate exists because a real site shipped with the demo game's FAQ and tier-list pages — run it after every content replacement.** <!-- check-rebrand-ignore -->
18. **Search pages never indexed.** `/search` and all locale search pages (`/[locale]/search`) MUST specify `robots: { index: false, follow: true }` and MUST NEVER enter `sitemap.xml`. Do NOT disallow search in `robots.txt` so crawlers can read the noindex directive.
19. **Automated Git Deploy & Safe PR Delivery.** When connected to Cloudflare Pages via GitHub, AI agents MUST deliver work via GitHub Draft PR (`gh pr create --draft`). Never run manual `wrangler pages deploy` or `vercel deploy` in production. Merging into `main` automatically triggers production Cloudflare Edge builds.
20. **Multi-Engine Post-Merge Indexing.** IndexNow now runs **automatically**: `.github/workflows/ci.yml` ends with `npm run indexnow:ci` on every push to `main` (and manual dispatch). That step is gated twice — `--wait` polls the production sitemap until Cloudflare has finished building from the same commit, then `--verify-live` drops any URL that does not return HTTP 200 before announcing. It is `continue-on-error: true` and the script always exits 0. After PR merge, the remaining manual steps are Google Indexing API batch submit via Search Console MCP (`indexing_batch_submit`, daily 200 quota) and Bing Webmaster Tools API (`bing_url_submit_batch`).
21. **Knowledge Synchronization (Nowledge Mem).** Recall context at session start via `memory_search` before re-analyzing architecture or game mechanics. Distill official announcements (Steam `event_gid`, 4-tier system specs, confirmed prices) as atomic memories. Never label official developer communications as speculation.
22. **Multilingual 1:1 Content Parity.** Any locale declared in `siteConfig.locales` MUST achieve 100% guide and hub parity with the default locale before production launch. Never deploy partial multilingual directories (e.g. 4 articles in sub-locales vs 22 in default) — Google flags incomplete directories as thin content / doorways, breaking bidirectional hreflang and causing "Discovered - currently not indexed". Either commit to full 1:1 translation for a locale, or do not add it to `locales`.
22. **Video facts get frame-verified.** Proper nouns (characters, areas, items) are accepted from one of three sources only: the game's own on-screen label in an extracted frame, a hand-written chapter list, or 2+ independent sources — and even 2+ ASR transcripts can agree and still be wrong (measured: both wrote "Broner"; the on-screen label reads **Brauner**). Footage and captions never enter git (`research/videos/`, `research/transcripts/` are ignored); reports carry `&t=seconds` links instead. Workflow: `.agent/skills/wb-video-facts` — `.workbuddy/skills` is a **symlink** to `.agent/skills`, so WorkBuddy sessions load the same single copy.

## Commands

```bash
npm run dev              # dev server
npm run build            # search index → next build
npm run typecheck        # tsc --noEmit, 0 errors expected
npm run lint             # next lint
npm run check:content    # scripts/check_content.py — content lint (13 rules, errors fail)
npm run check:rebrand    # scripts/check_rebrand.py — template-fingerprint scan (demo-game leftovers)
npm run check:links      # scripts/check_links.py — dead-link scan + header nav-link gate on out/ (run after build)
npm run audit:freshness  # scripts/refresh_audit.py — stale content report (P0/P1/P2/TR)
npm run audit:seo        # scripts/audit_seo.py — live-server SEO checks (needs dev server)
npm run search:index     # rebuild public/search-index.json only
npm run indexnow:init    # generate/reuse .indexnow-key + public/<key>.txt (idempotent)
npm run submit:indexnow  # submit production sitemap URLs to IndexNow (Bing/Yandex)
npm run indexnow:ci      # CI form: --local --wait 600 --verify-live (deploy + liveness gates)
```

## Agent Skills

`.agent/skills/` holds task-specific playbooks (Agent Skills open standard; Antigravity reads this directory):

- `wb-new-article` — write one guide from source material, gates included
- `wb-batch-articles` — keyword list → batch of drafts without doorway-page patterns
- `wb-refresh` — read-only freshness audit → prioritized update plan
- `wb-seo-audit` — pre-publish / pre-ad-application checklist with four-state verdicts
- `wb-video-facts` — video → captions / chapters / clips → frame-verified names and facts

## Next.js Static Export Gotchas (verified)

1. **`output: 'export'` means no dynamic anything.** Every page needs `generateStaticParams`; `app/sitemap.ts` and `app/robots.ts` need `export const dynamic = 'force-static'`.
2. **YAML dates are `Date` objects, not strings.** Unquoted `published: 2026-09-25` crashes React at prerender ("Objects are not valid as a React child"). `lib/content.ts asDateString()` exists because translations kept doing this.
3. **Default-locale URLs have no prefix.** Canonical for English is `/guide/x`, for others `/<locale>/guide/x`. Get this wrong in metadata and Google sees duplicates.
4. **`config/pages.ts` and `content/` drift silently.** `validateContentCoverage()` warns at build; treat warnings as bugs — a listed-but-missing page is a 404 in the nav.
5. **Images are `unoptimized: true`** (static export). Use fixed width/height or aspect-ratio boxes to avoid CLS.

## Decisions to Confirm with the User Before Deviating

- Adding any server runtime (API routes, ISR, middleware logic beyond locale redirect).
- Turning on new ad networks or ad positions.
- Changing the domain, hub set, or locale list.
- Publishing content based on unverified game facts.
