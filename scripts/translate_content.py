#!/usr/bin/env python3
"""Translate guide content into another locale, with structural validation.

`locales: ['en','es','de']` in the config is a promise the site makes. If
the translations do not exist, the language switcher is a dead control and the
site silently is not multilingual. This makes translating a first-class,
repeatable step rather than something an operator is expected to remember:

    # 1. what is missing, or stale because the English changed
    python3 scripts/translate_content.py status --site-dir .

    # 2. emit translation jobs, split per locale and batch
    python3 scripts/translate_content.py plan --site-dir . --locale es --out es.json

    # 3. translate every `english` value into the target locale

    # 4. validate and write; anything that breaks the contract is rejected
    python3 scripts/translate_content.py apply --site-dir . es.json

The contract is enforced, not trusted. A translated file is rejected when:
  * `slug`, `hub`, `published`, `modified` or `image` differ from the source
    (slug drift silently breaks the URL and the hreflang cluster)
  * the markdown structure changes (heading levels, table shape, bullet counts)
  * a URL is altered or dropped
  * a proper noun from config/proper-nouns.txt is missing
  * the title or description lands outside its length budget
  * the body is suspiciously short relative to the source

Values are compared with the *directory* locale, and CJK budgets are applied to
ja/ko/zh, matching audit_seo.py and rewrite_meta.py so all tools agree.
"""

from __future__ import annotations

import argparse
import glob
import json
import pathlib
import re
import sys

# Rendered budgets, same numbers as audit_seo.py / rewrite_meta.py.
LIMITS = {
    "latin": {"title": 78, "hardTitle": 90, "description": 155, "hardDescription": 172},
    "de": {"title": 86, "hardTitle": 100, "description": 165, "hardDescription": 180},
    "cjk": {"title": 30, "hardTitle": 38, "description": 110, "hardDescription": 130},
}
CJK_LOCALES = {"ja", "ko", "zh"}
KANA = re.compile(r"[\u3040-\u30ff]")
HANGUL = re.compile(r"[\uac00-\ud7af]")
HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
CJK_ANY = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uac00-\ud7af]")
URL = re.compile(r"https?://\S+")
NUMBER = re.compile(r"\d[\d.,]*")

# Frontmatter keys copied verbatim. Translating any of these breaks routing.
FROZEN = ("slug", "hub", "published", "modified", "image")
# Keys that must be translated.
TRANSLATABLE_SCALAR = ("title", "description")
TRANSLATABLE_LIST = ("quickGuide",)
# Bulk prose can legitimately differ in length; this is the sanity floor.
MIN_BODY_RATIO = 0.45
# A Japanese/Korean/Chinese page carries roughly 2-3 non-space characters per
# English word (measured on the house-style ja pages: 2.56-3.29), so a word-count
# floor would reject every correct CJK translation.
MIN_CJK_CHARS_PER_WORD = 1.6


def script_of(text: str, path: pathlib.Path | None = None) -> str:
    if path is not None:
        parts = path.parts
        if "content" in parts:
            index = parts.index("content")
            if index + 1 < len(parts) and parts[index + 1] in CJK_LOCALES:
                return "cjk"
    if HANGUL.search(text) or KANA.search(text):
        return "cjk"
    if not HAN.search(text):
        return "latin"
    return "cjk" if len(CJK_ANY.findall(text)) / max(len(text), 1) >= 0.4 else "latin"


def limits_for(locale: str, text: str, path: pathlib.Path | None = None) -> dict[str, int]:
    if locale in CJK_LOCALES or script_of(text, path) == "cjk":
        return LIMITS["cjk"]
    if locale == "de":
        return LIMITS["de"]
    return LIMITS["latin"]


def site_name_suffix(site_dir: pathlib.Path) -> str:
    config = site_dir / "config" / "site.config.ts"
    if not config.exists():
        return ""
    match = re.search(r"fullName:\s*'([^']+)'", config.read_text(encoding="utf-8"))
    return f" - {match.group(1)}" if match else ""


def load_glossary(site_dir: pathlib.Path) -> set[str]:
    names: set[str] = set()
    for candidate in (site_dir / "config" / "proper-nouns.txt", site_dir / "research" / "proper-nouns.txt"):
        if candidate.exists():
            for line in candidate.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    names.add(line.lower())
    return names


def split_frontmatter(text: str) -> tuple[str, str] | None:
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    return (match.group(1), match.group(2)) if match else None


def field(block: str, key: str) -> str | None:
    """Reads a scalar frontmatter value.

    A literal `null` reads as absent. Some locales wrote `modified: null` where
    the source omits the key, and returning the string "null" made `status`
    report every such file permanently stale.
    """
    match = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', block, re.M)
    if not match:
        return None
    value = match.group(1).strip()
    return None if value in ("", "null", "~") else value


LIST_KEY = re.compile(r"^(\s*)(\w+):\s*$", re.M)


def harvest_lists(block: str) -> dict[str, int]:
    """Item count of each list-valued frontmatter key (quickGuide, cards, faq).

    Counts top-level dash items only, where "top-level" means more indented than
    the key itself. A stricter pattern that required every continuation line to
    begin with "-" collapsed the nested `cards`/`faq` mappings to 1 while
    `quickGuide` (plain strings) counted correctly — so the two were compared
    against different baselines. These lists drive rendered sections, so a lost
    item drops a section rather than merely shortening prose.
    """
    counts: dict[str, int] = {}
    for match in LIST_KEY.finditer(block):
        indent, key = len(match.group(1)), match.group(2)
        rest = block[match.end():]
        total = 0
        for line in rest.splitlines():
            if not line.strip():
                continue
            line_indent = len(line) - len(line.lstrip())
            if line_indent <= indent:
                break
            if line_indent == indent + 2 and re.match(r"^\s*-\s+", line):
                total += 1
        if total:
            counts[key] = total
    return counts


def body_blocks(body: str) -> dict:
    """Shape fingerprint of the markdown, used to detect a lossy translation."""
    headings = re.findall(r"^(#{1,6})\s+(.+)$", body, re.M)
    rows = [line for line in body.splitlines() if line.strip().startswith("|")]
    bullets = [line for line in body.splitlines() if re.match(r"^\s*[-*]\s+", line)]
    return {
        "headingLevels": [level for level, _ in headings],
        "headingCount": len(headings),
        "tableRows": len(rows),
        "bullets": len(bullets),
        "words": len(body.split()),
    }


def collect_sources(site_dir: pathlib.Path, source: str) -> dict[str, dict]:
    sources: dict[str, dict] = {}
    for name in sorted(glob.glob(str(site_dir / "content" / source / "*.md"))):
        path = pathlib.Path(name)
        raw = path.read_text(encoding="utf-8")
        parts = split_frontmatter(raw)
        if not parts:
            continue
        block, body = parts
        sources[path.name] = {"block": block, "body": body, "shape": body_blocks(body)}
    return sources


def configured_locales(site_dir: pathlib.Path, exclude: str = "") -> list[str]:
    """Locale list from site.config.ts, falling back to content directories."""
    config = site_dir / "config" / "site.config.ts"
    if config.exists():
        match = re.search(r"locales:\s*\[([^\]]*)\]", config.read_text(encoding="utf-8"))
        if match:
            found = re.findall(r"'([^']+)'", match.group(1))
            if found:
                return [loc for loc in found if loc != exclude]
    return [
        part.name
        for part in sorted((site_dir / "content").iterdir())
        if part.is_dir() and part.name not in {"legal", exclude}
    ]


def lists_untranslated(target_block: str, source_block: str, locale: str) -> bool:
    """Whether a translated page is missing its frontmatter lists, or still has
    them in English.

    Counting files is not enough: a page whose `quickGuide`/`cards`/`faq` blocks
    were dropped renders without its quick-guide callout, cards and FAQ, and one
    whose blocks are still English renders them in the wrong language. Both look
    "translated" by file count.
    """
    for key in harvest_lists(source_block):
        found = harvest_lists(target_block).get(key, 0)
        if found < harvest_lists(source_block)[key]:
            return True

        match = re.search(rf"^{key}:\n((?:[ \t]+.*\n)+)", target_block, re.M)
        if not match:
            return True
        body = match.group(1)
        if locale in CJK_LOCALES:
            if not KANA.search(body) and not HANGUL.search(body):
                return True
        else:
            # Latin locales: an English block has no locale-specific function
            # words, so a very low count means it was never translated.
            low = body.lower()
            markers = {
                "de": (" der ", " die ", " das ", " und ", " mit ", " für "),
                "es": (" el ", " la ", " los ", " y ", " con ", " para "),
            }.get(locale, ())
            if markers and sum(low.count(m) for m in markers) < 2:
                return True
    return False


def cmd_status(args) -> int:
    sources = collect_sources(args.site_dir, args.source)
    # Report what the site is CONFIGURED for, not what directories happen to
    # exist. Listing only existing directories made a site with four configured
    # locales and zero translations report nothing at all, which is exactly the
    # state where the operator most needs to be told.
    locales = args.locales or configured_locales(args.site_dir, exclude=args.source)
    if not locales:
        print("no non-default locales configured; nothing to translate", file=sys.stderr)
        return 0
    print(f"source: content/{args.source} ({len(sources)} files)\n")
    incomplete = 0
    for locale in locales:
        done = {
            pathlib.Path(name).name
            for name in glob.glob(str(args.site_dir / "content" / locale / "*.md"))
        }
        missing = sorted(set(sources) - done)
        stale: list[str] = []
        untranslated_lists: list[str] = []
        for name in sorted(set(sources) & done):
            target = args.site_dir / "content" / locale / name
            text = target.read_text(encoding="utf-8")
            parts = split_frontmatter(text)
            if not parts:
                stale.append(name)
                continue
            block = parts[0]
            if any(
                field(block, key) != field(sources[name]["block"], key) for key in FROZEN
            ):
                stale.append(name)
                continue
            # A file can be "translated" while its frontmatter lists are missing
            # or still English. Those lists drive rendered sections (quick-guide
            # callout, cards, FAQ), so this is a real gap, not a cosmetic one —
            # and it is invisible from the file count alone.
            if lists_untranslated(block, sources[name]["block"], locale):
                untranslated_lists.append(name)

        state = "ok" if not missing and not stale and not untranslated_lists else "incomplete"
        if state != "ok":
            incomplete += 1
        print(f"  {locale:5s} {len(done):>3}/{len(sources)} translated  [{state}]")
        if missing:
            print(f"        missing {len(missing)}: {', '.join(missing[:3])}{' ...' if len(missing) > 3 else ''}")
        if stale:
            print(f"        stale frontmatter {len(stale)}: {', '.join(stale[:3])}")
        if untranslated_lists:
            print(
                f"        frontmatter lists missing/untranslated {len(untranslated_lists)}: "
                f"{', '.join(untranslated_lists[:3])}"
            )
    return 0 if incomplete == 0 else 1


def cmd_plan(args) -> int:
    sources = collect_sources(args.site_dir, args.source)
    target_dir = args.site_dir / "content" / args.locale
    glossary = load_glossary(args.site_dir)
    suffix = site_name_suffix(args.site_dir)
    reserve = 0 if args.locale in CJK_LOCALES else len(suffix)

    items = []
    for name, src in sorted(sources.items()):
        if (target_dir / name).exists() and not args.force:
            continue
        limits = limits_for(args.locale, field(src["block"], "title") or "", None)
        # Word-boundary match, so "unity" is only checked when the page really
        # names Unity rather than saying "community".
        nouns = sorted({n for n in glossary if noun_present(n, (src["body"] + src["block"]).lower())})
        items.append(
            {
                "file": name,
                "english": split_frontmatter(
                    (args.site_dir / "content" / args.source / name).read_text(encoding="utf-8")
                )[1],
                "frontmatter": {
                    key: field(src["block"], key) for key in FROZEN
                },
                "title": field(src["block"], "title"),
                "description": field(src["block"], "description"),
                # Harvest per key. A bare bullet scrape counted quickGuide +
                # cards + faq together (13 for this template), and the validator
                # then demanded that many quickGuide items — rejecting correct
                # translations that localise the three blocks separately.
                "frontmatterLists": harvest_lists(src["block"]),
                "targetLocale": args.locale,
                "titleBudget": limits["title"] - reserve,
                "descriptionBudget": limits["description"],
                "properNouns": nouns,
                "shape": src["shape"],
            }
        )
        if args.batch and len(items) >= args.batch:
            break

    payload = {
        "instruction": (
            f"Translate every English string into {args.locale}. Do not summarise, do not drop a "
            "clause and do not add facts. If a constraint seems impossible to satisfy honestly, "
            "report it instead of working around it: never add a sentence to make a check pass. "
            "Keep each `frontmatter` value byte-identical in the "
            "output file, but DO translate the structured frontmatter lists (quickGuide, cards, "
            "faq), keeping each list's item count and its keys. "
            "Keep markdown structure identical: same headings (translated text), same "
            "table shape, same bullet counts, same bold usage. Preserve every URL and every proper "
            "noun verbatim in its original script. Titles must fit titleBudget characters and "
            "descriptions must fit descriptionBudget."
        ),
        "locale": args.locale,
        "count": len(items),
        "items": items,
    }
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {args.out}: {len(items)} file(s) to translate into {args.locale}")
    for item in items[:8]:
        print(f"  {item['file']}")
    return 0


def validate(item: dict, translated: str, site_dir: pathlib.Path, glossary: set[str]) -> list[str]:
    """Rejects a translation that breaks routing, structure or facts."""
    problems: list[str] = []
    parts = split_frontmatter(translated)
    if not parts:
        return ["no frontmatter block"]
    block, body = parts
    locale = item["targetLocale"]

    for key, expected in item["frontmatter"].items():
        actual = field(block, key)
        if expected and actual != expected:
            problems.append(f"{key} changed: {expected!r} -> {actual!r}")

    shape = body_blocks(body)
    for key in ("headingCount", "tableRows", "bullets"):
        if shape[key] != item["shape"][key]:
            problems.append(f"structure changed: {key} {item['shape'][key]} -> {shape[key]}")

    # Script-aware length floor. `body.split()` counts whitespace tokens, and
    # Japanese prose has no spaces, so every ja file measured ~0.1 of the English
    # count and a correct translation was rejected as "summarised". CJK is
    # measured in non-space characters against a per-word ratio instead.
    source_words = item["shape"]["words"]
    if source_words:
        if script_of(translated) == "cjk":
            measured = len(re.sub(r"\s", "", body))
            floor = source_words * MIN_CJK_CHARS_PER_WORD
        else:
            measured = shape["words"]
            floor = source_words * MIN_BODY_RATIO
        if measured < floor:
            problems.append(
                f"body too short: {measured} vs floor {floor:.0f} "
                f"(possible summarising)"
            )

    src_urls = set(URL.findall(json.dumps(item, ensure_ascii=False)))
    missing_urls = [u for u in src_urls if u not in translated]
    if missing_urls:
        problems.append(f"URL dropped: {missing_urls[0]}")

    lowered = translated.lower()
    for noun in item["properNouns"]:
        if not noun_present(noun, lowered):
            problems.append(f"proper noun missing: {noun}")

    title = field(block, "title") or ""
    desc = field(block, "description") or ""
    if title and len(title) > item["titleBudget"]:
        problems.append(f"title {len(title)} over budget {item['titleBudget']}")
    if desc and len(desc) > item["descriptionBudget"]:
        problems.append(f"description {len(desc)} over budget {item['descriptionBudget']}")

    # Each list-valued block must keep its item count: they drive the page
    # template (quick-guide callout, cards, FAQ), so losing items silently drops
    # rendered sections rather than just shortening prose.
    got_lists = harvest_lists(block)
    for key, expected in (item.get("frontmatterLists") or {}).items():
        got = got_lists.get(key, 0)
        if got < expected:
            problems.append(f"{key} items {expected} -> {got}")

    # Japanese prose is written without spaces, but the CJK length floor is
    # measured in non-space characters, so an agent can clear it by inserting
    # 分かち書き spaces. That is a rendering artefact, not a translation, and it
    # ships silently: two published files carried a space before "の" after a
    # date. Only flag the unambiguous shape (a space between two CJK characters
    # that follows a digit, i.e. a date) so that legitimate mixed-script spacing
    # such as "Unity で" or "SSD を" is left alone.
    if script_of(translated) == "cjk":
        # U+3000 (ideographic space) is legitimate Japanese spacing — "2026年9月29日　の"
        # is correct — while an ASCII space or tab in the same place is the 分かち書き
        # artefact that lets a machine translation clear the character floor. So match
        # `\d ... \s ... CJK` across a digit-containing run and then inspect the
        # whitespace, rather than matching only `\d\s+`: the space in "2026年9月29日 の"
        # follows 日, not the digit, so a `\d\s+` pattern never fires on a real date.
        # The trailing class excludes U+3000 and U+3001 (、), which are punctuation and
        # legitimate, not artefacts.
        artefact = next(
            (
                m
                for m in re.finditer(r"\d[\d\u3040-\u30ff\u4e00-\u9fff]*?(\s+)[\u3040-\u30ff\u4e00-\u9fff]", body)
                if not m.group(1).strip(" \t")  # ASCII space/tab only, not U+3000
            ),
            None,
        )
        if artefact:
            start = max(0, artefact.start() - 12)
            problems.append(f"stray space after a number: ...{body[start:artefact.end() + 12]}...")

    return problems


def noun_present(noun: str, text: str) -> bool:
    """Whether a proper noun appears as a word, not as a substring.

    Plain `in` matching produced false passes and forced translators into awkward
    glosses: "unity" matched inside "community", and "windows" matched the common
    noun in "40 UI windows". Word boundaries fix both, and matter because these
    names are the fact-sensitive part of the page.
    """
    if re.search(r"[^\x00-\x7f]", noun):
        return noun in text
    return re.search(rf"(?<![\w-]){re.escape(noun)}(?![\w-])", text) is not None


def cmd_apply(args) -> int:
    payload = json.loads(args.queue.read_text(encoding="utf-8"))
    glossary = load_glossary(args.site_dir)
    target_dir = args.site_dir / "content" / payload["locale"]
    target_dir.mkdir(parents=True, exist_ok=True)

    written = rejected = 0
    for item in payload["items"]:
        translated = item.get("translated")
        if not translated:
            continue
        problems = validate(item, translated, args.site_dir, glossary)
        if problems:
            rejected += 1
            print(f"  REJECT {item['file']}")
            for problem in problems[:4]:
                print(f"         {problem}")
            continue
        (target_dir / item["file"]).write_text(translated.rstrip("\n") + "\n", encoding="utf-8")
        written += 1
        print(f"  wrote content/{payload['locale']}/{item['file']}")

    print(f"\n{written} written, {rejected} rejected")
    return 1 if rejected else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_status = sub.add_parser("status", help="what is missing or stale per locale")
    p_status.add_argument("--site-dir", type=pathlib.Path, default=pathlib.Path("."))
    p_status.add_argument("--source", default="en")
    p_status.add_argument("--locales", nargs="*", default=None)

    p_plan = sub.add_parser("plan", help="emit translation jobs")
    p_plan.add_argument("--site-dir", type=pathlib.Path, default=pathlib.Path("."))
    p_plan.add_argument("--source", default="en")
    p_plan.add_argument("--locale", required=True)
    p_plan.add_argument("--out", type=pathlib.Path, required=True)
    p_plan.add_argument("--batch", type=int, default=0, help="cap how many files to include")
    p_plan.add_argument("--force", action="store_true", help="re-emit files that already exist")

    p_apply = sub.add_parser("apply", help="validate and write translations")
    p_apply.add_argument("queue", type=pathlib.Path)
    p_apply.add_argument("--site-dir", type=pathlib.Path, default=pathlib.Path("."))

    args = parser.parse_args()
    if args.command == "status":
        return cmd_status(args)
    if args.command == "plan":
        return cmd_plan(args)
    return cmd_apply(args)


if __name__ == "__main__":
    raise SystemExit(main())
