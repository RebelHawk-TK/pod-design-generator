"""Travel video generator config — timing, style sets, output paths.

Imports shared constants from the promo video_gen module and adds
travel-specific overrides for the longer 28s format.
"""

from __future__ import annotations

from video_gen.config import (
    BASE_DIR,
    FONTS_DIR,
    FPS,
    HEIGHT,
    LANDMARKS,
    POSTER_SOURCE_DIR,
    STYLES,
    TITLE_FONT,
    BODY_FONT,
    WIDTH,
    WORK_RES,
)

# Re-export shared constants for convenience
__all__ = [
    "BASE_DIR", "FONTS_DIR", "FPS", "HEIGHT", "LANDMARKS",
    "POSTER_SOURCE_DIR", "STYLES", "TITLE_FONT", "BODY_FONT",
    "WIDTH", "WORK_RES",
    # Travel-specific
    "OUTPUT_DIR", "AUDIO_CACHE_DIR",
    "INTRO_DURATION", "CLIP_1_DURATION", "CLIP_2_DURATION",
    "CLIP_3_DURATION", "OUTRO_DURATION", "CROSSFADE",
    "VOICEOVER_START", "TTS_VOICE", "TTS_RATE",
    "STYLE_SET_A", "STYLE_SET_B",
]

# ---------------------------------------------------------------------------
# Output paths (separate from promo videos)
# ---------------------------------------------------------------------------

OUTPUT_DIR = BASE_DIR / "output" / "videos_travel"
AUDIO_CACHE_DIR = OUTPUT_DIR / ".audio_cache"

# ---------------------------------------------------------------------------
# Timing (seconds) — 28s total under 30s limit
#
# Intro(3) + Clip1(8) + Clip2(8) + Clip3(6) + Outro(5) = 30s raw
# Minus 4 crossfades × 0.5s = -2s overlap → 28s final
# ---------------------------------------------------------------------------

INTRO_DURATION = 3.0
CLIP_1_DURATION = 8.0
CLIP_2_DURATION = 8.0
CLIP_3_DURATION = 6.0
OUTRO_DURATION = 5.0
CROSSFADE = 0.5

# Voiceover starts 1.5s in (overlaps tail of intro)
VOICEOVER_START = 1.5

# ---------------------------------------------------------------------------
# TTS config — slower documentary feel
# ---------------------------------------------------------------------------

TTS_VOICE = "en-US-GuyNeural"
TTS_RATE = "+0%"

# ---------------------------------------------------------------------------
# Style sets — each video uses 3 styles
# Video A: impressionist/peaceful set
# Video B: expressionist/dramatic set
# ---------------------------------------------------------------------------

STYLE_SET_A = ["starry_night", "great_wave", "water_lilies"]
STYLE_SET_B = ["the_scream", "cafe_terrace", "composition_vii"]
