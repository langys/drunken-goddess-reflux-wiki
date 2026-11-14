#!/usr/bin/env python3
"""indexnow.py — IndexNow key management + sitemap submission.

Design borrowed from AnvilWiki (scripts/submit-indexnow.ts), adapted to this
repo's stdlib-only Python convention:

  * Single identity: repo-root `.indexnow-key` (64 hex chars). First `init`
    generates it, every later run reuses it byte-for-byte. COMMIT this file —
    the key is public by design (it is served at /<key>.txt) and committing
    keeps local runs and CI on the same identity.
  * `init` also writes `public/<key>.txt` (content = the key), which Next.js
    copies to `out/` on build, so the key file is live after the next deploy.
  * `submit` reads the PRODUCTION sitemap (fallback: local out/sitemap.xml
    with --local) and POSTs the URL list to api.indexnow.org with exponential
    backoff on 429/5xx. Network/HTTP failures never fail the deploy: the
    command exits 0 after reporting. Missing key = zero requests, silent skip.

Usage:
  python3 scripts/indexnow.py init   --site-dir .
  python3 scripts/indexnow.py submit --site-dir . [--local] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import secrets
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request

KEY_FILE = ".indexnow-key"
KEY_RE = re.compile(r"^[0-9a-f]{64}$")
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"
MAX_URLS_PER_REQUEST = 10_000
RETRYABLE = {429, 500, 502, 503, 504}
BACKOFF_SECONDS = [5, 15, 45]


def read_key(site_dir: pathlib.Path) -> str | None:
    f = site_dir / KEY_FILE
    if not f.exists():
        return None
    key = f.read_text(encoding="utf-8").strip()
    return key if KEY_RE.match(key) else None


def site_url(site_dir: pathlib.Path) -> str:
    cfg = (site_dir / "config" / "site.config.ts").read_text(encoding="utf-8")
    m = re.search(r"url: '(https://[^']+)'", cfg)
    if not m:
        raise SystemExit("ERROR: could not parse url from config/site.config.ts")
    return m.group(1).rstrip("/")


def cmd_init(site_dir: pathlib.Path) -> int:
    existing = read_key(site_dir)
    key = existing or secrets.token_hex(32)
    (site_dir / KEY_FILE).write_text(key + "\n", encoding="utf-8")

    # Remove stale key files from public/ (rotation), then write the current one.
    public = site_dir / "public"
    for old in public.glob("*.txt"):
        if KEY_RE.match(old.stem) and old.stem != key:
            old.unlink()
            print(f"removed stale key file public/{old.name}")
    (public / f"{key}.txt").write_text(key, encoding="utf-8")

    print(("reused existing" if existing else "generated new") + f" key: {key[:12]}…")
    print(f"wrote {KEY_FILE} and public/{key}.txt — commit both; key file goes live on next deploy")
    return 0


def fetch_sitemap_urls(base: str) -> list[str]:
    # A browser UA is required: Cloudflare's bot protection (Browser Integrity
    # Check / Bot Fight Mode) 403s the default `Python-urllib/3.x` agent even
    # for public files like sitemap.xml.
    req = urllib.request.Request(
        f"{base}/sitemap.xml",
        headers={"User-Agent": "Mozilla/5.0 (compatible; IndexNowSubmit/1.0; +https://api.indexnow.org/)"},
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            xml = resp.read().decode("utf-8", errors="replace")
    except Exception:
        # Robust fallback to curl if Python TLS handshake is interrupted by platform SSL
        res = subprocess.run(
            ["curl", "-sL", "-A", "Mozilla/5.0 (compatible; IndexNowSubmit/1.0; +https://api.indexnow.org/)", f"{base}/sitemap.xml"],
            capture_output=True,
            text=True,
            check=True,
        )
        xml = res.stdout
    return re.findall(r"<loc>(https://[^<]+)</loc>", xml)


def local_sitemap_urls(site_dir: pathlib.Path) -> list[str]:
    xml = (site_dir / "out" / "sitemap.xml").read_text(encoding="utf-8")
    return re.findall(r"<loc>(https://[^<]+)</loc>", xml)


def post_batch(payload: dict) -> int:
    req = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except urllib.error.URLError as e:
        print(f"  network error: {e.reason}", file=sys.stderr)
        return -1


def cmd_submit(site_dir: pathlib.Path, local: bool, dry_run: bool) -> int:
    key = read_key(site_dir)
    if not key:
        print("indexnow: no .indexnow-key — run `npm run indexnow:init` first; skipping (0 requests)")
        return 0
    base = site_url(site_dir)
    host = re.sub(r"^https://", "", base)

    try:
        urls = local_sitemap_urls(site_dir) if local else fetch_sitemap_urls(base)
    except Exception as e:
        print(f"indexnow: could not read sitemap ({e}); skipping without failing the deploy", file=sys.stderr)
        return 0
    if not urls:
        print("indexnow: sitemap contained no URLs; nothing to submit")
        return 0

    key_location = f"{base}/{key}.txt"
    print(f"indexnow: submitting {len(urls)} URL(s) for host {host}"
          + (" (dry-run)" if dry_run else ""))
    if dry_run:
        for u in urls[:10]:
            print(f"  {u}")
        if len(urls) > 10:
            print(f"  … and {len(urls) - 10} more")
        return 0

    submitted = 0
    for i in range(0, len(urls), MAX_URLS_PER_REQUEST):
        batch = urls[i : i + MAX_URLS_PER_REQUEST]
        payload = {"host": host, "key": key, "keyLocation": key_location, "urlList": batch}
        status = -1
        for attempt, wait in enumerate([0] + BACKOFF_SECONDS):
            if wait:
                print(f"  retry in {wait}s (attempt {attempt + 1})…")
                time.sleep(wait)
            status = post_batch(payload)
            if status not in RETRYABLE and status != -1:
                break
        if status in (200, 202):
            submitted += len(batch)
            print(f"  batch ok ({len(batch)} URLs, HTTP {status})")
        else:
            # Never fail the deploy on submission problems — Bing throttling a
            # new site is normal and must not block releases.
            print(f"  batch FAILED (HTTP {status}) after retries; continuing", file=sys.stderr)
    print(f"indexnow: {submitted}/{len(urls)} URL(s) submitted")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["init", "submit"])
    ap.add_argument("--site-dir", default=".")
    ap.add_argument("--local", action="store_true", help="read out/sitemap.xml instead of the production sitemap")
    ap.add_argument("--dry-run", action="store_true", help="list URLs without POSTing")
    args = ap.parse_args()
    site_dir = pathlib.Path(args.site_dir).resolve()

    if args.command == "init":
        return cmd_init(site_dir)
    return cmd_submit(site_dir, args.local, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
