#!/usr/bin/env python3
"""Generate matching SVG, PNG, ICO and Apple icons using Python's stdlib.

Usage: python3 scripts/make_logo.py --name "Example Wiki" --color "#991b1b"
All formats share geometry; ICO contains 16, 32 and 48px RGBA frames.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from functools import cached_property
import json
import math
import pathlib
import re
import struct
import zlib

Point = tuple[float, float]
RGB = tuple[int, int, int]


@dataclass(frozen=True)
class Polygon:
    points: tuple[Point, ...]
    opacity: float = 1

    def contains(self, x: float, y: float) -> bool:
        inside = False
        a = self.points[-1]
        for b in self.points:
            if (a[1] > y) != (b[1] > y):
                cross = a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
                if x < cross:
                    inside = not inside
            a = b
        return inside

    def svg(self, ink: str, bg: str) -> str:
        points = ' '.join(f'{x:.4f},{y:.4f}' for x, y in self.points)
        return f'<polygon points="{points}" fill="{ink}" opacity="{self.opacity}"/>'


@dataclass(frozen=True)
class Disc:
    """Filled circle. `fill='bg'` cuts a hole (eyes, portholes, notches)."""
    cx: float
    cy: float
    radius: float
    fill: str = 'ink'

    def contains(self, x: float, y: float) -> bool:
        return (x - self.cx) ** 2 + (y - self.cy) ** 2 <= self.radius ** 2

    def svg(self, ink: str, bg: str) -> str:
        color = bg if self.fill == 'bg' else ink
        return f'<circle cx="{self.cx}" cy="{self.cy}" r="{self.radius}" fill="{color}"/>'


@dataclass(frozen=True)
class Ring:
    cx: float
    cy: float
    radius: float
    width: float
    opacity: float = 1

    def contains(self, x: float, y: float) -> bool:
        distance = (x - self.cx) ** 2 + (y - self.cy) ** 2
        return (self.radius - self.width / 2) ** 2 <= distance <= (self.radius + self.width / 2) ** 2

    def svg(self, ink: str, bg: str) -> str:
        return (f'<circle cx="{self.cx}" cy="{self.cy}" r="{self.radius}" '
                f'fill="none" stroke="{ink}" stroke-width="{self.width}"/>')


@dataclass(frozen=True)
class Stroke:
    start: Point
    end: Point
    width: float
    opacity: float = 1

    def contains(self, x: float, y: float) -> bool:
        ax, ay = self.start
        dx, dy = self.end[0] - ax, self.end[1] - ay
        t = max(0, min(1, ((x - ax) * dx + (y - ay) * dy) / (dx * dx + dy * dy)))
        return (x - ax - t * dx) ** 2 + (y - ay - t * dy) ** 2 <= (self.width / 2) ** 2

    def svg(self, ink: str, bg: str) -> str:
        return (f'<line x1="{self.start[0]}" y1="{self.start[1]}" '
                f'x2="{self.end[0]}" y2="{self.end[1]}" stroke="{ink}" '
                f'stroke-width="{self.width}" stroke-linecap="round"/>')


@dataclass(frozen=True)
class Polyline:
    points: tuple[Point, ...]
    width: float
    opacity: float = 1

    @cached_property
    def segments(self):
        radius = self.width / 2
        return tuple((a[0], a[1], b[0] - a[0], b[1] - a[1],
                      (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2,
                      min(a[0], b[0]) - radius, max(a[0], b[0]) + radius,
                      min(a[1], b[1]) - radius, max(a[1], b[1]) + radius)
                     for a, b in zip(self.points, self.points[1:]) if a != b)

    @cached_property
    def bounds(self):
        radius = self.width / 2
        return (min(x for x, _ in self.points) - radius,
                max(x for x, _ in self.points) + radius,
                min(y for _, y in self.points) - radius,
                max(y for _, y in self.points) + radius)

    def contains(self, x: float, y: float) -> bool:
        left, right, top, bottom = self.bounds
        if not (left <= x <= right and top <= y <= bottom):
            return False
        for ax, ay, dx, dy, length, left, right, top, bottom in self.segments:
            if left <= x <= right and top <= y <= bottom:
                t = max(0, min(1, ((x - ax) * dx + (y - ay) * dy) / length))
                if (x - ax - t * dx) ** 2 + (y - ay - t * dy) ** 2 <= (self.width / 2) ** 2:
                    return True
        return False

    def svg(self, ink: str, bg: str) -> str:
        points = ' '.join(f'{x:.4f},{y:.4f}' for x, y in self.points)
        return (f'<polyline points="{points}" fill="none" stroke="{ink}" '
                f'stroke-width="{self.width}" stroke-linecap="round" stroke-linejoin="round"/>')


@dataclass(frozen=True)
class Mark:
    parts: tuple[Polygon | Disc | Ring | Stroke | Polyline, ...]
    corner_radius: float = 14


def load_mark(file: pathlib.Path) -> Mark:
    """Load project-owned geometry; all output formats use the same primitives."""
    data = json.loads(file.read_text(encoding='utf-8'))

    def number(value, minimum, maximum):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError('mark coordinates and sizes must be finite numbers')
        if not minimum <= value <= maximum:
            raise ValueError(f'mark value must be between {minimum} and {maximum}')
        return value

    def point(value):
        if not isinstance(value, list) or len(value) != 2:
            raise ValueError('mark points must contain two coordinates')
        return tuple(number(v, 0, 64) for v in value)

    raw_parts = data.get('parts')
    if not isinstance(raw_parts, list) or not 1 <= len(raw_parts) <= 32:
        raise ValueError('mark must contain 1 to 32 parts')
    parts = []
    for part in raw_parts:
        kind = part.get('type')
        if kind == 'polygon':
            points = tuple(point(p) for p in part['points'])
            if not 3 <= len(points) <= 128:
                raise ValueError('mark polygons need 3 to 128 points')
            parts.append(Polygon(points))
        elif kind == 'disc':
            centre = point(part.get('center'))
            fill = part.get('fill', 'ink')
            if fill not in ('ink', 'bg'):
                raise ValueError("mark disc fill must be 'ink' or 'bg'")
            parts.append(Disc(centre[0], centre[1], number(part.get('radius'), 0.5, 32), fill))
        elif kind == 'curve':
            curves = part['curves']
            if not isinstance(curves, list) or not 1 <= len(curves) <= 8:
                raise ValueError('mark strokes need 1 to 8 cubic curves')
            points = ()
            for curve in curves:
                if not isinstance(curve, list) or len(curve) != 4:
                    raise ValueError('mark cubic curves need four control points')
                controls = tuple(point(p) for p in curve)
                if points and controls[0] != points[-1]:
                    raise ValueError('mark stroke curves must connect')
                points += cubic(*controls)[1:] if points else cubic(*controls)
            if len(set(points)) < 2:
                raise ValueError('mark strokes cannot have zero length')
            parts.append(Polyline(points, number(part['width'], 0.5, 16)))
        else:
            raise ValueError(f'unsupported mark part: {kind}')
    return Mark(tuple(parts), number(data.get('cornerRadius', 14), 0, 32))


def arc(cx: float, cy: float, radius: float, start: int, end: int) -> tuple[Point, ...]:
    return tuple((cx + radius * math.cos(math.radians(start + (end - start) * i / 16)),
                  cy + radius * math.sin(math.radians(start + (end - start) * i / 16)))
                 for i in range(17))


def cubic(a: Point, b: Point, c: Point, d: Point) -> tuple[Point, ...]:
    points = []
    for i in range(17):
        t = i / 16
        points.append(tuple((1 - t) ** 3 * a[j] + 3 * (1 - t) ** 2 * t * b[j]
                            + 3 * (1 - t) * t ** 2 * c[j] + t ** 3 * d[j] for j in (0, 1)))
    return tuple(points)


# SVG and raster outputs share these primitives; no separate fallback drawing.
book_left = ((18, 44),) + arc(26, 22, 8, 180, 270) + ((32, 14), (32, 44),) + arc(26, 52, 8, 270, 180)
STYLES = {
    'compass': (Ring(32, 32, 14, 4), Stroke((32, 12), (32, 18), 4),
                Stroke((32, 46), (32, 52), 4), Stroke((12, 32), (18, 32), 4),
                Stroke((46, 32), (52, 32), 4)),
    'book': (Polygon(book_left), Polygon(tuple((64 - x, y) for x, y in book_left), 0.65)),
    'shield': (Polygon(((32, 12), (48, 18))
                       + cubic((48, 32), (48, 42), (41, 49), (32, 52))
                       + cubic((32, 52), (23, 49), (16, 42), (16, 32)) + ((16, 18),)),),
    'burst': (Polygon(((32, 10), (37, 27), (54, 32), (37, 37),
                       (32, 54), (27, 37), (10, 32), (27, 27))),),
    'broom': (Stroke((20, 44), (44, 20), 6), Polygon(((40, 24), (48, 16), (52, 20), (44, 28)))),
    'sword': (Polygon(((32, 12), (36, 18), (36, 38), (28, 38), (28, 18))),
              Polygon(((22, 38), (42, 38), (42, 43), (22, 43))),
              Polygon(((29, 43), (35, 43), (35, 52), (29, 52)))),
}

STYLE_FOR_HINT = {
    'witch': 'broom', 'magic': 'broom', 'hogwarts': 'broom',
    'scav': 'compass', 'survival': 'compass', 'map': 'compass',
    'guide': 'book', 'wiki': 'book', 'tale': 'book',
    'war': 'shield', 'battle': 'shield', 'defend': 'shield', 'tower': 'shield',
    'star': 'burst', 'anime': 'burst', 'idol': 'burst',
    'sword': 'sword', 'knight': 'sword', 'quest': 'sword',
}


def pick_style(name: str, explicit: str | None) -> str:
    if explicit:
        if explicit not in STYLES:
            raise ValueError(f"unknown style '{explicit}'; choose from {', '.join(STYLES)}")
        return explicit
    for hint, style in STYLE_FOR_HINT.items():
        if hint in name.lower():
            return style
    return 'compass'


def hex_to_rgb(value: str) -> RGB:
    if not re.fullmatch(r'#?(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})', value):
        raise ValueError('color must be a 3- or 6-digit hex color')
    value = value.lstrip('#')
    if len(value) == 3:
        value = ''.join(c * 2 for c in value)
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def relative_luminance(rgb: RGB) -> float:
    def channel(c: int) -> float:
        s = c / 255
        return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def build_svg(style: str | Mark, bg: str, ink: str, rounded: bool) -> str:
    mark = style if isinstance(style, Mark) else Mark(STYLES[style])
    rx = f' rx="{mark.corner_radius}"' if rounded else ''
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img">'
            f'<rect width="64" height="64"{rx} fill="{bg}"/>'
            + ''.join(part.svg(ink, bg) for part in mark.parts) + '</svg>\n')


def png_chunk(tag: bytes, data: bytes) -> bytes:
    return (struct.pack('>I', len(data)) + tag + data
            + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF))


def build_png(size: int, bg: RGB, ink: RGB, style: str | Mark, rounded: bool = True) -> bytes:
    """4x supersampling preserves thin strokes, round caps and corner alpha."""
    rows = []
    mark = style if isinstance(style, Mark) else Mark(STYLES[style])
    radius = mark.corner_radius
    scale = 64 / size
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            total = [0.0, 0.0, 0.0]
            covered = 0
            for sy in range(4):
                py = (y + (sy + 0.5) / 4) * scale
                for sx in range(4):
                    px = (x + (sx + 0.5) / 4) * scale
                    dx, dy = max(radius - px, 0, px - (64 - radius)), max(radius - py, 0, py - (64 - radius))
                    if rounded and dx * dx + dy * dy > radius ** 2:
                        continue
                    color = list(bg)
                    for part in mark.parts:
                        if part.contains(px, py):
                            if getattr(part, 'fill', 'ink') == 'bg':
                                color = list(bg)
                            else:
                                color = [c * (1 - part.opacity) + k * part.opacity
                                         for c, k in zip(color, ink)]
                    for i in range(3):
                        total[i] += color[i]
                    covered += 1
            row.extend(round(c / covered) if covered else 0 for c in total)
            row.append(round(covered * 255 / 16))
        rows.append(bytes(row))
    return (b'\x89PNG\r\n\x1a\n'
            + png_chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0))
            + png_chunk(b'IDAT', zlib.compress(b''.join(rows), 9)) + png_chunk(b'IEND', b''))


def build_ico(frames: dict[int, bytes]) -> bytes:
    offset = 6 + 16 * len(frames)
    entries = []
    for size, data in frames.items():
        dim = 0 if size == 256 else size
        entries.append(struct.pack('<BBBBHHII', dim, dim, 0, 0, 1, 32, len(data), offset))
        offset += len(data)
    return struct.pack('<HHH', 0, 1, len(frames)) + b''.join(entries) + b''.join(frames.values())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--name', required=True, help='game/site name, used to pick a mark')
    parser.add_argument('--color', required=True, help='theme color, e.g. #1f8f96')
    mark_args = parser.add_mutually_exclusive_group()
    mark_args.add_argument('--style', choices=STYLES, default=None)
    mark_args.add_argument('--mark-file', type=pathlib.Path, help='project-specific 64px geometry JSON')
    parser.add_argument('--site-dir', type=pathlib.Path, default=pathlib.Path('.'))
    parser.add_argument('--square', action='store_true', help='square corners instead of rounded')
    args = parser.parse_args()
    try:
        bg = hex_to_rgb(args.color)
        source = args.mark_file
        # A configured project mark wins over automatic catalogue selection.
        default_source = args.site_dir / 'config/brand-mark.json'
        if source is None and args.style is None and default_source.is_file():
            source = default_source
        style = load_mark(source) if source else pick_style(args.name, args.style)
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as error:
        parser.error(str(error))
    ink = (15, 19, 26) if relative_luminance(bg) > 0.45 else (255, 255, 255)
    svg = build_svg(style, '#%02x%02x%02x' % bg, '#%02x%02x%02x' % ink, not args.square)
    # Keep bytes in memory: parallel sites never share a temporary file.
    frames = {size: build_png(size, bg, ink, style, not args.square) for size in (16, 32, 48, 96, 180, 192, 512)}
    public = args.site_dir / 'public'
    public.mkdir(parents=True, exist_ok=True)
    for name in ('logo.svg', 'icon.svg'):
        (public / name).write_text(svg, encoding='utf-8')
    for size in (32, 96):
        (public / f'favicon-{size}x{size}.png').write_bytes(frames[size])
    (public / 'apple-touch-icon.png').write_bytes(frames[180])
    (public / 'android-chrome-192x192.png').write_bytes(frames[192])
    (public / 'android-chrome-512x512.png').write_bytes(frames[512])
    (public / 'favicon.ico').write_bytes(build_ico({size: frames[size] for size in (16, 32, 48)}))
    label = str(source) if source else style
    print(f'wrote matching SVG / 32px, 96px, 192px, 512px PNG / 16,32,48px ICO / 180px Apple icons (mark: {label})')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
