#!/usr/bin/env python3
"""Trim over-long titles and descriptions in content frontmatter.

Search results truncate the title around 600px and the description around 920px;
text past that is invisible, so an over-long title buries its own keyword.
Translations are the usual cause — Spanish and German run 20-40% longer than
English, so a title that fits in English blows the budget once translated.

Two signals matter, and the gap between them is deliberate:

* **target** — the length that displays in full. Going over is a warning.
* **hard**  — where truncation is near-certain. Only past this is text rewritten.

Rewriting only happens past `hard`, and a rewrite must keep at least
MIN_KEEP_RATIO of the target length. If dropping clauses cannot achieve that,
the original is kept: a title with one extra clause that still displays beats a
three-word stub, and the point is discoverability, not tidiness.

The title is measured **as rendered** (frontmatter + the layout's site-name
suffix), because budgeting the frontmatter alone under-counts by ~18 characters
and ships titles that are visibly cut off.

Only `title:` and `description:` lines are touched. Slugs, hubs, dates and body
text are never modified, and nothing is reworded — clauses are only ever dropped
whole, so every remaining statement stays true. Text is never cut mid-phrase:
if no clause boundary fits the budget, the original is left alone and a rewrite
is the correct remedy (see scripts/rewrite_meta.py).

Usage:
    python3 scripts/trim_meta.py --site-dir .            # report only
    python3 scripts/trim_meta.py --site-dir . --write    # apply
"""

from __future__ import annotations

import argparse
import glob
import pathlib
import re

# `target` is the length that renders in full; `hard` is where truncation is
# near-certain and worth cutting text for. The gap is the point: a title 3
# characters over target still displays, and mangling it to hit a round number
# costs a real qualifier. Only `hard` breaches are rewritten.
LIMITS = {
    "latin": {"title": 78, "hardTitle": 90, "description": 155, "hardDescription": 172},
    # German compounds run 15-20% longer than English for the same content.
    "de": {"title": 86, "hardTitle": 100, "description": 165, "hardDescription": 180},
    # CJK budgets are page-specific: one glyph ~ two Latin characters.
    "cjk": {"title": 30, "hardTitle": 38, "description": 110, "hardDescription": 130},
}
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uac00-\ud7af]")

# Clause separators, most preferred cut point first. The full-width forms matter
# for CJK: a Japanese title separates its qualifier with "：" and no space, so
# omitting it makes the trimmer cut the whole qualifier and leave a bare game
# name (observed: "Witchbrook のコツと小技：..." -> "Witchbrook").
TITLE_BREAKS = [" — ", " – ", " | ", ": ", "：", ":", "; ", " - ", ", "]
DESC_BREAKS = [". ", "。", "; ", "；", " — ", " – ", ", ", "、"]

# A rewrite must keep at least this share of the target length, or it is not
# worth making. Without a floor the clause-dropper happily returns a stub.
MIN_KEEP_RATIO = 0.7


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


def frontmatter_limits(site_dir: pathlib.Path, path: pathlib.Path, text: str) -> dict[str, int]:
    """Length budgets expressed for the frontmatter value.

    limits_for() returns rendered budgets (what a search result shows). The
    frontmatter is shorter than the rendered title by the site-name suffix, so
    comparing the two directly let titles 15-20 characters over budget pass.
    """
    limits = dict(limits_for(path, text))
    if script_of(text, path) == "cjk":
        return limits
    reserve = len(site_name_suffix(site_dir))
    return {key: value - reserve for key, value in limits.items()}


def limits_for(path: pathlib.Path, text: str) -> dict[str, int]:
    if script_of(text, path) == "cjk":
        return LIMITS["cjk"]
    # The locale is the directory directly under content/. `path.parent.name` is
    # the wrong thing to test: for content/de/foo.md the parent is "de" only by
    # luck, but for content/legal/de/foo.md it is also "de" while the content
    # dirs sit one level deeper — checking it there silently gave German files
    # the Latin budget.
    parts = path.parts
    locale = ""
    if "content" in parts:
        index = parts.index("content")
        if index + 1 < len(parts):
            locale = parts[index + 1]
    if locale == "de":
        return LIMITS["de"]
    return LIMITS["latin"]


def site_name_suffix(site_dir: pathlib.Path) -> str:
    """Reads the suffix the layout appends to every title, from the config.

    Reading it rather than hardcoding keeps this correct when a site is renamed.
    """
    config = site_dir / "config" / "site.config.ts"
    if not config.exists():
        return ""
    match = re.search(r"fullName:\s*'([^']+)'", config.read_text(encoding="utf-8"))
    return f" - {match.group(1)}" if match else ""


def trim_title(title: str, budget: int, target: int) -> str:
    """Keeps the longest leading clause run that fits, without becoming a stub."""
    if len(title) <= budget:
        return title

    floor = int(target * MIN_KEEP_RATIO)
    best = ""
    for sep in TITLE_BREAKS:
        if sep not in title:
            continue
        parts = title.split(sep)
        # Longest prefix that fits wins, so the most information survives.
        for keep in range(len(parts) - 1, 0, -1):
            candidate = (sep if sep in {"：", ":"} else sep).join(parts[:keep]).strip()
            if len(candidate) <= budget:
                best = candidate
                break
        if best:
            break

    if best and len(best) >= floor:
        return best

    # No clause boundary landed in budget. Do NOT fall back to cutting at a word
    # boundary: that produces text like "Furniture, Layouts and" or
    # "...es el que.", which reads as broken and is worse than being long. The
    # right fix for these is a rewrite (scripts/rewrite_meta.py); until then the
    # original stays and the search engine truncates it with an ellipsis.
    return title


def trim_description(desc: str, budget: int, target: int) -> str:
    """Same policy as titles: cut at clause boundaries, never down to a stub."""
    if len(desc) <= budget:
        return desc

    floor = int(target * MIN_KEEP_RATIO)
    best = ""
    for sep in DESC_BREAKS:
        if sep not in desc:
            continue
        parts = desc.split(sep)
        for keep in range(len(parts) - 1, 0, -1):
            candidate = sep.join(parts[:keep]).strip()
            if not candidate.endswith((".", "!", "?")):
                candidate += "."
            if len(candidate) <= budget:
                best = candidate
                break
        if best:
            break

    if best and len(best) >= floor:
        return best

    # Same reasoning as titles: no mid-phrase cutting. A long, informative
    # description that the search engine trims with an ellipsis is better than a
    # sentence that stops in the middle of a clause.
    return desc


def get_field(block: str, field: str) -> str | None:
    match = re.search(rf'^{field}:\s*"?(.*?)"?\s*$', block, re.M)
    return match.group(1) if match else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--site-dir", type=pathlib.Path, default=pathlib.Path("."))
    parser.add_argument("--write", action="store_true", help="apply the edits (default is report only)")
    args = parser.parse_args()

    root = args.site_dir
    files: list[str] = []
    for pattern in ("content/*/*.md", "content/legal/*.md", "content/legal/*/*.md"):
        files.extend(glob.glob(str(root / pattern)))

    reserve_suffix = site_name_suffix(root)
    reserve = len(reserve_suffix)
    if reserve_suffix:
        print(f"title suffix reserved: {reserve} chars ({reserve_suffix!r})")

    changed = 0
    for name in sorted(set(files)):
        path = pathlib.Path(name)
        text = path.read_text(encoding="utf-8")
        head = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not head:
            continue

        original = head.group(1)
        block = original

        title = get_field(block, "title")
        desc = get_field(block, "description")
        if not title:
            continue
        limits = limits_for(path, title)

        fm = frontmatter_limits(root, path, title)
        is_cjk = script_of(title, path) == "cjk"
        title_reserve = 0 if is_cjk else reserve
        new_title = trim_title(title, fm["hardTitle"], fm["title"])
        new_desc = (
            trim_description(desc, limits["hardDescription"], limits["description"])
            if desc
            else desc
        )

        if new_title != title:
            block = re.sub(
                r"^title:\s*.*$",
                'title: "' + new_title.replace('"', '\\"') + '"',
                block, count=1, flags=re.M,
            )
        if desc and new_desc != desc:
            block = re.sub(
                r"^description:\s*.*$",
                'description: "' + new_desc.replace('"', '\\"') + '"',
                block, count=1, flags=re.M,
            )

        if block != original:
            changed += 1
            rel = path.relative_to(root)
            if new_title != title:
                unit = "chars" if is_cjk else "rendered"
                print(
                    f"  T {unit} {len(title) + title_reserve:>3}->{len(new_title) + title_reserve:<3} {rel}"
                )
            if desc and new_desc != desc:
                print(f"  D {len(desc):>3}->{len(new_desc):<3} {rel}")
            if args.write:
                path.write_text(text[: head.start(1)] + block + text[head.end(1):], encoding="utf-8")

    verb = "updated" if args.write else "would update"
    print(f"\n{verb} {changed} file(s)")
    if not args.write and changed:
        print("re-run with --write to apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
