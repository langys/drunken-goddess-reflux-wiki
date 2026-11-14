#!/usr/bin/env python3
"""Content/media diagnostics; length is a review signal, never an SEO verdict.

Stdlib only. With --out-dir, check rendered article image duplication, reserved
image dimensions, and hreflang targets. Human review still verifies game facts.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, unquote


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.article = False
        self.images = []
        self.alternates = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'article':
            self.article = True
        if self.article and tag == 'img':
            self.images.append(a)
        if tag == 'link' and a.get('rel') == 'alternate' and a.get('hreflang'):
            self.alternates.append((a['hreflang'], a.get('href', '')))

    def handle_endtag(self, tag):
        if tag == 'article':
            self.article = False


def resolves(out, href):
    path = unquote(urlsplit(href).path).strip('/')
    return (out / path / 'index.html').is_file() or (out / (path + '.html')).is_file()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--site-dir', default='.')
    ap.add_argument('--out-dir')
    ap.add_argument('--json-out')
    args = ap.parse_args()
    root = Path(args.site_dir)
    rows, errors = [], []
    paragraphs = defaultdict(list)
    for p in sorted((root / 'content').glob('*/*.md')):
        if p.parent.name == 'legal':
            continue
        s = p.read_text(encoding='utf-8')
        body = re.sub(r'\A---\s*\n.*?\n---\s*\n', '', s, count=1, flags=re.S)
        text = re.sub(r'!?\[([^]]*)\]\([^)]+\)', r'\1', body)
        text = re.sub(r'https?://\S+', '', text)
        images = re.findall(r'!\[([^]]*)\]\(([^)]+)\)', body)
        urls = re.findall(r'https?://[^\s)<>]+', body)
        rows.append({'file': str(p.relative_to(root)), 'locale': p.parent.name,
                     'words': len(re.findall(r'\b[\w-]+\b', text)),
                     'cjk_characters': len(re.findall(r'[\u3040-\u30ff\u3400-\u9fff]', text)),
                     'body_images': len(images), 'external_sources': len(set(urls))})
        for paragraph in re.split(r'\n\s*\n', text):
            paragraph = ' '.join(paragraph.split())
            if len(paragraph) >= 160 and not paragraph.startswith(('#', '|', '-', '>', '1.')):
                paragraphs[(p.parent.name, paragraph)].append(str(p.relative_to(root)))
        if not urls:
            errors.append(f'{p.relative_to(root)}: no traceable external source')
        if len(images) != len({src for _, src in images}):
            errors.append(f'{p.relative_to(root)}: repeated body image URL')
    if not rows:
        errors.append('no articles found: check --site-dir and content/<locale>/*.md')
    assets = defaultdict(list)
    for p in (root / 'public/images').rglob('*'):
        if p.is_file():
            assets[hashlib.sha256(p.read_bytes()).hexdigest()].append(str(p.relative_to(root)))
    duplicate_assets = [paths for paths in assets.values() if len(paths) > 1]
    repeated = [{'locale': k[0], 'text': k[1], 'files': files}
                for k, files in paragraphs.items() if len(set(files)) > 1]
    rendered = {'html_files': 0, 'article_images': 0, 'broken_alternates': []}
    if args.out_dir:
        out = Path(args.out_dir)
        if not out.is_dir():
            errors.append(f'export directory does not exist: {out}')
        for p in sorted(out.rglob('*.html')):
            page = Page()
            page.feed(p.read_text(encoding='utf-8'))
            rendered['html_files'] += 1
            rendered['article_images'] += len(page.images)
            srcs = [im.get('src') for im in page.images]
            if len(srcs) != len(set(srcs)):
                errors.append(f'{p.relative_to(out)}: repeated rendered article image')
            for im in page.images:
                if not (im.get('width') and im.get('height')):
                    errors.append(f'{p.relative_to(out)}: image dimensions missing: {im.get("src")}')
            for lang, href in page.alternates:
                if not resolves(out, href):
                    rendered['broken_alternates'].append({'file': str(p.relative_to(out)), 'language': lang, 'href': href})
        if rendered['html_files'] == 0:
            errors.append('no exported HTML found: run npm run build first')
        errors.extend(f'{r["file"]}: broken hreflang {r["language"]} {r["href"]}' for r in rendered['broken_alternates'])
    report = {'articles': rows, 'duplicate_public_images': duplicate_assets,
              'repeated_paragraphs': repeated, 'rendered': rendered, 'errors': errors}
    for locale in sorted({row['locale'] for row in rows}):
        local = [row for row in rows if row['locale'] == locale]
        print(f'{locale}: {len(local)} articles; {sum(x["words"] for x in local)} body words; '
              f'{sum(x["cjk_characters"] for x in local)} CJK characters; '
              f'{sum(x["external_sources"] > 0 for x in local)} with sources; '
              f'{sum(x["body_images"] for x in local)} body images')
    print(f'Exact repeated paragraphs: {len(repeated)} (review signals, not automatic failures)')
    print(f'Duplicate public image files: {len(duplicate_assets)}')
    if args.out_dir:
        print(f'Rendered: {rendered["html_files"]} HTML files; {len(rendered["broken_alternates"])} broken hreflang targets')
    for e in errors:
        print('[fail] ' + e)
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f'{len(errors)} errors; facts and image relevance still require editorial review')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
