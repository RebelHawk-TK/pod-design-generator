"""Assemble 28s travel/history videos from Ken Burns clips, text overlays, and voiceover.

Video timeline (28s total, under 30s limit):
    0-3s   Style A, zoom in             (silence)      Landmark name + location
    3-11s  Style A, pan left-to-right   Voiceover      (no text)
    11-19s Style B, diagonal pan        Voiceover      (no text)
    19-25s Style C, reverse pan zoom    Voiceover      (no text)
    25-28s Style C, zoom out, fade      (silence)      CTA bottom-third
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import edge_tts
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import (
    AudioFileClip,
    CompositeAudioClip,
    CompositeVideoClip,
    ImageClip,
    VideoClip,
    concatenate_videoclips,
    vfx,
)

from video_gen.ken_burns import make_frame_generator

from .config import (
    AUDIO_CACHE_DIR,
    BODY_FONT,
    CLIP_1_DURATION,
    CLIP_2_DURATION,
    CLIP_3_DURATION,
    CROSSFADE,
    FPS,
    HEIGHT,
    INTRO_DURATION,
    LANDMARKS,
    OUTPUT_DIR,
    OUTRO_DURATION,
    POSTER_SOURCE_DIR,
    STYLE_SET_A,
    STYLE_SET_B,
    TITLE_FONT,
    TTS_RATE,
    TTS_VOICE,
    VOICEOVER_START,
    WIDTH,
)
from .scripts import TRAVEL_SCRIPTS


# ---------------------------------------------------------------------------
# Camera move assignments for the 5-clip structure
# ---------------------------------------------------------------------------

INTRO_MOVE = "zoom_in"
CLIP_1_MOVE = "pan_left_to_right"
CLIP_2_MOVE = "diagonal"
CLIP_3_MOVE = "pan_right_to_left_zoom"
OUTRO_MOVE = "zoom_out"


# ---------------------------------------------------------------------------
# Text overlays
# ---------------------------------------------------------------------------

def _load_font(font_path: Path, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(str(font_path), size)
    except OSError:
        return ImageFont.load_default()


def _render_text_overlay(
    text_lines: list[tuple[str, int, Path]],
    bg_alpha: int = 160,
    position: str = "center",
) -> np.ndarray:
    """Render text lines with semi-transparent background.

    Args:
        text_lines: List of (text, font_size, font_path) tuples.
        bg_alpha: Background strip transparency (0-255).
        position: "center" (intro) or "bottom" (outro CTA).

    Returns:
        RGBA numpy array (HEIGHT x WIDTH x 4).
    """
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    fonts = []
    bboxes = []
    for text, size, fpath in text_lines:
        font = _load_font(fpath, size)
        fonts.append(font)
        bbox = draw.textbbox((0, 0), text, font=font)
        bboxes.append(bbox)

    line_heights = [bb[3] - bb[1] for bb in bboxes]
    line_spacing = 16
    total_h = sum(line_heights) + line_spacing * (len(text_lines) - 1)
    strip_padding = 30

    if position == "bottom":
        # Bottom-third: place text in lower 20% of frame
        strip_bottom = HEIGHT - 80
        strip_top = strip_bottom - total_h - 2 * strip_padding
    else:
        # Center
        strip_top = (HEIGHT - total_h) // 2 - strip_padding
        strip_bottom = (HEIGHT + total_h) // 2 + strip_padding

    draw.rectangle(
        [(0, strip_top), (WIDTH, strip_bottom)],
        fill=(0, 0, 0, bg_alpha),
    )

    y = strip_top + strip_padding
    for i, (text, _size, _fpath) in enumerate(text_lines):
        bbox = bboxes[i]
        text_w = bbox[2] - bbox[0]
        x = (WIDTH - text_w) // 2
        draw.text((x, y), text, fill=(255, 255, 255, 255), font=fonts[i])
        y += line_heights[i] + line_spacing

    return np.array(img)


def _make_overlay_clip(
    text_lines: list[tuple[str, int, Path]],
    duration: float,
    fade_in: float = 0.8,
    fade_out: float = 0.8,
    position: str = "center",
) -> ImageClip:
    """Create a text overlay clip with fade in/out."""
    overlay_arr = _render_text_overlay(text_lines, position=position)
    clip = ImageClip(overlay_arr, duration=duration)
    effects = []
    if fade_in > 0:
        effects.append(vfx.CrossFadeIn(fade_in))
    if fade_out > 0:
        effects.append(vfx.CrossFadeOut(fade_out))
    if effects:
        clip = clip.with_effects(effects)
    return clip


# ---------------------------------------------------------------------------
# TTS (separate cache from promo videos)
# ---------------------------------------------------------------------------

async def _generate_tts_async(text: str, output_path: Path) -> None:
    communicate = edge_tts.Communicate(text, TTS_VOICE, rate=TTS_RATE)
    await communicate.save(str(output_path))


def _generate_voiceover(
    landmark_id: str,
    variant: str,
    script: str,
    *,
    force: bool = False,
) -> Path:
    """Generate (or load cached) voiceover for a travel video."""
    AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = AUDIO_CACHE_DIR / f"{landmark_id}_travel_{variant}.mp3"

    if cache_path.exists() and not force:
        return cache_path

    asyncio.run(_generate_tts_async(script, cache_path))
    return cache_path


# ---------------------------------------------------------------------------
# Poster loading
# ---------------------------------------------------------------------------

def _get_poster_path(landmark_id: str, style_id: str) -> Path:
    return POSTER_SOURCE_DIR / f"{landmark_id}_{style_id}_poster.png"


# ---------------------------------------------------------------------------
# Main compositor
# ---------------------------------------------------------------------------

def compose_travel_video(
    landmark_id: str,
    variant: str,
    *,
    force: bool = False,
) -> Path:
    """Compose a 28s travel/history video for a landmark.

    Args:
        landmark_id: Key into LANDMARKS dict.
        variant: "a" or "b" — selects style set and script.
        force: Overwrite existing video and regenerate voiceover.

    Returns:
        Path to the output MP4.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{landmark_id}_travel_{variant}.mp4"

    if output_path.exists() and not force:
        print(f"  Skipping {output_path.name} (exists). Use --force to overwrite.")
        return output_path

    lm = LANDMARKS[landmark_id]
    styles = STYLE_SET_A if variant == "a" else STYLE_SET_B

    # Get script
    scripts = TRAVEL_SCRIPTS.get(landmark_id)
    if not scripts or variant not in scripts:
        raise ValueError(f"No travel script for {landmark_id} variant {variant}")
    script_text = scripts[variant]

    # Generate voiceover
    print(f"  Generating voiceover ({len(script_text.split())} words)...")
    vo_path = _generate_voiceover(landmark_id, variant, script_text, force=force)

    # Load 3 source images (one per style)
    images: list[Image.Image] = []
    for sid in styles:
        img_path = _get_poster_path(landmark_id, sid)
        if not img_path.exists():
            raise FileNotFoundError(f"Missing poster: {img_path}")
        images.append(Image.open(img_path).convert("RGB"))

    print(f"  Building Ken Burns clips (5 segments)...")

    # --- Intro clip (3s): Style A, zoom in, title overlay ---
    intro_gen = make_frame_generator(images[0], INTRO_MOVE, INTRO_DURATION)
    intro_clip = VideoClip(intro_gen, duration=INTRO_DURATION).with_fps(FPS)

    intro_overlay = _make_overlay_clip(
        [
            (lm["display_name"].upper(), 72, TITLE_FONT),
            (lm["location"], 40, BODY_FONT),
        ],
        duration=INTRO_DURATION,
        fade_in=0.5,
        fade_out=0.5,
        position="center",
    )
    intro_clip = CompositeVideoClip(
        [intro_clip, intro_overlay], size=(WIDTH, HEIGHT)
    )

    # --- Clip 1 (8s): Style A, pan left-to-right ---
    clip1_gen = make_frame_generator(images[0], CLIP_1_MOVE, CLIP_1_DURATION)
    clip1 = VideoClip(clip1_gen, duration=CLIP_1_DURATION).with_fps(FPS)

    # --- Clip 2 (8s): Style B, diagonal ---
    clip2_gen = make_frame_generator(images[1], CLIP_2_MOVE, CLIP_2_DURATION)
    clip2 = VideoClip(clip2_gen, duration=CLIP_2_DURATION).with_fps(FPS)

    # --- Clip 3 (6s): Style C, reverse pan zoom ---
    clip3_gen = make_frame_generator(images[2], CLIP_3_MOVE, CLIP_3_DURATION)
    clip3 = VideoClip(clip3_gen, duration=CLIP_3_DURATION).with_fps(FPS)

    # --- Outro clip (5s): Style C, zoom out, bottom-third CTA ---
    outro_gen = make_frame_generator(images[2], OUTRO_MOVE, OUTRO_DURATION)
    outro_clip = VideoClip(outro_gen, duration=OUTRO_DURATION).with_fps(FPS)

    outro_overlay = _make_overlay_clip(
        [
            ("moderndesignconcept.com", 48, TITLE_FONT),
            ("Link in bio", 36, BODY_FONT),
        ],
        duration=OUTRO_DURATION,
        fade_in=0.8,
        fade_out=1.0,
        position="bottom",
    )
    outro_clip = CompositeVideoClip(
        [outro_clip, outro_overlay], size=(WIDTH, HEIGHT)
    )

    # --- Concatenate with crossfades ---
    print(f"  Compositing video...")
    all_clips = [intro_clip, clip1, clip2, clip3, outro_clip]

    transition_clips = [all_clips[0]]
    for clip in all_clips[1:]:
        transition_clips.append(
            clip.with_effects([vfx.CrossFadeIn(CROSSFADE)])
        )

    final_video = concatenate_videoclips(
        transition_clips,
        method="compose",
        padding=-CROSSFADE,
    )

    # --- Add voiceover audio starting at VOICEOVER_START ---
    vo_audio = AudioFileClip(str(vo_path))
    vo_audio = vo_audio.with_start(VOICEOVER_START)
    final_audio = CompositeAudioClip([vo_audio])
    final_video = final_video.with_audio(final_audio)

    # --- Export ---
    print(f"  Exporting to {output_path.name}...")
    final_video.write_videofile(
        str(output_path),
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        threads=4,
        logger="bar",
    )

    # Clean up
    for clip in all_clips:
        clip.close()
    final_video.close()
    vo_audio.close()

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"  Done: {output_path.name} ({size_mb:.1f} MB)")
    return output_path
