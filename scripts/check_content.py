#!/usr/bin/env python3
"""check_content.py — content lint for the markdown guides (inspired by
AnvilWiki's scripts/check-content.ts, adapted to this repo's structure).

Rules (E = error, exit 1; W = warning, report only):

  E1  body must not contain an H1 (`# ...`) — H1 is rendered from frontmatter title
  W2  heading levels must not skip (h2 -> h4)
  E3  every markdown image needs alt text
  W4  each article should link to >=3 internal pages (anti orphan-page)
  E5  internal links must resolve to a real route of the same locale
  E6  non-default-locale bodies must prefix internal links with /<locale>/
  E7  frontmatter title: required, <=80 chars (warn <20)
  E8  frontmatter description: required, 40-165 chars
  E9  frontmatter hub must exist in config/site.config.ts `hubs`
  E10 frontmatter slug must equal the file name
  E11 published/modified must be ISO dates (YYYY-MM-DD)
  W12 no duplicate title/description across articles (same locale)
  W13 quickGuide + faq recommended (AI-answer & rich-result readiness)
  W14 non-default locales should achieve 1:1 guide parity with default locale
  E15 frontmatter image must resolve to an existing local file under public/
  E16 in-article markdown images must resolve to existing files under public/
  E17 anti "全屏都是一个图": no single cover image can be reused across >25% of guides (min 4 guides)
  W18 in-article screenshots recommended for rich visual presentation (图文并茂)

Stdlib only, like the rest of scripts/. Run: python3 scripts/check_content.py --site-dir .
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
SCALAR_RE = re.compile(r"^([A-Za-z_][\w]*):\s*(?:\"([^\"]*)\"|'([^']*)'|([^#\n]+?))\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s")
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\((/[^)\s]*)\)")
HUBS_RE = re.compile(r"^\s{4}(\w+): \{ label: '[^']*', href: '([^']+)'", re.M)
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

LEGAL_ROUTES = ["/about", "/contact", "/privacy", "/terms", "/search"]
TITLE_MAX = 80
DESC_MIN, DESC_MAX = 40, 165
MIN_INTERNAL_LINKS = 3


def parse_scalar_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Extract simple `key: value` scalars; list/nested values are ignored
    (presence can still be probed via `key:` prefix lines)."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        s = SCALAR_RE.match(line)
        if s:
            fm[s.group(1)] = next(g for g in s.groups()[1:] if g is not None)
    return fm, text[m.end():]


def strip_code_fences(body: str) -> str:
    return re.sub(r"```.*?```", "", body, flags=re.S)


def load_hubs(site_dir: pathlib.Path) -> dict[str, str]:
    cfg = (site_dir / "config" / "site.config.ts").read_text(encoding="utf-8")
    return {m.group(1): m.group(2) for m in HUBS_RE.finditer(cfg)}


def load_locales(site_dir: pathlib.Path) -> tuple[str, list[str]]:
    cfg = (site_dir / "config" / "site.config.ts").read_text(encoding="utf-8")
    default = re.search(r"defaultLocale: '(\w+)'", cfg)
    locales = re.search(r"locales: \[([^\]]+)\]", cfg)
    loc_list = re.findall(r"'(\w+)'", locales.group(1)) if locales else ["en"]
    return (default.group(1) if default else "en"), loc_list


def build_routes(site_dir: pathlib.Path, hubs: dict[str, str], default: str, locale: str) -> set[str]:
    """All valid internal routes for one locale (no trailing slash)."""
    prefix = "" if locale == default else f"/{locale}"
    routes = {prefix or "/", f"{prefix}/"}
    for href in hubs.values():
        routes.add(f"{prefix}{href}")
    content_dir = site_dir / "content" / locale
    hub_by_slug: dict[str, str] = {}
    if content_dir.is_dir():
        for md in content_dir.glob("*.md"):
            fm, _ = parse_scalar_frontmatter(md.read_text(encoding="utf-8"))
            hub = fm.get("hub", "")
            if hub in hubs:
                hub_by_slug[fm.get("slug", md.stem)] = hubs[hub]
        for slug, hub_href in hub_by_slug.items():
            routes.add(f"{prefix}{hub_href}/{slug}")
    for legal in LEGAL_ROUTES:
        routes.add(f"{prefix}{legal}")
    return routes


def check_file(md: pathlib.Path, locale: str, default: str, hubs: dict[str, str], routes: set[str], site_dir: pathlib.Path | None = None):
    errors: list[str] = []
    warnings: list[str] = []
    text = md.read_text(encoding="utf-8").replace("\r\n", "\n")
    fm, body = parse_scalar_frontmatter(text)
    body = strip_code_fences(body)

    if not fm:
        errors.append("missing or malformed frontmatter block")
        return errors, warnings, fm

    # E7 / E8 — title & description
    title = fm.get("title", "")
    if not title:
        errors.append("frontmatter: title is required")
    elif len(title) > TITLE_MAX:
        errors.append(f"title is {len(title)} chars (max {TITLE_MAX})")
    elif len(title) < 20:
        warnings.append(f"title is only {len(title)} chars — too short to rank")
    desc = fm.get("description", "")
    if not desc:
        errors.append("frontmatter: description is required")
    elif not (DESC_MIN <= len(desc) <= DESC_MAX):
        errors.append(f"description is {len(desc)} chars (must be {DESC_MIN}-{DESC_MAX})")

    # E9 — hub
    hub = fm.get("hub", "")
    if hub not in hubs:
        errors.append(f"hub '{hub}' not defined in config/site.config.ts hubs {sorted(hubs)}")

    # E10 — slug == filename
    slug = fm.get("slug", "")
    if slug and slug != md.stem:
        errors.append(f"slug '{slug}' != file name '{md.stem}' (URL would drift from manifest)")

    # E11 — ISO dates
    for key in ("published", "modified"):
        val = fm.get(key)
        if key == "published" and not val:
            errors.append("frontmatter: published date is required")
        if val and not ISO_DATE_RE.match(val):
            errors.append(f"{key} '{val}' is not ISO YYYY-MM-DD")

    # E15 — frontmatter cover image existence
    cover = fm.get("image", "").strip()
    if cover:
        clean_cover = cover.split()[0].strip("\"'")
        if clean_cover.startswith("/") and site_dir:
            img_path = site_dir / "public" / clean_cover.lstrip("/")
            if not img_path.is_file():
                errors.append(f"frontmatter image '{clean_cover}' does not exist under public/")

    # E1 — no H1 in body
    for i, line in enumerate(body.splitlines(), 1):
        if line.startswith("# "):
            errors.append(f"body line {i}: H1 found — H1 comes from frontmatter title, start at H2")
            break

    # W2 — heading skips
    prev = 0
    for line in body.splitlines():
        h = HEADING_RE.match(line)
        if h:
            level = len(h.group(1))
            if prev and level > prev + 1:
                warnings.append(f"heading skips h{prev} -> h{level}: '{line.strip()[:50]}'")
            prev = level

    # E3 / E16 / W18 — images
    markdown_images = IMG_RE.findall(body)
    for alt, src in markdown_images:
        if not alt.strip():
            errors.append(f"image without alt text: {src[:60]}")
        clean_src = src.split()[0].strip("\"'")
        if clean_src.startswith("/") and site_dir:
            img_path = site_dir / "public" / clean_src.lstrip("/")
            if not img_path.is_file():
                errors.append(f"in-article image '{clean_src}' does not exist under public/")
    if len(markdown_images) == 0:
        warnings.append("no in-article images or screenshots found — recommend adding illustrations (图文并茂) for reader engagement")

    # W4 / E5 / E6 — internal links
    links = MD_LINK_RE.findall(body)
    internal = [l.split("#")[0].rstrip("/") or "/" for l in links]
    if len(internal) < MIN_INTERNAL_LINKS:
        warnings.append(f"only {len(internal)} internal link(s) (<{MIN_INTERNAL_LINKS}) — orphan-page risk")
    prefix = "" if locale == default else f"/{locale}"
    for link in internal:
        if locale != default and not (link == prefix or link.startswith(prefix + "/")):
            errors.append(f"internal link '{link}' missing '/{locale}/' prefix (would serve the English page)")
            continue
        if link not in routes:
            errors.append(f"internal link '{link}' does not resolve to a real {locale} route")

    # W13 — AI-answer readiness
    raw_fm = text[: text.find("---", 3)] if text.startswith("---") else ""
    if "quickGuide:" not in raw_fm:
        warnings.append("no quickGuide block — missing Quick Answer / AI-overview candidate")
    if "faq:" not in raw_fm:
        warnings.append("no faq block — missing FAQ rich-result candidate")

    return errors, warnings, fm


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-dir", default=".")
    args = ap.parse_args()
    site_dir = pathlib.Path(args.site_dir).resolve()

    hubs = load_hubs(site_dir)
    if not hubs:
        print("ERROR: could not parse hubs from config/site.config.ts", file=sys.stderr)
        return 2
    default, locales = load_locales(site_dir)

    total_e = total_w = files = 0
    seen: dict[str, dict[str, str]] = {}  # locale -> {title/desc -> slug}
    covers_by_locale: dict[str, dict[str, list[str]]] = {}  # locale -> {cover -> [slugs]}
    locale_file_counts: dict[str, int] = {}

    for locale in locales:
        content_dir = site_dir / "content" / locale
        if not content_dir.is_dir():
            continue
        routes = build_routes(site_dir, hubs, default, locale)
        seen.setdefault(locale, {})
        covers_by_locale.setdefault(locale, {})
        locale_files = sorted(content_dir.glob("*.md"))
        locale_file_counts[locale] = len(locale_files)

        for md in locale_files:
            files += 1
            errors, warnings, fm = check_file(md, locale, default, hubs, routes, site_dir)
            for key in ("title", "description"):
                val = fm.get(key, "")
                if val:
                    owner = seen[locale].get(val)
                    if owner:
                        warnings.append(f"duplicate {key} also used by '{owner}'")
                    else:
                        seen[locale][val] = md.stem
            cover = fm.get("image", "").strip()
            if cover:
                clean_cover = cover.split()[0].strip("\"'")
                covers_by_locale[locale].setdefault(clean_cover, []).append(md.stem)
            for msg in errors:
                total_e += 1
                print(f"ERROR   {locale}/{md.name}: {msg}")
            for msg in warnings:
                total_w += 1
                print(f"WARN    {locale}/{md.name}: {msg}")

    # E17: Anti "全屏都是一个图" / Image Diversity Gate
    for locale, covers in covers_by_locale.items():
        total_in_locale = locale_file_counts.get(locale, 0)
        if total_in_locale >= 4:
            for cover, slugs in sorted(covers.items()):
                count = len(slugs)
                ratio = count / total_in_locale
                if count > 3 and ratio > 0.25:
                    total_e += 1
                    print(
                        f"ERROR   {locale}: Image duplication / low visual diversity (E17): cover '{cover}' "
                        f"is reused by {count}/{total_in_locale} articles ({slugs[:4]}...). "
                        f"Each article must have distinct or topic-matched artwork — do not reuse hero or placeholder image everywhere (全屏都是一个图)."
                    )

    # W14: Multilingual 1:1 Parity check
    default_dir = site_dir / "content" / default
    default_slugs = {md.stem for md in default_dir.glob("*.md")} if default_dir.is_dir() else set()
    for loc in locales:
        if loc == default:
            continue
        loc_dir = site_dir / "content" / loc
        if not loc_dir.is_dir():
            total_w += 1
            print(f"WARN    {loc}: configured in siteConfig.locales but content/{loc} directory is missing")
            continue
        loc_slugs = {md.stem for md in loc_dir.glob("*.md")}
        missing = default_slugs - loc_slugs
        if missing:
            total_w += 1
            print(f"WARN    {loc}: missing {len(missing)} guide(s) from default '{default}' (breaks 1:1 multilingual parity): {sorted(missing)}")

    print(f"\ncheck-content: {files} files, {total_e} error(s), {total_w} warning(s)")
    return 1 if total_e else 0


if __name__ == "__main__":
    sys.exit(main())
