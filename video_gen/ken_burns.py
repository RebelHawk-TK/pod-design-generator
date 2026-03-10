"""Ken Burns zoom/pan effect from still images.

Takes a high-res image and produces a moviepy VideoClip with smooth
camera motion (zoom-in, pan, zoom-out, diagonal).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
from PIL import Image

from .config import WORK_RES, WIDTH, HEIGHT, FPS


@dataclass
class CropRect:
    """Defines a crop region as center (cx, cy) and scale (fraction of image)."""
    cx: float  # center x, 0-1
    cy: float  # center y, 0-1
    scale: float  # crop width as fraction of image width


# Aspect ratio of output (vertical 9:16)
ASPECT = WIDTH / HEIGHT  # 0.5625


def _smoothstep(t: float) -> float:
    """Hermite smoothstep for eased interpolation."""
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


# ---------------------------------------------------------------------------
# Predefined camera moves (start_crop, end_crop)
# Each crop is relative to a square working image (WORK_RES x WORK_RES).
# scale=0.55 means the crop window is 55% of the image width,
# which for 9:16 gives a tall vertical slice.
# ---------------------------------------------------------------------------

CAMERA_MOVES: dict[str, tuple[CropRect, CropRect]] = {
    "zoom_in": (
        CropRect(cx=0.5, cy=0.5, scale=0.65),
        CropRect(cx=0.5, cy=0.45, scale=0.45),
    ),
    "pan_left_to_right": (
        CropRect(cx=0.35, cy=0.5, scale=0.55),
        CropRect(cx=0.65, cy=0.5, scale=0.55),
    ),
    "pan_right_to_left_zoom": (
        CropRect(cx=0.65, cy=0.5, scale=0.60),
        CropRect(cx=0.40, cy=0.45, scale=0.48),
    ),
    "zoom_out": (
        CropRect(cx=0.5, cy=0.45, scale=0.42),
        CropRect(cx=0.5, cy=0.5, scale=0.65),
    ),
    "diagonal": (
        CropRect(cx=0.35, cy=0.60, scale=0.58),
        CropRect(cx=0.60, cy=0.40, scale=0.48),
    ),
}

# Order of camera moves assigned to clips in a video
DEFAULT_MOVE_SEQUENCE = ["zoom_in", "pan_left_to_right", "pan_right_to_left_zoom"]
INTRO_MOVE = "zoom_in"
OUTRO_MOVE = "zoom_out"


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def _crop_frame(img: Image.Image, crop: CropRect) -> Image.Image:
    """Crop a region from img according to CropRect and resize to output dims."""
    w, h = img.size
    crop_w = crop.scale * w
    crop_h = crop_w / ASPECT  # taller than wide for vertical video

    # Clamp so we don't go out of bounds
    left = max(0, crop.cx * w - crop_w / 2)
    top = max(0, crop.cy * h - crop_h / 2)
    right = min(w, left + crop_w)
    bottom = min(h, top + crop_h)

    # Adjust if clamped
    if right - left < crop_w:
        left = max(0, right - crop_w)
    if bottom - top < crop_h:
        top = max(0, bottom - crop_h)

    cropped = img.crop((int(left), int(top), int(right), int(bottom)))
    return cropped.resize((WIDTH, HEIGHT), Image.LANCZOS)


def make_frame_generator(
    img: Image.Image,
    move_name: str,
    duration: float,
) -> Callable[[float], np.ndarray]:
    """Return a function t -> numpy frame array for the given camera move."""
    # Downscale to working resolution
    work_img = img.resize((WORK_RES, WORK_RES), Image.LANCZOS)

    start, end = CAMERA_MOVES[move_name]

    def get_frame(t: float) -> np.ndarray:
        progress = _smoothstep(t / duration)
        current = CropRect(
            cx=_lerp(start.cx, end.cx, progress),
            cy=_lerp(start.cy, end.cy, progress),
            scale=_lerp(start.scale, end.scale, progress),
        )
        frame_img = _crop_frame(work_img, current)
        return np.array(frame_img)

    return get_frame
