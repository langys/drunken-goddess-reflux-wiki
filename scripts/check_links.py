#!/usr/bin/env python3
"""check_links.py — link health scan over the built site (out/).

Run AFTER `npm run build`. Two checks:

1. Dead internal links. Extracts href="/..." from every HTML file and verifies
   the target exists as either out/<path>.html or out/<path>/index.html. Asset
   paths (files with an extension under /_next, /images, icons, etc.) are
   checked with a plain filesystem exists() instead.

2. Header nav links present. Every page that renders a <header> must carry a
   real <a href> for each configured hub (plus /articles) inside that header.
   This catches regressions where nav items stop being links — e.g. rendered
   as <button>s whose dropdown links are only mounted when open. That is the
   2026-10-17 incident: the dead-link pass had zero signal, because a missing
   link is not a dead link. Expected URLs are read from
   config/site.config.ts, so the gate adapts to any hub set automatically.

Exit 1 when any dead link or missing nav link is found. Inspired by AnvilWiki's
check-links gate.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

HREF_RE = re.compile(r'href="(/[^"#?]*)"')
HREF_ANY_RE = re.compile(r'href="([^"]*)"')
HEADER_RE = re.compile(r"<header\b[\s\S]*?</header>", re.IGNORECASE)
SKIP_PREFIXES = ("/_next/",)

# --- nav expectations, read from the site's single source of truth ----------
HUB_RE = re.compile(r"^\s{4}(\w+): \{ label: '[^']*', href: '([^']+)'", re.M)
LOCALES_RE = re.compile(r"locales:\s*\[([^\]]*)\]")
DEFAULT_LOCALE_RE = re.compile(r"defaultLocale:\s*'([^']+)'")
NAV_EXTRA: tuple[str, ...] = ()  # site-specific extra header routes, if any


def route_exists(out: pathlib.Path, path: str) -> bool:
    p = path.rstrip("/")
    if p == "":
        return (out / "index.html").exists()
    candidate = out / p.lstrip("/")
    if candidate.suffix:  # asset-like path (/favicon.ico, /ads.txt, /search-index.json)
        return candidate.exists()
    return (
        (out / f"{p.lstrip('/')}.html").exists()
        or (candidate / "index.html").exists()
    )


def load_nav_expectations(site_dir: pathlib.Path) -> tuple[list[str], set[str], str]:
    """Hub hrefs + configured locales + default locale from site.config.ts."""
    cfg = (site_dir / "config" / "site.config.ts").read_text(encoding="utf-8")
    hubs = [m.group(2) for m in HUB_RE.finditer(cfg)]
    m = LOCALES_RE.search(cfg)
    locales = set(re.findall(r"'([^']+)'", m.group(1))) if m else set()
    d = DEFAULT_LOCALE_RE.search(cfg)
    default_locale = d.group(1) if d else "en"
    return hubs, locales, default_locale


def nav_prefix_for(rel: pathlib.Path, locales: set[str], default_locale: str) -> str:
    """Locale prefix under which this page's header links live.

    next-intl `localePrefix: 'as-needed'` — the default locale has no prefix,
    every other locale prefixes its links, so expectations differ per page.
    """
    first = rel.parts[0] if rel.parts else ""
    if first in locales and first != default_locale:
        return f"/{first}"
    return ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--site-dir", default=".")
    args = ap.parse_args()
    out = pathlib.Path(args.out_dir).resolve()
    if not out.is_dir():
        print(f"ERROR: {out} not found — run `npm run build` first", file=sys.stderr)
        return 2

    hubs, locales, default_locale = load_nav_expectations(pathlib.Path(args.site_dir))
    if not hubs:
        print("ERROR: could not read hubs from config/site.config.ts", file=sys.stderr)
        return 2
    expected_suffixes = [*hubs, *NAV_EXTRA]

    dead: dict[str, set[str]] = {}
    nav_gaps: dict[str, set[str]] = {}
    checked = 0
    header_pages = 0
    index_has_header = False

    for html in out.rglob("*.html"):
        rel = html.relative_to(out)
        text = html.read_text(encoding="utf-8", errors="replace")

        for href in set(HREF_RE.findall(text)):
            if href.startswith(SKIP_PREFIXES) or href.startswith("//"):
                continue
            checked += 1
            if not route_exists(out, href):
                dead.setdefault(href, set()).add(str(rel))

        blocks = HEADER_RE.findall(text)
        if not blocks:
            continue
        header_pages += 1
        if str(rel) == "index.html":
            index_has_header = True
        prefix = nav_prefix_for(rel, locales, default_locale)
        present: set[str] = set()
        for block in blocks:
            present.update(HREF_ANY_RE.findall(block))
        for suffix in expected_suffixes:
            expected = f"{prefix}{suffix}"
            if expected not in present:
                nav_gaps.setdefault(expected, set()).add(str(rel))

    for href in sorted(dead):
        sources = sorted(dead[href])
        print(f"DEAD  {href}  <- {sources[0]}" + (f" (+{len(sources)-1} more)" if len(sources) > 1 else ""))
    for expected in sorted(nav_gaps):
        sources = sorted(nav_gaps[expected])
        print(f"MISSING nav link {expected}  <- {sources[0]}" + (f" (+{len(sources)-1} more)" if len(sources) > 1 else ""))

    missing_index_header = header_pages > 0 and not index_has_header
    if missing_index_header:
        print("MISSING <header> on index.html — the site header did not render on the home page")

    print(
        f"\ncheck-links: {checked} internal links checked, {len(dead)} dead target(s), "
        f"{len(nav_gaps)} missing nav link(s) across {header_pages} page(s) with <header>"
    )
    return 1 if (dead or nav_gaps or missing_index_header) else 0


if __name__ == "__main__":
    sys.exit(main())
