#!/usr/bin/env python3
"""Pull official media for a game from the Steam API and write it into site.config.ts.

Everything here is first-party (the same payload the store page renders), so no
scraped or third-party imagery enters the site. Images and video are hot-linked
from the publisher's CDN rather than committed to the repo.

Note on trailers: Steam's public payload no longer carries an `mp4` field, only
`dash_*`/`hls_*` manifests — but the files are still served at the legacy
`cdn.akamai.steamstatic.com/steam/apps/<movieId>/movie480.mp4` path, so the movie
*id* is what we store and the component builds the URL. If the developer also
publishes on YouTube, pass `--youtube` and that source is used instead.

Usage:
    python3 scripts/fetch_steam_media.py --appid 1846700 --site-dir .
    python3 scripts/fetch_steam_media.py --appid 3373500 --youtube vlpiYIcfReE
    python3 scripts/fetch_steam_media.py --appid 1846700 --print   # preview only
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

API = "https://store.steampowered.com/api/appdetails?appids={appid}&l=english"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0 Safari/537.36"
)

MEDIA_BLOCK = re.compile(r"  media: \{.*?\n  \},", re.S)


def fetch(appid: str) -> dict:
    request = urllib.request.Request(API.format(appid=appid), headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)

    entry = payload.get(str(appid)) or {}
    if not entry.get("success"):
        raise SystemExit(f"Steam returned no data for appid {appid} (check the id)")
    return entry["data"]


def ts(value: str) -> str:
    return json.dumps(value or "")


def pick_trailer(movies: list[dict], preferred: str | None) -> dict | None:
    """Prefer an explicitly named trailer, then Steam's own `highlight` flag."""
    if preferred:
        for movie in movies:
            if preferred.lower() in (movie.get("name") or "").lower():
                return movie
    for movie in movies:
        if movie.get("highlight"):
            return movie
    return movies[0] if movies else None


def build_block(data: dict, appid: str, youtube: str | None) -> tuple[str, dict]:
    name = data.get("name", "Game")
    movies = data.get("movies") or []
    screenshots = data.get("screenshots") or []

    trailer = pick_trailer(movies, None)
    movie_id = str(trailer.get("id")) if trailer and trailer.get("id") else ""
    poster = (trailer or {}).get("thumbnail", "")
    # Keep Steam's own thumbnail path. The tempting "upgrade" to movie_max.jpg is a
    # trap: that file returns 404 on the same CDN prefix, so the home-page trailer
    # poster renders as a broken image. Verified against app 1488490 on 2026-09-14.

    credit = (data.get("developers") or [""])[0]

    shots = [
        {"url": shot.get("path_full", ""), "alt": f"{name} gameplay screenshot {index + 1}"}
        for index, shot in enumerate(screenshots[:6])
        if shot.get("path_full")
    ]

    lines = [
        "  media: {",
        f"    youtubeId: {ts(youtube or '')},",
        f"    steamMovieId: {ts(movie_id)},",
        f"    trailerTitle: {ts((trailer or {}).get('name', ''))},",
        f"    trailerCredit: {ts(credit)},",
        f"    trailerPoster: {ts(poster)},",
        "    screenshots: [",
    ]
    for shot in shots:
        lines.append(f"      {{ url: {ts(shot['url'])}, alt: {ts(shot['alt'])} }},")
    lines.append("    ] as { url: string; alt: string }[],")
    lines.append("  },")

    summary = {
        "name": name,
        "movieId": movie_id,
        "youtube": youtube or "",
        "trailerName": (trailer or {}).get("name", ""),
        "shots": len(shots),
        "shotTotal": len(screenshots),
        "movies": len(movies),
    }
    return "\n".join(lines), summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--appid", required=True, help="Steam app id, e.g. 1846700")
    parser.add_argument("--youtube", default=None, help="YouTube video id for the official trailer, if any")
    parser.add_argument("--site-dir", type=pathlib.Path, default=pathlib.Path("."))
    parser.add_argument("--print", dest="preview", action="store_true", help="preview without writing")
    args = parser.parse_args()

    try:
        data = fetch(args.appid)
    except urllib.error.URLError as error:
        print(f"error: could not reach Steam: {error}", file=sys.stderr)
        return 1

    block, summary = build_block(data, args.appid, args.youtube)

    if args.preview:
        print(block)
        return 0

    config = args.site_dir / "config" / "site.config.ts"
    if not config.exists():
        print(f"error: {config} not found", file=sys.stderr)
        return 1

    text = config.read_text(encoding="utf-8")
    if not MEDIA_BLOCK.search(text):
        print(
            "error: could not find the `media: { ... },` block in site.config.ts.\n"
            "       Restore it from the skill template, then re-run.",
            file=sys.stderr,
        )
        return 1

    # Splice by index rather than regex substitution: the block contains nested
    # braces (`screenshots: [ { ... } ]`), so a whole-match replace is easier to
    # get wrong than a plain start/end slice.
    match = MEDIA_BLOCK.search(text)
    assert match is not None
    updated = text[: match.start()] + block + text[match.end() :]
    config.write_text(updated, encoding="utf-8")

    print(f"updated {config}")
    print(f"  game        : {summary['name']}")
    print(f"  trailer     : {summary['trailerName'] or '(none)'}")
    print(f"  source      : {'youtube ' + summary['youtube'] if summary['youtube'] else 'steam movie ' + (summary['movieId'] or '(none)')}")
    print(f"  screenshots : {summary['shots']} kept of {summary['shotTotal']}")
    if not summary["youtube"] and not summary["movieId"]:
        print("  note: no trailer found; the video block will not render")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
