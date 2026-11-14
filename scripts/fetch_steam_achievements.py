#!/usr/bin/env python3
"""Fetch Steam achievement data (definitions + global unlock rates) for a game.

WHY THIS SCRIPT EXISTS (measured 2026-10):
The Steam Community achievements page is now a React app. Parsing the legacy
`achieveRow` markup returns ZERO rows with no error at all — a scraper that
"worked" before will now silently produce empty data. This script reads the
page's embedded dehydrated state instead:

  * achievement definitions — {"internal_key":256,"api_name":"1","name":...,
    "description":...,"hidden":true}
  * global rates             — "percentages":{"256":87.9,...}
    (the embedded JSON uses mixed escaping; normalize \\" back to " first)

Every entry is cross-checked against the keyless official Web API
(ISteamUserStats/GetGlobalAchievementPercentagesForApp). Both channels are
public and need no API key. The legacy markup parse is kept as a fallback.

Display semantics of the redesigned page (relevant when writing content):
hidden achievements are collapsed into a "N hidden achievements" summary row;
expanding shows masked "Hidden achievement" rows whose names/details sit
behind a per-item "Click to reveal spoilers" toggle. Unlock rates stay visible.

Usage:
  python3 fetch_steam_achievements.py --appid 4231820 -o research/steam-achievements-2026-10-17.json
  python3 fetch_steam_achievements.py --appid 4231820 --print     # stdout only

Exit code 1 when nothing was parsed (structure changed again — inspect first).
Pure stdlib, no dependencies — matches the skill's no-pip rule.
"""

import argparse
import html as html_lib
import json
import re
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

UA = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131 Safari/537.36"
    )
}
PAGE_URL = "https://steamcommunity.com/stats/{appid}/achievements/?l=english"
API_URL = (
    "https://api.steampowered.com/ISteamUserStats/"
    "GetGlobalAchievementPercentagesForApp/v2/?gameid={appid}"
)


def fetch(url, tries=3, timeout=45):
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001 — retry any transport error
            last = exc
            if attempt + 1 < tries:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"fetch failed after {tries} tries: {url} ({last})")


def _unescape(value):
    if "\\u" in value:
        try:
            return value.encode().decode("unicode_escape")
        except Exception:  # noqa: BLE001
            return value
    return value


def _grab_balanced(text, start):
    """Brace-match from text[start] == '{' (string-aware)."""
    depth, i, in_str, esc = 0, start, False, False
    while i < len(text):
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[start : i + 1]
        i += 1
    return None


def parse_page_state(html):
    """Extract achievements from the React page's embedded dehydrated state."""
    text = html.replace('\\"', '"').replace("\\\\", "\\")
    defs = {}
    pattern = re.compile(
        r'\{"internal_key":(\d+),"api_name":"([^"]*)",'
        r'"name":"((?:[^"\\]|\\.)*)","description":"((?:[^"\\]|\\.)*)",'
        r'"hidden":(true|false)'
    )
    for m in pattern.finditer(text):
        key = int(m.group(1))
        defs[key] = {
            "internal_key": key,
            "api_name": m.group(2),
            "name": _unescape(m.group(3)),
            "description": _unescape(m.group(4)) or None,
            "hidden": m.group(5) == "true",
        }
    best = {}
    for m in re.finditer(r'"percentages":', text):
        brace = text.find("{", m.end())
        frag = _grab_balanced(text, brace) if brace != -1 else None
        if not frag:
            continue
        try:
            data = json.loads(frag)
        except json.JSONDecodeError:
            continue
        if len(data) > len(best):
            best = data
    items = []
    for key, entry in defs.items():
        entry = dict(entry)
        entry["percent"] = round(float(best.get(str(key), 0.0)), 1)
        items.append(entry)
    return items


def parse_legacy_markup(html):
    """Fallback for the pre-redesign page markup (achieveRow blocks)."""
    out = []
    seen = set()
    for block in html.split("achieveRow")[1:]:
        name_m = re.search(r"<h3>(.*?)</h3>", block, re.S)
        if not name_m:
            continue
        name = html_lib.unescape(re.sub(r"<[^>]+>", "", name_m.group(1))).strip()
        if not name or name in seen:
            continue
        seen.add(name)
        desc_m = re.search(r"<h5>(.*?)</h5>", block, re.S)
        desc = (
            html_lib.unescape(re.sub(r"<[^>]+>", "", desc_m.group(1))).strip()
            if desc_m
            else ""
        )
        pct_m = re.search(r'class="achievePercent">\s*([\d.]+)%', block)
        out.append(
            {
                "internal_key": None,
                "api_name": None,
                "name": name,
                "description": desc or None,
                "hidden": not desc,
                "percent": float(pct_m.group(1)) if pct_m else 0.0,
            }
        )
    return out


def fetch_api(appid):
    data = json.loads(fetch(API_URL.format(appid=appid)))
    return data["achievementpercentages"]["achievements"]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--appid", required=True, help="Steam app id, e.g. 4231820")
    parser.add_argument("-o", "--output", help="write a JSON snapshot to this path")
    parser.add_argument(
        "--print",
        dest="print_only",
        action="store_true",
        help="print the table and exit without writing a file",
    )
    args = parser.parse_args()

    html = fetch(PAGE_URL.format(appid=args.appid))
    items = parse_page_state(html)
    source_note = "embedded dehydrated state"
    if not items:
        print(
            "WARNING: embedded-state parse returned 0 entries — "
            "falling back to legacy achieveRow markup",
            file=sys.stderr,
        )
        items = parse_legacy_markup(html)
        source_note = "legacy achieveRow markup (fallback)"
    if not items:
        print(
            "ERROR: no achievements parsed from either format. The page "
            "structure may have changed again — inspect the raw HTML before "
            "trusting any output.",
            file=sys.stderr,
        )
        return 1

    api = fetch_api(args.appid)
    api_map = {a["name"]: float(a["percent"]) for a in api}
    matched, mismatches = 0, []
    for it in items:
        ref = api_map.get(it.get("api_name")) if it.get("api_name") else None
        if ref is None:
            continue
        matched += 1
        if abs(it["percent"] - round(ref, 1)) > 0.15:
            mismatches.append((it["name"], it["percent"], round(ref, 1)))

    print(f"achievements: {len(items)}  (source: {source_note})")
    print(
        f"api cross-check: {matched}/{len(items)} matched by api_name, "
        f"{len(mismatches)} mismatch(es)"
    )
    for name, page_v, api_v in mismatches:
        print(f"  MISMATCH {name}: page={page_v} api={api_v}")
    print()
    print(f"{'rate':>6}  {'hidden':<6} name")
    print("-" * 68)
    for it in sorted(items, key=lambda x: x["percent"], reverse=True):
        flag = "hidden" if it["hidden"] else ""
        print(f"{it['percent']:>6}  {flag:<6} {it['name']}")

    if args.output and not args.print_only:
        out = {
            "source": PAGE_URL.format(appid=args.appid),
            "appid": int(args.appid),
            "count": len(items),
            "fetched": datetime.now().strftime("%Y-%m-%d"),
            "note": (
                "Built from the community page's embedded state (React app "
                "since Oct 2026); cross-checked against "
                "GetGlobalAchievementPercentagesForApp."
            ),
            "items": items,
            "api_percentages": [
                {"name": a["name"], "percent": str(a["percent"])} for a in api
            ],
        }
        Path(args.output).write_text(
            json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"\nsaved: {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
