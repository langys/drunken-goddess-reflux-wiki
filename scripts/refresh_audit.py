#!/usr/bin/env python3
"""refresh_audit.py — deterministic content-freshness report (read-only;
inspired by AnvilWiki's scripts/refresh-audit.ts).

Priority rules:
  P0  release/news-type hubs older than RELEASE_P0_DAYS (time-sensitive info)
  P0  any guide older than STALE_P0_DAYS since last modification
  P1  any guide older than STALE_P1_DAYS
  P2  any guide older than STALE_P2_DAYS
  TR  translation whose `modified` lags the English source by > LAG_DAYS

Exit code is always 0 (report-only) unless --strict is passed and P0s exist.
Run: python3 scripts/refresh_audit.py --site-dir .
"""
from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import sys

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
SCALAR_RE = re.compile(r"^([A-Za-z_][\w]*):\s*(?:\"([^\"]*)\"|'([^']*)'|([^#\n]+?))\s*$")

RELEASE_HUBS = {"release", "news"}
RELEASE_P0_DAYS = 30
STALE_P0_DAYS = 180
STALE_P1_DAYS = 90
STALE_P2_DAYS = 60
LAG_DAYS = 14


def parse_fm(text: str) -> dict[str, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        s = SCALAR_RE.match(line)
        if s:
            fm[s.group(1)] = next(g for g in s.groups()[1:] if g is not None)
    return fm


def parse_date(val: str) -> dt.date | None:
    try:
        return dt.date.fromisoformat(val[:10])
    except ValueError:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-dir", default=".")
    ap.add_argument("--strict", action="store_true", help="exit 1 when P0 items exist")
    args = ap.parse_args()
    site_dir = pathlib.Path(args.site_dir).resolve()
    today = dt.date.today()

    rows: list[tuple[str, str, str, int, str]] = []  # (prio, locale, slug, age, note)
    en_modified: dict[str, dt.date] = {}
    translated: dict[str, list[tuple[str, dt.date]]] = {}

    content_root = site_dir / "content"
    for locale_dir in sorted(content_root.iterdir()):
        if not locale_dir.is_dir() or locale_dir.name == "legal":
            continue
        locale = locale_dir.name
        for md in sorted(locale_dir.glob("*.md")):
            fm = parse_fm(md.read_text(encoding="utf-8"))
            modified = parse_date(fm.get("modified", "") or fm.get("published", ""))
            if not modified:
                rows.append(("P1", locale, md.stem, -1, "no valid published/modified date"))
                continue
            age = (today - modified).days
            hub = fm.get("hub", "")
            prio = None
            if hub in RELEASE_HUBS and age > RELEASE_P0_DAYS:
                prio = "P0"
            elif age > STALE_P0_DAYS:
                prio = "P0"
            elif age > STALE_P1_DAYS:
                prio = "P1"
            elif age > STALE_P2_DAYS:
                prio = "P2"
            if prio:
                rows.append((prio, locale, md.stem, age, f"hub={hub or '?'} last touched {modified}"))
            if locale == "en":
                en_modified[md.stem] = modified
            else:
                translated.setdefault(md.stem, []).append((locale, modified))

    for slug, versions in sorted(translated.items()):
        src = en_modified.get(slug)
        if not src:
            continue
        for locale, mod in versions:
            lag = (src - mod).days
            if lag > LAG_DAYS:
                rows.append(("TR", locale, slug, lag, f"English source updated {src}, translation stuck at {mod}"))

    order = {"P0": 0, "P1": 1, "P2": 2, "TR": 3}
    rows.sort(key=lambda r: (order[r[0]], -r[2] if r[2] > 0 else 0))
    counts = {k: sum(1 for r in rows if r[0] == k) for k in order}

    print(f"freshness audit @ {today} — P0:{counts['P0']} P1:{counts['P1']} P2:{counts['P2']} TR:{counts['TR']}\n")
    for prio, locale, slug, age, note in rows:
        age_s = f"{age:>4}d" if age >= 0 else "   -"
        print(f"{prio}  {locale}/{slug:<55} {age_s}  {note}")

    if not rows:
        print("all content within freshness thresholds")
    return 1 if (args.strict and counts["P0"]) else 0


if __name__ == "__main__":
    sys.exit(main())
