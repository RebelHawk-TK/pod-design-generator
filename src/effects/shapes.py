"""Geometric shape primitives for pattern generation."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw


def draw_circle(
    draw: ImageDraw.ImageDraw,
    center: tuple[int, int],
    radius: int,
    fill: str | tuple | None = None,
    outline: str | tuple | None = None,
    width: int = 2,
) -> None:
    x, y = center
    draw.ellipse(
        [x - radius, y - radius, x + radius, y + radius],
        fill=fill,
        outline=outline,
        width=width,
    )


def draw_triangle(
    draw: ImageDraw.ImageDraw,
    center: tuple[int, int],
    size: int,
    fill: str | tuple | None = None,
    outline: str | tuple | None = None,
    rotation: float = 0,
    width: int = 2,
) -> None:
    """Draw an equilateral triangle centered at `center`."""
    cx, cy = center
    points = []
    for i in range(3):
        angle = math.radians(rotation + i * 120 - 90)
        px = cx + size * math.cos(angle)
        py = cy + size * math.sin(angle)
        points.append((px, py))
    draw.polygon(points, fill=fill, outline=outline, width=width)


def draw_diamond(
    draw: ImageDraw.ImageDraw,
    center: tuple[int, int],
    size: int,
    fill: str | tuple | None = None,
    outline: str | tuple | None = None,
    width: int = 2,
) -> None:
    cx, cy = center
    points = [
        (cx, cy - size),
        (cx + size, cy),
        (cx, cy + size),
        (cx - size, cy),
    ]
    draw.polygon(points, fill=fill, outline=outline, width=width)


def draw_star(
    draw: ImageDraw.ImageDraw,
    center: tuple[int, int],
    outer_radius: int,
    inner_radius: int | None = None,
    points: int = 5,
    fill: str | tuple | None = None,
    outline: str | tuple | None = None,
    rotation: float = -90,
    width: int = 2,
) -> None:
    """Draw a star with given number of points."""
    if inner_radius is None:
        inner_radius = outer_radius // 2
    cx, cy = center
    coords = []
    for i in range(points * 2):
        r = outer_radius if i % 2 == 0 else inner_radius
        angle = math.radians(rotation + i * (360 / (points * 2)))
        coords.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(coords, fill=fill, outline=outline, width=width)


def draw_hexagon(
    draw: ImageDraw.ImageDraw,
    center: tuple[int, int],
    size: int,
    fill: str | tuple | None = None,
    outline: str | tuple | None = None,
    width: int = 2,
) -> None:
    cx, cy = center
    coords = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        coords.append((cx + size * math.cos(angle), cy + size * math.sin(angle)))
    draw.polygon(coords, fill=fill, outline=outline, width=width)
