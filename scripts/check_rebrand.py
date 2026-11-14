#!/usr/bin/env python3
"""check_rebrand.py — template-purity lint ("换皮残留扫描").

Catches the classic scaffold failure mode: the new site ships with leftover
fingerprints from the template's demo game (or from a previous rebrand).

Two layers:

  E  denylist scan — every text file is searched for template/demo markers
     (built-in: the demo game name, placeholder domains, the llms.txt
     placeholder banner) plus any `--legacy` strings you pass (e.g. the
     previous game's name when rebranding an existing site).
  W  slug convention — content/<locale>/*.md file names should start with
     `<GameName>-` (from siteConfig.name). A file that doesn't is usually a
     demo article that survived the rebrand.

Exit 1 on any error. Stdlib only.

Usage:
  python3 scripts/check_rebrand.py --site-dir .
  python3 scripts/check_rebrand.py --site-dir . --legacy OldGameName
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

# Built-in template fingerprints (case-insensitive). These come from the
# game-wiki-site-builder template's demo content — none of them may survive
# into a real site. (example.com/example.wiki are deliberately NOT here:
# they are RFC-reserved and appear legitimately in docs and test fixtures.)
BUILTIN_DENYLIST = [
    "scavland",
    "placehold.co",
    "__SITE_SLUG__",
    "TEMPLATE PLACEHOLDER",
    "lorem ipsum",
]

SCAN_EXTENSIONS = {".ts", ".tsx", ".md", ".json", ".py", ".mjs", ".js", ".css", ".html", ".txt", ".yml", ".yaml"}
SKIP_DIRS = {"node_modules", ".git", ".next", "out", ".wrangler", ".workbuddy", "__pycache__"}
SKIP_FILES = {"package-lock.json", "check_rebrand.py", "CHANGELOG.md"}
NAME_RE = re.compile(r"^\s{2}name: '([^']+)'", re.M)


def game_name(site_dir: pathlib.Path) -> str:
    cfg = (site_dir / "config" / "site.config.ts").read_text(encoding="utf-8")
    m = NAME_RE.search(cfg)
    return m.group(1) if m else ""


def iter_files(site_dir: pathlib.Path):
    for p in sorted(site_dir.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(site_dir)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if p.name in SKIP_FILES or p.suffix.lower() not in SCAN_EXTENSIONS:
            continue
        yield p, rel


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-dir", default=".")
    ap.add_argument("--legacy", action="append", default=[],
                    help="extra forbidden string (repeatable), e.g. the previous game's name")
    args = ap.parse_args()
    site_dir = pathlib.Path(args.site_dir).resolve()

    denylist = BUILTIN_DENYLIST + [s for s in args.legacy if s]
    errors = warnings = scanned = 0

    for p, rel in iter_files(site_dir):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        scanned += 1
        low = text.lower()
        for marker in denylist:
            if marker.lower() in low:
                for i, line in enumerate(text.splitlines(), 1):
                    # Lines documenting the gate itself may legitimately name
                    # the markers; exempt them explicitly (noqa-style).
                    if "check-rebrand-ignore" in line:
                        continue
                    if marker.lower() in line.lower():
                        errors += 1
                        print(f"ERROR   {rel}:{i}: template fingerprint '{marker}': {line.strip()[:80]}")

    # Slug convention per locale.
    name = game_name(site_dir)
    if name:
        prefix = name.replace(" ", "-").lower()
        content = site_dir / "content"
        for locale_dir in sorted(content.iterdir()) if content.is_dir() else []:
            if not locale_dir.is_dir() or locale_dir.name == "legal":
                continue
            for md in sorted(locale_dir.glob("*.md")):
                if not md.stem.lower().startswith(prefix + "-"):
                    warnings += 1
                    print(f"WARN    {md.relative_to(site_dir)}: file name does not start with '{prefix}-' "
                          f"(possible demo-content leftover)")

    print(f"\ncheck-rebrand: {scanned} files scanned, {errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
