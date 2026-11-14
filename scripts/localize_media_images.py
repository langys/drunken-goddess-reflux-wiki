#!/usr/bin/env python3
"""Save configured media images locally without changing their bytes (stdlib only).

Run after fetch_steam_media.py. Only trailerPoster and screenshot URL literals
inside the media block are changed. Original URLs, dimensions and SHA-256 hashes
are recorded in docs/local-media-images.json. Download failures leave config intact.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import pathlib
import re
import struct
import urllib.request

MEDIA = re.compile(r"  media: \{.*?\n  \},", re.S)
IMAGE = re.compile(r"\b(?:trailerPoster|url):\s*(['\"])(.*?)\1")
MAX_BYTES = 20 * 1024 * 1024


def image_info(data: bytes) -> tuple[str, int, int]:
    if data.startswith(b"\x89PNG\r\n\x1a\n") and data[12:16] == b"IHDR":
        width, height = struct.unpack(">II", data[16:24])
        return "png", width, height
    if data.startswith(b"\xff\xd8"):
        offset = 2
        while offset + 4 <= len(data):
            if data[offset] != 0xFF:
                break
            while offset < len(data) and data[offset] == 0xFF:
                offset += 1
            marker = data[offset]
            offset += 1
            if marker in (0xD9, 0xDA):
                break
            length = int.from_bytes(data[offset:offset + 2], "big")
            if length < 2 or offset + length > len(data):
                break
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                          0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                height, width = struct.unpack(">HH", data[offset + 3:offset + 7])
                return "jpg", width, height
            offset += length
    raise ValueError("Expected a valid JPEG or PNG image")


def download(url: str) -> tuple[str, bytes, dict]:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError(f"Image exceeds 20 MiB: {url}")
    extension, width, height = image_info(data)
    if width <= 0 or height <= 0:
        raise ValueError(f"Invalid dimensions: {url}")
    digest = hashlib.sha256(data).hexdigest()
    path = f"/images/media/official-{digest[:16]}.{extension}"
    return url, data, {"sourceUrl": url, "path": path, "width": width,
                       "height": height, "bytes": len(data), "sha256": digest}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=pathlib.Path, default=pathlib.Path("."))
    args = parser.parse_args()
    root = args.site_dir.resolve()
    config = root / "config" / "site.config.ts"
    text = config.read_text(encoding="utf-8")
    match = MEDIA.search(text)
    if not match:
        raise ValueError("Missing media block in config/site.config.ts")
    block = match.group()
    values = [value for _, value in IMAGE.findall(block) if value]
    for value in values:
        if value.startswith("/"):
            if not (root / "public" / value.lstrip("/")).is_file():
                raise FileNotFoundError(f"Missing local image: {value}")
        elif not value.startswith("https://"):
            raise ValueError(f"Expected a local path or HTTPS image: {value}")
    urls = list(dict.fromkeys(value for value in values if value.startswith("https://")))
    if not urls:
        print(f"All {len(values)} configured media images are local; no changes")
        return 0

    # Fetch independent assets first; write references only after all succeed.
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        images = list(pool.map(download, urls))
    manifest_path = root / "docs" / "local-media-images.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else []
    entries = {entry["path"]: entry for entry in manifest}
    for url, data, entry in images:
        destination = root / "public" / entry["path"].lstrip("/")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        block = block.replace(url, entry["path"])
        entries[entry["path"]] = entry
        print(f"{entry['path']} ({entry['width']}x{entry['height']}, {len(data):,} bytes)")
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(list(entries.values()), indent=2) + "\n", encoding="utf-8")
    config.write_text(text[:match.start()] + block + text[match.end():], encoding="utf-8")
    print(f"Localized {len(images)} images; originals preserved byte for byte")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
