#!/usr/bin/env python3
"""Run similarweb-extractor to fetch keyword intelligence and search volume.

Automates keyword generator (phrase match, related keywords, trending, questions)
and keyword overview (search volume, trends, CPC, competitors) for a target game.

Usage:
    python3 scripts/fetch_similarweb.py "<keyword>"
    python3 scripts/fetch_similarweb.py "Drunken Goddess Reflux" --country 999 --out-dir research
"""

from __future__ import annotations

import argparse
import os
import pathlib
import subprocess
import sys


def find_similarweb_extractor() -> pathlib.Path | None:
    # 1. Check user gemini config skills
    home = pathlib.Path.home()
    candidates = [
        home / ".gemini" / "config" / "skills" / "similarweb-extractor" / "scripts" / "extract.js",
        pathlib.Path("/Users/langyongshan/.gemini/config/skills/similarweb-extractor/scripts/extract.js"),
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch SimilarWeb keyword data for game wiki site.")
    parser.add_argument("keyword", help="Target keyword/game name (e.g. 'Drunken Goddess Reflux')")
    parser.add_argument("--country", default="999", help="Country code (999=Worldwide, 840=US, default: 999)")
    parser.add_argument("--out-dir", default="research", help="Output directory (default: research)")
    args = parser.parse_args()

    extractor_js = find_similarweb_extractor()
    if not extractor_js:
        print("ERROR: similarweb-extractor script not found.", file=sys.stderr)
        print("Expected at: ~/.gemini/config/skills/similarweb-extractor/scripts/extract.js", file=sys.stderr)
        return 1

    out_path = pathlib.Path(args.out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    print(f"[*] Running similarweb-extractor for: '{args.keyword}'")
    print(f"[*] Output directory: {out_path.resolve()}")

    # 1. Run keyword-generator
    cmd_gen = [
        "node",
        str(extractor_js),
        "keyword-generator",
        "--keyword",
        args.keyword,
        "--country",
        args.country,
        "--tabs",
        "all",
        "--output-dir",
        str(out_path),
        "--format",
        "both",
    ]
    print(f"[1/2] Fetching keyword lists (phrase match, related, trending, questions)...")
    res_gen = subprocess.run(cmd_gen)
    if res_gen.returncode != 0:
        print(f"[!] Warning: keyword-generator exited with code {res_gen.returncode}", file=sys.stderr)

    # 2. Run keyword-overview
    cmd_ov = [
        "node",
        str(extractor_js),
        "keyword-overview",
        "--keyword",
        args.keyword,
        "--country",
        args.country,
        "--output-dir",
        str(out_path),
        "--format",
        "both",
    ]
    print(f"[2/2] Fetching keyword overview (volume, trends, competitors)...")
    res_ov = subprocess.run(cmd_ov)
    if res_ov.returncode != 0:
        print(f"[!] Warning: keyword-overview exited with code {res_ov.returncode}", file=sys.stderr)

    print(f"[+] SimilarWeb extraction complete! Files written to: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
