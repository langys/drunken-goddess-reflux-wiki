"""Check actual encoded favicon output and the historical cross-format defects."""
import hashlib
import json
import pathlib
import re
import struct
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zlib

import make_logo


def decode_png(data):
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    offset, compressed = 8, bytearray()
    width = height = None
    while offset < len(data):
        length = struct.unpack_from('>I', data, offset)[0]
        tag = data[offset + 4:offset + 8]
        payload = data[offset + 8:offset + 8 + length]
        crc = struct.unpack_from('>I', data, offset + 8 + length)[0]
        assert crc == zlib.crc32(tag + payload) & 0xFFFFFFFF
        if tag == b'IHDR':
            width, height, depth, color, compression, filtering, interlace = struct.unpack('>IIBBBBB', payload)
            assert (depth, color, compression, filtering, interlace) == (8, 6, 0, 0, 0)
        if tag == b'IDAT':
            compressed.extend(payload)
        offset += 12 + length
        if tag == b'IEND':
            break
    assert offset == len(data)
    raw = zlib.decompress(compressed)
    assert len(raw) == height * (1 + width * 4)
    rows = []
    for y in range(height):
        start = y * (1 + width * 4)
        assert raw[start] == 0
        rows.append([tuple(raw[start + 1 + x * 4:start + 5 + x * 4]) for x in range(width)])
    return width, height, rows


def decode_ico(data):
    reserved, kind, count = struct.unpack_from('<HHH', data)
    assert (reserved, kind) == (0, 1)
    offset = 6 + 16 * count
    frames = {}
    for i in range(count):
        width, height, colors, zero, planes, bpp, length, start = struct.unpack_from('<BBBBHHII', data, 6 + 16 * i)
        width, height = width or 256, height or 256
        assert (colors, zero, planes, bpp, start) == (0, 0, 1, 32, offset)
        payload = data[start:start + length]
        assert decode_png(payload)[:2] == (width, height)
        frames[width] = payload
        offset += length
    assert offset == len(data)
    return frames


class FaviconTests(unittest.TestCase):
    bg = (153, 27, 27)
    ink = (255, 255, 255)

    def test_compass_raster_matches_svg_landmarks(self):
        svg = ET.fromstring(make_logo.build_svg('compass', '#991b1b', '#ffffff', True))
        ns = '{http://www.w3.org/2000/svg}'
        self.assertEqual(svg.find(ns + 'circle').attrib['r'], '14')
        self.assertEqual(len(svg.findall(ns + 'line')), 4)
        _, _, rows = decode_png(make_logo.build_png(64, self.bg, self.ink, 'compass'))
        for x, y in ((32, 12), (46, 32), (32, 50), (13, 32)):
            self.assertEqual(rows[y][x], self.ink + (255,))
        # The old square ring painted (20,18) white and omitted the compass ticks.
        for x, y in ((20, 18), (32, 32), (4, 32)):
            self.assertEqual(rows[y][x], self.bg + (255,))

    def test_all_styles_have_distinct_rasters_and_known_marks(self):
        samples = {'book': (24, 30), 'shield': (32, 32), 'burst': (32, 32),
                   'broom': (32, 32), 'sword': (32, 30)}
        digests = set()
        for style in make_logo.STYLES:
            data = make_logo.build_png(32, self.bg, self.ink, style)
            digests.add(hashlib.sha256(data).digest())
            self.assertEqual(decode_png(data)[:2], (32, 32))
            if style in samples:
                _, _, rows = decode_png(make_logo.build_png(64, self.bg, self.ink, style))
                x, y = samples[style]
                self.assertEqual(rows[y][x], self.ink + (255,), style)
        self.assertEqual(len(digests), 6)

    def test_book_preserves_translucent_right_page(self):
        _, _, rows = decode_png(make_logo.build_png(64, self.bg, self.ink, 'book'))
        self.assertEqual(rows[30][24], (255, 255, 255, 255))
        self.assertEqual(rows[30][40], (219, 175, 175, 255))

    def test_bg_disc_cuts_the_same_hole_in_svg_and_raster(self):
        mark = make_logo.Mark((make_logo.Polygon(((8, 8), (56, 8), (56, 56), (8, 56))),
                               make_logo.Disc(32, 32, 10, 'bg')))
        svg = make_logo.build_svg(mark, '#991b1b', '#ffffff', True)
        self.assertIn('<circle cx="32" cy="32" r="10" fill="#991b1b"/>', svg)
        _, _, rows = decode_png(make_logo.build_png(64, self.bg, self.ink, mark))
        self.assertEqual(rows[32][32], self.bg + (255,))
        self.assertEqual(rows[32][20], self.ink + (255,))

    def test_rounded_square_and_antialiasing(self):
        _, _, rows = decode_png(make_logo.build_png(32, self.bg, self.ink, 'compass'))
        self.assertEqual(rows[0][0][3], 0)
        self.assertTrue(any(0 < p[3] < 255 for row in rows for p in row))
        self.assertTrue(any(self.bg[0] < p[0] < 255 and p[3] == 255 for row in rows for p in row))
        _, _, square = decode_png(make_logo.build_png(16, self.bg, self.ink, 'compass', False))
        self.assertEqual(square[0][0], self.bg + (255,))

    def test_ico_dimensions_bit_depth_and_shared_png_payload(self):
        frames = {size: make_logo.build_png(size, self.bg, self.ink, 'compass') for size in (16, 32, 48)}
        self.assertEqual(decode_ico(make_logo.build_ico(frames)), frames)

    def test_parallel_cli_generations_stay_in_their_site(self):
        with tempfile.TemporaryDirectory() as temp:
            cases = [('compass', '#991b1b'), ('sword', '#123456'), ('book', '#eeeeee')]
            jobs = []
            for style, color in cases:
                root = pathlib.Path(temp) / style
                process = subprocess.Popen([sys.executable, str(pathlib.Path(make_logo.__file__)),
                                            '--name', 'Example', '--color', color, '--style', style,
                                            '--site-dir', str(root)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                jobs.append((process, root, style, color))
            for process, root, style, color in jobs:
                stdout, stderr = process.communicate(timeout=60)
                self.assertEqual(process.returncode, 0, stderr.decode())
                public = root / 'public'
                self.assertEqual((public / 'logo.svg').read_bytes(), (public / 'icon.svg').read_bytes())
                self.assertIn(color, (public / 'icon.svg').read_text())
                png = (public / 'favicon-32x32.png').read_bytes()
                _, _, rows = decode_png(png)
                self.assertEqual(rows[2][16], make_logo.hex_to_rgb(color) + (255,))
                self.assertEqual(decode_ico((public / 'favicon.ico').read_bytes())[32], png)
                for name, size in [('favicon-96x96.png', 96), ('apple-touch-icon.png', 180)]:
                    self.assertEqual(decode_png((public / name).read_bytes())[:2], (size, size))

    def test_cli_rejects_invalid_color_before_writing(self):
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run([sys.executable, str(pathlib.Path(make_logo.__file__)), '--name', 'Example',
                                     '--color', '991b1bextra', '--site-dir', temp], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((pathlib.Path(temp) / 'public').exists())
        self.assertEqual(make_logo.hex_to_rgb('#abc'), (170, 187, 204))

    def test_checked_in_site_icons_share_the_configured_brand(self):
        root = pathlib.Path(make_logo.__file__).resolve().parent.parent
        config = root / 'config/site.config.ts'
        if not config.exists():
            self.skipTest('skill source has no site; scaffold integration checks its generated icons')
        color = re.search(r"themeColorHex:\s*'([^']+)'", config.read_text())[1]
        bg = make_logo.hex_to_rgb(color)
        ink = (15, 19, 26) if make_logo.relative_luminance(bg) > 0.45 else (255, 255, 255)
        public = root / 'public'
        svg = (public / 'icon.svg').read_text()
        self.assertEqual(svg, (public / 'logo.svg').read_text())
        custom = root / 'config/brand-mark.json'
        if custom.is_file():
            mark = make_logo.load_mark(custom)
            self.assertEqual(svg, make_logo.build_svg(mark, '#%02x%02x%02x' % bg,
                                                     '#%02x%02x%02x' % ink, 'rx=' in svg))
            self.assertNotIn(svg, [make_logo.build_svg(style, '#%02x%02x%02x' % bg,
                              '#%02x%02x%02x' % ink, 'rx=' in svg) for style in make_logo.STYLES])
        else:
            styles = [style for style in make_logo.STYLES if svg == make_logo.build_svg(
                style, '#%02x%02x%02x' % bg, '#%02x%02x%02x' % ink, 'rx=' in svg)]
            self.assertEqual(len(styles), 1, 'SVG must match the configured mark and theme color')
            mark = styles[0]
        for name, size in [('favicon-32x32.png', 32), ('favicon-96x96.png', 96), ('apple-touch-icon.png', 180)]:
            self.assertEqual((public / name).read_bytes(), make_logo.build_png(size, bg, ink, mark, 'rx=' in svg))
        frames = decode_ico((public / 'favicon.ico').read_bytes())
        self.assertEqual(set(frames), {16, 32, 48})
        self.assertEqual(frames[32], (public / 'favicon-32x32.png').read_bytes())

    def test_custom_mark_cli_auto_detection_and_shared_geometry(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            source = root / 'config/brand-mark.json'
            source.parent.mkdir()
            source.write_text(json.dumps({'cornerRadius': 8, 'parts': [
                {'type': 'curve', 'width': 6, 'curves': [[[16, 16], [32, 16], [32, 48], [48, 48]]]}
            ]}))
            mark = make_logo.load_mark(source)
            result = subprocess.run([sys.executable, str(pathlib.Path(make_logo.__file__)),
                                     '--name', 'Example', '--color', '#991b1b', '--site-dir', temp],
                                    capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            self.assertEqual((root / 'public/icon.svg').read_text(),
                             make_logo.build_svg(mark, '#991b1b', '#ffffff', True))
            png = (root / 'public/favicon-32x32.png').read_bytes()
            self.assertEqual(png, make_logo.build_png(32, self.bg, self.ink, mark))
            self.assertEqual(decode_ico((root / 'public/favicon.ico').read_bytes())[32], png)
            _, _, rows = decode_png(make_logo.build_png(64, self.bg, self.ink, mark))
            self.assertEqual(rows[16][16], self.ink + (255,))
            self.assertEqual(rows[48][48], self.ink + (255,))

    def test_custom_mark_rejects_disconnected_and_invalid_curves(self):
        with tempfile.TemporaryDirectory() as temp:
            source = pathlib.Path(temp) / 'mark.json'
            for curves in (
                [[[16, 16], [16, 16], [16, 16], [16, 16]]],
                [[[0, 0], [8, 8], [16, 16], [24, 24]], [[25, 25], [32, 32], [48, 48], [64, 64]]],
                [[[0, 0], [8, 8], [16, 16], [65, 24]]],
            ):
                source.write_text(json.dumps({'parts': [{'type': 'curve', 'width': 6, 'curves': curves}]}))
                with self.assertRaises(ValueError):
                    make_logo.load_mark(source)


if __name__ == '__main__':
    unittest.main()
