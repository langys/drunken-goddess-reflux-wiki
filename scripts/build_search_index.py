#!/usr/bin/env python3
"""Build the static search index consumed by the site's search dialog.

Reads `content/<locale>/*.md`, extracts the frontmatter plus the markdown
headings and opening prose of each page, and writes `public/search-index.json`.

Why a static index and not a hosted search service: the whole site is
prerendered, and shipping a JSON file to the client keeps search instant, free,
and independent of any third party. At a few hundred pages the file stays small
enough (~40-80KB gzipped) that fetching it on first open is faster than any
network round trip to a search API.

Usage:
    python3 scripts/build_search_index.py                 # from the site root
    python3 scripts/build_search_index.py --site-dir . --pretty
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
HEADING = re.compile(r"^(#{2,3})\s+(.+?)\s*$", re.M)
# Strip markdown syntax so indexed text matches what a reader typed.
NOISE = [
    (re.compile(r"\[([^\]]+)\]\([^)]+\)"), r"\1"),
    (re.compile(r"[*_`>#]"), ""),
    (re.compile(r"\|"), " "),
    (re.compile(r"\s+"), " "),
]


def parse_frontmatter(text: str) -> tuple[dict, str]:
    match = FRONTMATTER.match(text)
    if not match:
        return {}, text
    block, body = match.group(1), text[match.end():]
    data: dict = {}
    for line in block.splitlines():
        if not line.strip() or line.startswith((" ", "\t", "-")):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip().strip('"').strip("'")
        if value:
            data[key.strip()] = value
    return data, body


def clean(value: str) -> str:
    for pattern, replacement in NOISE:
        value = pattern.sub(replacement, value)
    return value.strip()


def build_entries(site_dir: pathlib.Path) -> list[dict]:
    content_root = site_dir / "content"
    if not content_root.is_dir():
        print(f"error: no content directory at {content_root}", file=sys.stderr)
        return []

    # `legal/` holds shared pages with a per-locale override, so it is NOT a
    # locale directory — treating it as one would index four pages labelled
    # "legal" and hide them from every real locale.
    locale_dirs = sorted(
        p for p in content_root.iterdir() if p.is_dir() and p.name != "legal"
    )
    if not locale_dirs:
        print(f"error: no locale directories under {content_root}", file=sys.stderr)
        return []

    entries: list[dict] = []
    legal_root = content_root / "legal"

    for locale_dir in locale_dirs:
        locale = locale_dir.name

        for path in sorted(locale_dir.glob("*.md")):
            raw = path.read_text(encoding="utf-8", errors="replace")
            meta, body = parse_frontmatter(raw)

            headings = [clean(h) for _, h in HEADING.findall(body)]
            # Drop the first heading when it merely repeats the title.
            title = meta.get("title", path.stem.replace("-", " "))
            headings = [h for h in headings if h.lower() != title.lower()]

            prose = clean(HEADING.sub(" ", body))
            hub = meta.get("hub", "guide")
            slug = meta.get("slug", path.stem)

            entries.append(
                {
                    "slug": slug,
                    "locale": locale,
                    "hub": hub,
                    "title": title,
                    "description": meta.get("description", ""),
                    "headings": headings[:12],
                    "text": prose[:600],
                }
            )

        # Legal pages: prefer the localized file, fall back to the shared one —
        # the same rule lib/legal.ts applies at render time, so search never
        # links to a page the site does not actually serve in that locale.
        legal_dir = legal_root / locale
        for slug in ("about", "contact", "privacy", "terms"):
            localized = legal_dir / f"{slug}.md"
            shared = legal_root / f"{slug}.md"
            path = localized if localized.exists() else shared
            if not path.exists():
                continue
            meta, body = parse_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
            entries.append(
                {
                    "slug": slug,
                    "locale": locale,
                    "hub": "legal",
                    "title": meta.get("title", slug.title()),
                    "description": meta.get("description", ""),
                    "headings": [clean(h) for _, h in HEADING.findall(body)][:8],
                    "text": clean(HEADING.sub(" ", body))[:400],
                }
            )

    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--site-dir", type=pathlib.Path, default=pathlib.Path("."))
    parser.add_argument("--out", type=pathlib.Path, default=None, help="default: <site-dir>/public/search-index.json")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    entries = build_entries(args.site_dir)
    if not entries:
        print("error: nothing indexed — check that content/<locale>/*.md exist", file=sys.stderr)
        return 1

    out = args.out or (args.site_dir / "public" / "search-index.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2 if args.pretty else None),
        encoding="utf-8",
    )

    by_locale: dict[str, int] = {}
    for entry in entries:
        by_locale[entry["locale"]] = by_locale.get(entry["locale"], 0) + 1

    size_kb = out.stat().st_size / 1024
    print(f"wrote {out} — {len(entries)} pages, {size_kb:.1f} KB")
    for locale, count in sorted(by_locale.items()):
        print(f"  {locale}: {count}")
    if size_kb > 250:
        print("  warning: index is large; consider indexing titles + headings only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
