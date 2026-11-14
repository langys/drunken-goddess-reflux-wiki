#!/usr/bin/env python3
"""Check unique ad keys and pre-rendered Native destinations (stdlib only)."""
import argparse
from html.parser import HTMLParser
from pathlib import Path


class AdParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.keys = set()
        self.duplicates = set()
        self.native_keys = set()
        self.ids = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        identifier = attrs.get('id')
        if identifier:
            self.ids[identifier] = self.ids.get(identifier, 0) + 1
        key = attrs.get('data-ad-placement')
        if not key:
            return
        if key in self.keys:
            self.duplicates.add(key)
        self.keys.add(key)
        if attrs.get('data-ad-format') == 'native':
            self.native_keys.add(key)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out-dir', default='out')
    root = Path(parser.parse_args().out_dir)
    pages = list(root.rglob('*.html'))
    if not pages:
        print(f'ERROR: no exported pages in {root}; build first')
        return 1
    errors = 0
    for page in pages:
        ads = AdParser()
        ads.feed(page.read_text(encoding='utf-8'))
        for key in sorted(ads.duplicates):
            print(f'DUPLICATE AD KEY {key}: {page.relative_to(root)}')
            errors += 1
        for key in sorted(ads.native_keys):
            count = ads.ids.get(f'container-{key}', 0)
            if count != 1:
                print(f'NATIVE TARGET COUNT {count} for {key}: {page.relative_to(root)}')
                errors += 1
    print(f'check-ads: {len(pages)} pages; {errors} ad key/container errors')
    return int(errors > 0)


if __name__ == '__main__':
    raise SystemExit(main())
