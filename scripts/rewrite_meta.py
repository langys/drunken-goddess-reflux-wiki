#!/usr/bin/env python3
"""Shorten over-long titles and descriptions by rewriting, not truncating.

Why this exists: cutting text to fit a character budget is the wrong fix. A
knowledgeable writer can say the same thing in fewer words, and that is the only
outcome that keeps both the length and the meaning. Chopping a trailing clause
loses a real qualifier ("Europe" is gone), and chopping at a word boundary leaves
a dangling half-phrase ("...Merits und"). Truncation is a last resort for text
that is grossly over; everything else should be rewritten.

This script builds the rewrite job and then applies the results:

    # 1. list everything that should be tightened, with its constraints
    python3 scripts/rewrite_meta.py list --site-dir . --out rewrites.json

    # 2. rewrite each `current` into `rewritten` (by hand, or by an LLM)
    #    keeping every fact, proper noun and number

    # 3. validate and apply — invalid entries are rejected, not written
    python3 scripts/rewrite_meta.py apply --site-dir . rewrites.json

Validation is deliberately strict, because a shortened title that quietly drops
a character name or invents a release date is worse than a long one. Every entry
is checked for: length budget, same language, same proper nouns, same numbers,
same URLs, and (for titles) an intact "Phrase: qualifier" shape.

Budgets are shared with audit_seo.py and trim_meta.py so all three agree on what
"too long" means.
"""

from __future__ import annotations

import argparse
import glob
import json
import pathlib
import re
import sys
import unicodedata

# `target` renders in full; `hard` is where truncation is near-certain.
LIMITS = {
    "latin": {"title": 78, "hardTitle": 90, "description": 155, "hardDescription": 172},
    # German compounds run 15-20% longer than English for the same content.
    "de": {"title": 86, "hardTitle": 100, "description": 165, "hardDescription": 180},
    # CJK budgets are page-specific: one glyph ~ two Latin characters.
    "cjk": {"title": 30, "hardTitle": 38, "description": 110, "hardDescription": 130},
}
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uac00-\ud7af]")
URL = re.compile(r"https?://\S+")
NUMBER = re.compile(r"\d[\d.,]*")

# Words that may legitimately disappear when tightening a sentence. Anything
# capitalised and not in here is treated as a proper noun that must survive.
COMMON_CAPS = {
    # en
    "a", "an", "the", "and", "or", "but", "if", "in", "on", "at", "to", "for",
    "of", "with", "from", "by", "as", "is", "are", "was", "were", "be", "been",
    "this", "that", "these", "those", "it", "its", "you", "your", "we", "our",
    "how", "what", "why", "when", "where", "which", "who", "can", "could",
    "should", "will", "would", "may", "might", "must", "not", "no", "all",
    "every", "each", "both", "more", "most", "less", "least", "before", "after",
    "during", "while", "until", "since", "than", "then", "also", "only", "even",
    "still", "yet", "here", "there", "get", "got", "make", "makes", "use",
    "using", "need", "needs", "want", "know", "find", "see", "look", "take",
    "give", "keep", "start", "guide", "guides", "tips", "tricks", "best",
    "all", "about", "into", "over", "under", "up", "down", "out", "off",
    # de
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "einen", "einem",
    "eines", "einer", "und", "oder", "aber", "wenn", "in", "im", "am", "an",
    "auf", "fur", "für", "mit", "von", "vom", "zu", "zum", "zur", "als", "ist",
    "sind", "war", "waren", "wird", "werden", "kann", "konnen", "können",
    "sich", "sie", "er", "es", "wir", "ihr", "du", "dein", "deine", "was",
    "wie", "wo", "wann", "warum", "wer", "welche", "welcher", "nicht", "kein",
    "keine", "alle", "mehr", "meiste", "vor", "nach", "wahrend", "während",
    "bis", "seit", "dann", "auch", "nur", "schon", "noch", "hier", "dort",
    "so", "um", "bei", "aus", "durch", "gegen", "ohne", "unter", "ueber",
    "über", "zwischen", "tun", "macht", "machen", "brauchen", "wissen",
    "leitfaden", "tipps", "tricks", "beste", "beste", "alle", "uber", "alles",
    # es
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "pero",
    "si", "en", "con", "de", "del", "por", "para", "como", "es", "son", "era",
    "sera", "será", "puede", "pueden", "tu", "tus", "su", "sus", "que", "qué",
    "como", "cómo", "donde", "dónde", "cuando", "cuándo", "quien", "quién",
    "no", "todo", "todos", "toda", "todas", "mas", "más", "menos", "antes",
    "despues", "después", "hasta", "desde", "entonces", "tambien", "también",
    "solo", "sólo", "aun", "aún", "aqui", "aquí", "alli", "allí", "guia",
    "guía", "guias", "guías", "consejos", "trucos", "mejores", "sobre", "entre",
    "sin", "hacia", "segun", "según",
    # ja (tokens are not capitalised, so this mainly guards latin inside ja)
    "steam", "pc",
}


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
    config = site_dir / "config" / "site.config.ts"
    if not config.exists():
        return ""
    match = re.search(r"fullName:\s*'([^']+)'", config.read_text(encoding="utf-8"))
    return f" - {match.group(1)}" if match else ""


def get_field(block: str, field: str) -> str | None:
    match = re.search(rf'^{field}:\s*"?(.*?)"?\s*$', block, re.M)
    return match.group(1) if match else None


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


def load_glossary(site_dir: pathlib.Path) -> set[str]:
    """Reads the site's proper-noun glossary, one name per line.

    Automatic detection cannot be trusted here. German capitalises every noun, so
    shape alone cannot separate "Mossport" from "Ladenbesitzer", and a heuristic
    that guesses wrong in the permissive direction silently publishes a page that
    lost a character name. An explicit list is boring and correct, and it is
    written once per site.

    Falls back to an empty set, in which case detection is shape-based and errs
    toward keeping tokens.
    """
    names: set[str] = set()
    for candidate in (
        site_dir / "config" / "proper-nouns.txt",
        site_dir / "research" / "proper-nouns.txt",
    ):
        if candidate.exists():
            for line in candidate.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    names.add(line.lower())
    return names


GLOSSARY: set[str] = set()


def proper_nouns(text: str) -> set[str]:
    """Identity-bearing tokens that must survive a rewrite.

    Matches against the glossary when there is one; otherwise falls back to
    shape, which over-keeps — a false "dropped proper noun" rejection costs one
    retry, while a false negative publishes a page missing a character name.
    """
    low = text.lower()
    found = {name for name in GLOSSARY if len(name) > 2 and noun_present(name, low)}

    if not GLOSSARY:
        for token in re.findall(r"[A-ZÄÖÜ][\w'’\-äöüß]{2,}", text):
            if token.lower() not in COMMON_CAPS:
                found.add(token)
    return found


def language_of(text: str) -> str:
    if script_of(text) == "cjk":
        return "cjk"
    lowered = f" {text.lower()} "
    de = sum(lowered.count(w) for w in (" der ", " die ", " das ", " und ", " mit ", " für ", " von ", " wie "))
    es = sum(lowered.count(w) for w in (" el ", " la ", " los ", " y ", " con ", " para ", " de ", " cómo "))
    if de > es:
        return "de"
    if es > de:
        return "es"
    return "latin"


def language_of_item(item: dict) -> str:
    """Language to validate against.

    The path is authoritative. A German description can be mostly place names
    ("Ein Rundgang durch Witchbrook, Mossport, Docklands und Shadhollow"), which
    starves the word-frequency heuristic and makes it report a language change
    that did not happen. The directory never lies.
    """
    parts = item["path"].split("/")
    if len(parts) > 2 and parts[0] == "content":
        directory = parts[1]
        if directory in {"en", "es", "de", "ja"}:
            return "cjk" if directory == "ja" else directory
        if directory == "legal":
            return language_of(item["current"])
    return language_of(item["current"])


def normalise_lead(value: str) -> str:
    """Strips what a rewrite may legitimately drop from a leading phrase.

    Particles, punctuation and spacing are not the keyword. Comparing raw strings
    rejected "Witchbrook のDiscord..." -> "Witchbrook Discord..." even though the
    keyword is identical.
    """
    lead = re.split(r"[:：]", value, 1)[0]
    lead = re.sub(r"[\s　]+", "", lead)
    lead = re.sub(r"[のをはがにでとやへも]", "", lead)
    return lead.lower()


def collect(site_dir: pathlib.Path, include_borderline: bool) -> list[dict]:
    global GLOSSARY
    GLOSSARY = load_glossary(site_dir)
    # Kept for reference in the emitted payload; the budgets already include it.
    reserve = len(site_name_suffix(site_dir))
    items: list[dict] = []
    files: list[str] = []
    for pattern in ("content/*/*.md", "content/legal/*.md", "content/legal/*/*.md"):
        files.extend(glob.glob(str(site_dir / pattern)))

    for name in sorted(set(files)):
        path = pathlib.Path(name)
        text = path.read_text(encoding="utf-8")
        head = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not head:
            continue
        block = head.group(1)
        title = get_field(block, "title")
        desc = get_field(block, "description")
        if not title:
            continue
        # Frontmatter budgets: the rendered budgets from limits_for() are larger
        # by the site-name suffix, and comparing frontmatter against those let
        # titles 15-20 characters over pass unchallenged.
        limits = frontmatter_limits(site_dir, path, title)

        for field, value, target_key, hard_key in (
            ("title", title, "title", "hardTitle"),
            ("description", desc, "description", "hardDescription"),
        ):
            if not value:
                continue
            length = len(value)
            target = limits[target_key]
            hard = limits[hard_key]
            if length > hard or (include_borderline and length > target):
                items.append(
                    {
                        "path": str(path.relative_to(site_dir)),
                        "field": field,
                        "current": value,
                        "length": length,
                        "target": target,
                        "hard": hard,
                        "over": length > hard,
                        "language": language_of(value),
                        "properNouns": sorted(proper_nouns(value)),
                        "numbers": sorted(set(NUMBER.findall(value))),
                        "urls": sorted(set(URL.findall(value))),
                    }
                )
    return items


def validate(entry: dict, item: dict) -> list[str]:
    """Rejects a rewrite that changes meaning, not just one that is too long."""
    problems: list[str] = []
    new = entry.get("rewritten", "").strip()
    if not new:
        return ["empty rewrite"]

    length = len(new) + (item["length"] - len(item["current"]))
    if length > item["target"]:
        problems.append(f"{length} chars still over target {item['target']}")
    if length < item["target"] * 0.6:
        problems.append(f"{length} chars is suspiciously short (lost content?)")

    # Only a *confident* mismatch is a problem. A name-dense sentence scores zero
    # for every language ("Ein Rundgang durch Witchbrook: Witchbrook College,
    # Student Village, Docklands, ..."), and treating "inconclusive" as "changed"
    # rejected a correct German rewrite.
    expected = language_of_item(item)
    detected = language_of(new)
    if detected != "latin" and detected != expected:
        problems.append(f"language changed: {expected} -> {detected}")

    # Identity must survive: a shortened title that drops a character name is a
    # different page as far as a reader (and a search engine) is concerned.
    lowered = new.lower()
    for noun in item["properNouns"]:
        if not noun_present(noun, lowered):
            problems.append(f"proper noun dropped: {noun}")
    for number in item["numbers"]:
        if number not in new:
            problems.append(f"number dropped: {number}")
    for url in item["urls"]:
        if url not in new:
            problems.append(f"URL dropped: {url}")

    if item["field"] == "title" and len(item["properNouns"]) > 0:
        # Keep the front-loaded keyword: the rewrite must still start with the
        # same leading phrase, just continued more economically.
        lead_before = normalise_lead(item["current"])
        lead_after = normalise_lead(new)
        if lead_before and lead_after and lead_before[:10] != lead_after[:10]:
            problems.append(
                f"leading keyword changed: {lead_before[:40]!r} -> {lead_after[:40]!r}"
            )

    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="emit the rewrite queue")
    p_list.add_argument("--site-dir", type=pathlib.Path, default=pathlib.Path("."))
    p_list.add_argument("--out", type=pathlib.Path, required=True)
    p_list.add_argument(
        "--include-borderline",
        action="store_true",
        help="also queue items that still display in full but exceed the target",
    )

    p_apply = sub.add_parser("apply", help="validate and write rewrites")
    p_apply.add_argument("queue", type=pathlib.Path)
    p_apply.add_argument("--site-dir", type=pathlib.Path, default=pathlib.Path("."))
    p_apply.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    if args.command == "list":
        items = collect(args.site_dir, args.include_borderline)
        payload = {
            "instruction": (
                "Rewrite each `current` so it fits `target` characters while keeping every fact, "
                "proper noun, number and URL. Do not truncate and do not drop a qualifier: find "
                "shorter wording for the same claim. Keep the leading keyword phrase of a title "
                "intact, and keep the \"Phrase: qualifier\" shape. Write `rewritten` next to "
                "`current` and leave everything else untouched."
            ),
            "count": len(items),
            "items": items,
        }
        args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        over = sum(1 for i in items if i["over"])
        print(f"wrote {args.out}: {len(items)} item(s) — {over} past the truncation point")
        for item in items[:10]:
            tag = "OVER" if item["over"] else "warn"
            print(f"  [{tag}] {item['field']:<11} {item['length']:>3}/{item['target']:<3} {item['path']}")
        return 0

    # apply
    payload = json.loads(args.queue.read_text(encoding="utf-8"))
    items = {f"{i['path']}|{i['field']}": i for i in payload.get("items", [])}
    applied = rejected = 0
    for entry in payload.get("items", []):
        if "rewritten" not in entry:
            continue
        key = f"{entry['path']}|{entry['field']}"
        item = items[key]

        # Idempotent: if the field already holds the rewrite, there is nothing to
        # do. Without this, re-running the same queue validates the rewritten
        # text against its own constraints and reports false failures.
        path = args.site_dir / entry["path"]
        existing = get_field(
            re.match(r"^---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.S).group(1),
            entry["field"],
        )
        if existing == entry["rewritten"]:
            print(f"  skip {key} (already applied)")
            continue

        problems = validate(entry, item)
        if problems:
            rejected += 1
            print(f"  REJECT {key}")
            for problem in problems[:4]:
                print(f"         {problem}")
            continue

        path = args.site_dir / entry["path"]
        text = path.read_text(encoding="utf-8")
        head = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        block = head.group(1)
        new_block = re.sub(
            rf'^{entry["field"]}:\s*.*$',
            f'{entry["field"]}: "' + entry["rewritten"].replace('"', '\\"') + '"',
            block, count=1, flags=re.M,
        )
        applied += 1
        delta = len(entry["rewritten"]) - len(entry["current"])
        print(f"  {'would ' if args.dry_run else ''}apply {key}  {len(entry['current'])}->{len(entry['rewritten'])} ({delta:+d})")
        if not args.dry_run:
            path.write_text(text[: head.start(1)] + new_block + text[head.end(1):], encoding="utf-8")

    print(f"\n{applied} applied, {rejected} rejected")
    return 1 if rejected else 0


if __name__ == "__main__":
    raise SystemExit(main())
