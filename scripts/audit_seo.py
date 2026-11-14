#!/usr/bin/env python3
"""Audit a site's content for the SEO essentials that templates cannot guarantee.

Two classes of problem, both of which silently cost traffic:

1. **Title / description length.** Search results truncate around 600px for the
   title and ~920px for the description. Text past that is invisible, so a
   long title buries the very keyword it was written for. Character counts are a
   proxy for pixel width (exact width needs a font renderer) but they are the
   standard proxy and good enough to catch what matters.
   CJK is measured differently: one glyph is roughly two Latin characters wide,
   so the limits are about half.

2. **Internal links.** Google discovers pages by following links. A broken
   internal link wastes crawl budget and, repeated, damages trust in the whole
   site; a page with no inbound internal links (an orphan) is effectively
   invisible no matter how good it is. This builds the link graph from the live
   pages and reports both.

Usage:
    python3 scripts/audit_seo.py --base http://localhost:3000
    python3 scripts/audit_seo.py --base https://www.example.wiki --strict
    python3 scripts/audit_seo.py --base http://localhost:3000 --json report.json

Exit code is the number of FAIL-level problems (0 when clean).
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0 Safari/537.36"
)

# Character budgets. Widths differ enough between scripts that one number would
# either pass everything in Japanese or fail everything in German.
# IMPORTANT: every value here is the RENDERED length, i.e. what a search result
# shows, and the rendered <title> is "frontmatter - <site name>". Content authors
# edit the frontmatter, so the tools convert once (frontmatter_limits) rather
# than each of them subtracting the suffix themselves. Comparing a frontmatter
# value against a rendered budget is the mistake that let titles 15-20
# characters over slip through a check that looked correct.
# `target` renders in full; `hard` is where truncation is near-certain. The gap
# is deliberate: a title a few characters over target still displays, and
# rewriting it to hit a round number costs a real qualifier. Only `hard`
# breaches fail.
LIMITS = {
    "latin": {"title": 78, "hardTitle": 90, "description": 155, "hardDescription": 172},
    # German compounds run 15-20% longer than English for the same content.
    "de": {"title": 86, "hardTitle": 100, "description": 165, "hardDescription": 180},
    # CJK budgets are page-specific: one glyph ~ two Latin characters.
    "cjk": {"title": 30, "hardTitle": 38, "description": 110, "hardDescription": 130},
}
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uac00-\ud7af]")

# Framework-generated paths that are not content links.
ASSET_PREFIXES = ("/_next/", "/_vercel/", "/static/", "/cdn-cgi/")
ASSET_SUFFIXES = (
    ".js", ".css", ".map", ".json", ".xml", ".txt", ".png", ".jpg", ".jpeg",
    ".webp", ".avif", ".svg", ".ico", ".woff", ".woff2", ".ttf", ".mp4", ".webm",
)

results: list[tuple[str, str, str]] = []


def record(level: str, name: str, detail: str = "") -> None:
    results.append((level, name, detail))


def fetch(url: str, timeout: int = 25) -> tuple[int, str]:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as error:
        return error.code, ""
    except Exception:  # noqa: BLE001 - transport errors are reported as 0
        return 0, ""


KANA = re.compile(r"[\u3040-\u30ff]")
HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
HANGUL = re.compile(r"[\uac00-\ud7af]")
CJK_ANY = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uac00-\ud7af]")


def script_of(text: str, path: "pathlib.Path | None" = None) -> str:
    """Whether this text should be measured with the CJK budget.

    The content directory decides first. Measuring by character ratio alone
    misclassifies mixed text — an English title containing a couple of Japanese
    words ("Witchbrook のコツと小技") is predominantly Latin but scores as CJK,
    which hands it a CJK budget and silently skips it from length checks.

    With no path to go on, require real CJK prose: kana (Japanese always has it),
    hangul, or a solid majority of CJK characters.
    """
    if path is not None:
        parts = path.parts
        if "content" in parts:
            index = parts.index("content")
            if index + 1 < len(parts):
                locale = parts[index + 1]
                if locale in {"ja", "ko", "zh"}:
                    return "cjk"
                if locale in {"en", "es", "de"}:
                    return "latin"

    if HANGUL.search(text) or KANA.search(text):
        return "cjk"
    if not HAN.search(text):
        return "latin"
    cjk = len(CJK_ANY.findall(text))
    return "cjk" if cjk / max(len(text), 1) >= 0.4 else "latin"


def cjk_suffix_allowance(title: str) -> int:
    """Character budget for the site-name suffix in a rendered title.

    A rendered title is "<page title> - <site name>". For CJK pages the suffix is
    still Latin, so it costs one character per character while the page part
    costs roughly two pixels per character. The suffix is therefore charged at
    its literal length — the CJK limits already account for double-width glyphs.

    This must match trim_meta.py exactly, or the audit reports titles the
    trimmer considers fine.
    """
    match = re.search(r"\s[-–—|]\s[^-–—|]+$", title)
    return len(match.group(0)) if match else 0


def limits_for(url: str, text: str) -> dict[str, int]:
    # The URL locale segment is authoritative; see script_of().
    script = script_of(text, pathlib.PurePosixPath(urllib.parse.urlparse(url).path))
    if script == "cjk":
        base = LIMITS["cjk"]
        allowance = cjk_suffix_allowance(text)
        return {
            "title": base["title"] + allowance,
            "hardTitle": base["hardTitle"] + allowance,
            "description": base["description"],
            "hardDescription": base["hardDescription"],
        }
    if re.search(r"(^|/)de(/|$)", urllib.parse.urlparse(url).path):
        return LIMITS["de"]
    return LIMITS["latin"]


def text_of(html: str, pattern: str) -> str | None:
    match = re.search(pattern, html, re.S | re.I)
    return match.group(1).strip() if match else None


def is_internal(href: str, host: str) -> bool:
    if href.startswith(("mailto:", "tel:", "javascript:", "#")):
        return False
    if href.startswith("http"):
        return urllib.parse.urlparse(href).netloc == host
    return href.startswith("/")


def normalise(href: str) -> str:
    path = urllib.parse.urlparse(href).path or "/"
    return path.rstrip("/") or "/"


def is_asset(path: str) -> bool:
    if path.startswith(ASSET_PREFIXES):
        return True
    return path.lower().endswith(ASSET_SUFFIXES)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", required=True, help="site root, e.g. http://localhost:3000")
    parser.add_argument("--json", type=pathlib.Path, default=None, help="write the full report as JSON")
    parser.add_argument("--strict", action="store_true", help="treat length overruns as failures")
    parser.add_argument("--max-pages", type=int, default=400, help="cap pages crawled (default 400)")
    args = parser.parse_args()

    base = args.base.rstrip("/")
    host = urllib.parse.urlparse(base).netloc

    status, sitemap = fetch(f"{base}/sitemap.xml")
    if status != 200:
        print(f"error: could not read {base}/sitemap.xml (HTTP {status})", file=sys.stderr)
        return 1
    urls = [u for u in re.findall(r"<loc>([^<]+)</loc>", sitemap)]
    if not urls:
        print("error: sitemap contains no URLs", file=sys.stderr)
        return 1

    # Crawl on the audited host even though the sitemap declares the canonical one.
    pages: dict[str, tuple[str, str]] = {}
    for absolute in urls[: args.max_pages]:
        parsed = urllib.parse.urlparse(absolute)
        target = f"{base}{parsed.path}" or base
        code, html = fetch(target)
        pages[normalise(parsed.path)] = (code, html)

    print(f"auditing {base} — {len(pages)} pages\n")

    # ---------------------------------------------------------------- lengths
    long_titles: list[tuple[str, int, int, str]] = []
    long_descs: list[tuple[str, int, int, str]] = []
    borderline: list[tuple[str, int, int, str]] = []
    missing_titles, missing_descs = [], []

    for path, (code, html) in sorted(pages.items()):
        if code != 200:
            continue
        title = text_of(html, r"<title[^>]*>(.*?)</title>")
        desc = text_of(html, r'<meta[^>]+name="description"[^>]+content="([^"]*)"')
        if not title:
            missing_titles.append(path)
        if not desc:
            missing_descs.append(path)
            continue

        for value, bucket, target_key, hard_key in (
            (title, long_titles, "title", "hardTitle"),
            (desc, long_descs, "description", "hardDescription"),
        ):
            limits = limits_for(path, value)
            length = len(value)
            if length > limits[hard_key]:
                bucket.append((path, length, limits[hard_key], value))
            elif length > limits[target_key]:
                borderline.append((path, length, limits[target_key], value))

    # A missing title or description is always a defect.
    if missing_titles:
        record("FAIL", "every page has a <title>", f"{len(missing_titles)}: {missing_titles[0]}")
    else:
        record("PASS", "every page has a <title>")
    if missing_descs:
        record("FAIL", "every page has a meta description", f"{len(missing_descs)}: {missing_descs[0]}")
    else:
        record("PASS", "every page has a meta description")

    def report_length(bucket: list, name: str, noun: str) -> None:
        if bucket:
            worst = max(bucket, key=lambda r: r[1] - r[2])
            record(
                "FAIL",
                name,
                f"{len(bucket)} {noun} past the truncation point; worst {worst[1]} vs {worst[2]} — {worst[0]}",
            )
        else:
            record("PASS", name)

    report_length(long_titles, "titles will not be truncated", "titles")
    report_length(long_descs, "descriptions will not be truncated", "descriptions")

    if borderline:
        worst = max(borderline, key=lambda r: r[1] - r[2])
        record(
            "FAIL" if args.strict else "WARN",
            "length within the comfortable band",
            f"{len(borderline)} slightly over the display width (still shown in full); "
            f"worst {worst[1]} vs {worst[2]} — {worst[0]}",
        )
    else:
        record("PASS", "length within the comfortable band")

    # ------------------------------------------------------------ link graph
    known = set(pages)
    inbound: collections.Counter[str] = collections.Counter()
    dead: dict[str, set[str]] = collections.defaultdict(set)
    outbound: dict[str, int] = {}

    for path, (code, html) in pages.items():
        if code != 200:
            continue
        count = 0
        for href in re.findall(r'href="([^"]+)"', html):
            if not is_internal(href, host):
                continue
            target = normalise(href)
            if is_asset(target):
                continue
            count += 1
            if target in known:
                inbound[target] += 1
            else:
                dead[path].add(target)
        outbound[path] = count

    broken = sum(len(v) for v in dead.values())
    if broken:
        sample = next(iter(dead.items()))
        record(
            "FAIL",
            "no broken internal links",
            f"{broken} across {len(dead)} pages; e.g. {sample[0]} -> {sorted(sample[1])[0]}",
        )
    else:
        record("PASS", "no broken internal links", f"{sum(inbound.values())} links checked")

    orphans = sorted(p for p in known if inbound[p] == 0 and pages[p][0] == 200)
    if orphans:
        record("FAIL", "no orphan pages", f"{len(orphans)} with zero inbound links: {orphans[0]}")
    else:
        record("PASS", "no orphan pages")

    # One inbound link means a page is reachable only from a single place, which
    # is fragile: if that one link changes, the page drops out of the crawl.
    weak = sorted((inbound[p], p) for p in known if 0 < inbound[p] <= 1 and pages[p][0] == 200)
    if weak:
        record("WARN", "pages have more than one inbound link", f"{len(weak)} with only one, e.g. {weak[0][1]}")
    else:
        record("PASS", "pages have more than one inbound link")

    total = sum(outbound.values())
    record("PASS", "internal link density", f"{total} links, avg {total / max(len(pages), 1):.1f} per page")

    # ----------------------------------------------------------------- output
    width = max(len(name) for _, name, _ in results)
    failures = 0
    for level, name, detail in results:
        if level == "FAIL":
            failures += 1
        marker = {"PASS": "ok  ", "WARN": "warn", "FAIL": "FAIL"}[level]
        print(f"[{marker}] {name.ljust(width)}  {detail}")

    if args.json:
        args.json.write_text(
            json.dumps(
                {
                    "base": base,
                    "pages": len(pages),
                    "overlongTitles": [{"path": p, "length": n, "limit": l} for p, n, l, _ in long_titles],
                    "overlongDescriptions": [{"path": p, "length": n, "limit": l} for p, n, l, _ in long_descs],
                    "borderline": [{"path": p, "length": n, "target": l} for p, n, l, _ in borderline],
                    "brokenLinks": {p: sorted(v) for p, v in dead.items()},
                    "orphans": orphans,
                    "weaklyLinked": [p for _, p in weak],
                    "checks": [{"level": l, "name": n, "detail": d} for l, n, d in results],
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"\nreport written to {args.json}")

    print(f"\n{failures} failure(s)")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
