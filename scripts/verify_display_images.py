#!/usr/bin/env python3
"""Fail when a page's social card has no title-free display variant.

Why this exists
---------------
`frontmatter.image` points at the page's social card (`/images/og/<slug>.webp`),
which has the page title painted onto the artwork by
`scripts/make_social_images.py`. That is correct for `og:image`, where the image
is the whole message, but it is wrong everywhere the page renders it: the card
heading and the `<h1>` already carry those words, so the picture read as a
duplicate of its own caption.

`displayImage()` in `components/Hero.tsx` therefore rewrites `/images/og/…` to
`/images/card/…`, the same screenshot with no painted title. That rewrite is a
pure string operation, so nothing at runtime notices when the variant is absent
— the page would simply serve a 404 for its lead image. This script is the check
that makes the invariant real.

    python3 scripts/verify_display_images.py --site-dir .
    python3 scripts/verify_display_images.py --site-dir . --json

Exits non-zero if any content file references an `/images/og/` image that has no
matching file under `/images/card/`.
"""

from __future__ import annotations

import argparse
import glob
import json
import pathlib
import re
import sys

IMAGE_LINE = re.compile(r'^image:\s*["\']?([^"\'\s]+)["\']?\s*$', re.M)
OG_IN_PATH = re.compile(r'/images/og/(.+)$')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--site-dir', default='.')
    parser.add_argument('--json', dest='json_out')
    args = parser.parse_args()

    root = pathlib.Path(args.site_dir).resolve()
    files = sorted(glob.glob(str(root / 'content' / '*' / '*.md')))
    if not files:
        print(f'error: no content found under {root / "content"}', file=sys.stderr)
        return 1

    references: dict[str, list[str]] = {}
    for name in files:
        text = pathlib.Path(name).read_text(encoding='utf-8')
        rel = str(pathlib.Path(name).relative_to(root))
        for image in IMAGE_LINE.findall(text):
            match = OG_IN_PATH.search(image)
            if match:
                references.setdefault(match.group(1), []).append(rel)

    if not references:
        print('no /images/og/ references found — nothing to check')
        return 0

    missing = {name: users for name, users in references.items() if not (root / 'public' / 'images' / 'card' / name).exists()}
    # A card variant nobody references is dead weight, not an error, but worth
    # reporting: it usually means a slug was renamed and the old file lingered.
    orphans = [
        p.name
        for p in sorted((root / 'public' / 'images' / 'card').glob('*'))
        if p.name not in references
    ] if (root / 'public' / 'images' / 'card').exists() else []

    for name, users in sorted(missing.items()):
        print(f'[fail] no display variant for {name} (used by {len(users)} file(s), e.g. {users[0]})')
    for name in orphans:
        print(f'[warn] unused display variant: {name}')

    total = len(references)
    print(f'\n{total - len(missing)}/{total} social cards have a title-free display variant')
    print(f'{len(missing)} missing, {len(orphans)} unused')

    if args.json_out:
        pathlib.Path(args.json_out).write_text(
            json.dumps({'checked': total, 'missing': sorted(missing), 'unused': orphans}, indent=2),
            encoding='utf-8',
        )
    return 1 if missing else 0


if __name__ == '__main__':
    raise SystemExit(main())
