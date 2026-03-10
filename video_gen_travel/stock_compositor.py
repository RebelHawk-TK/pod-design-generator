"""Assemble 28s travel videos from stock footage clips, text overlays, and voiceover.

Uses real Pexels stock clips instead of Ken Burns on art images.
Same timeline structure and voiceover scripts as the art-style travel videos.

Video timeline (28s total, under 30s limit):
    0-3s   Stock clip 1           (silence)      Landmark name + location
    3-11s  Stock clip 2           Voiceover      (no text)
    11-19s Stock clip 3           Voiceover      (no text)
    19-25s Stock clip 4 start     Voiceover      (no text)
    25-28s Stock clip 4 cont.     (silence)      CTA bottom-third
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
    VideoFileClip,
    concatenate_videoclips,
    vfx,
)

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
    OUTRO_DURATION,
    STOCK_CLIPS_DIR,
    STOCK_OUTPUT_DIR,
    TITLE_FONT,
    TTS_RATE,
    TTS_VOICE,
    VOICEOVER_START,
    WIDTH,
)
from .scripts import TRAVEL_SCRIPTS


# ---------------------------------------------------------------------------
# Text overlays (reused from compositor.py)
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
    """Render text lines with semi-transparent background. Returns RGBA array."""
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
        strip_bottom = HEIGHT - 80
        strip_top = strip_bottom - total_h - 2 * strip_padding
    else:
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
# TTS (shared cache with art-style travel videos)
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
    # Same cache key as art-style travel videos — same script, same audio
    cache_path = AUDIO_CACHE_DIR / f"{landmark_id}_travel_{variant}.mp3"

    if cache_path.exists() and not force:
        return cache_path

    asyncio.run(_generate_tts_async(script, cache_path))
    return cache_path


# ---------------------------------------------------------------------------
# Stock clip loading and processing
# ---------------------------------------------------------------------------

def _load_stock_clip(clip_path: Path, target_duration: float) -> VideoFileClip:
    """Load a stock clip and resize/crop to 1080x1920 portrait.

    Handles both portrait and landscape source clips:
    - Portrait clips get scaled to fit width, cropped vertically if needed
    - Landscape clips get scaled to fit height, cropped horizontally
    """
    clip = VideoFileClip(str(clip_path))

    # Trim to target duration (take from start)
    if clip.duration > target_duration:
        clip = clip.subclipped(0, target_duration)
    elif clip.duration < target_duration:
        # If clip is shorter than needed, loop it
        loops_needed = int(target_duration / clip.duration) + 1
        from moviepy import concatenate_videoclips as concat
        clip = concat([clip] * loops_needed).subclipped(0, target_duration)

    # Resize/crop to 1080x1920
    src_w, src_h = clip.size
    target_aspect = WIDTH / HEIGHT  # 0.5625

    src_aspect = src_w / src_h

    if src_aspect > target_aspect:
        # Source is wider — scale to match height, crop width
        scale = HEIGHT / src_h
        new_w = int(src_w * scale)
        clip = clip.resized((new_w, HEIGHT))
        # Center crop to WIDTH
        x_offset = (new_w - WIDTH) // 2
        clip = clip.cropped(x1=x_offset, x2=x_offset + WIDTH)
    else:
        # Source is taller or same — scale to match width, crop height
        scale = WIDTH / src_w
        new_h = int(src_h * scale)
        clip = clip.resized((WIDTH, new_h))
        # Center crop to HEIGHT
        y_offset = (new_h - HEIGHT) // 2
        clip = clip.cropped(y1=y_offset, y2=y_offset + HEIGHT)

    return clip.with_fps(FPS)


# ---------------------------------------------------------------------------
# Main compositor
# ---------------------------------------------------------------------------

def compose_stock_travel_video(
    landmark_id: str,
    variant: str,
    *,
    force: bool = False,
    source_dir: Path | None = None,
) -> Path:
    """Compose a 28s travel video using stock footage clips.

    Args:
        landmark_id: Key into LANDMARKS dict.
        variant: "a" or "b" — selects script variant.
        force: Overwrite existing video and regenerate voiceover.

    Returns:
        Path to the output MP4.
    """
    STOCK_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = STOCK_OUTPUT_DIR / f"{landmark_id}_stock_{variant}.mp4"

    if output_path.exists() and not force:
        print(f"  Skipping {output_path.name} (exists). Use --force to overwrite.")
        return output_path

    lm = LANDMARKS[landmark_id]

    # Get script
    scripts = TRAVEL_SCRIPTS.get(landmark_id)
    if not scripts or variant not in scripts:
        raise ValueError(f"No travel script for {landmark_id} variant {variant}")
    script_text = scripts[variant]

    # Generate voiceover
    print(f"  Generating voiceover ({len(script_text.split())} words)...")
    vo_path = _generate_voiceover(landmark_id, variant, script_text, force=force)

    # Load 4 stock clips
    clip_dir = STOCK_CLIPS_DIR / landmark_id
    if not clip_dir.exists():
        raise FileNotFoundError(
            f"Stock clips not found: {clip_dir}\n"
            f"Run: python3 download_stock_clips.py --landmark {landmark_id}"
        )

    clip_paths = sorted(clip_dir.glob("clip_*.mp4"))
    if len(clip_paths) < 4:
        raise FileNotFoundError(
            f"Need 4 clips in {clip_dir}, found {len(clip_paths)}.\n"
            f"Run: python3 download_stock_clips.py --landmark {landmark_id} --force"
        )

    # Clip durations matching the timeline:
    # Intro(3) + Clip1(8) + Clip2(8) + Clip3(6) + Outro(5) = 30 raw
    # Minus 4 crossfades × 0.5s = 28s final
    # Stock clip 1 → intro (3s)
    # Stock clip 2 → clip 1 (8s)
    # Stock clip 3 → clip 2 (8s)
    # Stock clip 4 → clip 3 (6s) + outro (5s) = 11s
    durations = [
        INTRO_DURATION,     # 3s
        CLIP_1_DURATION,    # 8s
        CLIP_2_DURATION,    # 8s
        CLIP_3_DURATION + OUTRO_DURATION,  # 11s (clip 4 spans clip3 + outro)
    ]

    print(f"  Loading and processing 4 stock clips...")
    stock_clips = []
    for i, cpath in enumerate(clip_paths[:4]):
        stock_clips.append(_load_stock_clip(cpath, durations[i]))

    print(f"  Building video segments...")

    # --- Intro (3s): Stock clip 1 with title overlay ---
    intro_clip = stock_clips[0].subclipped(0, INTRO_DURATION)
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

    # --- Clip 1 (8s): Stock clip 2 ---
    clip1 = stock_clips[1].subclipped(0, CLIP_1_DURATION)

    # --- Clip 2 (8s): Stock clip 3 ---
    clip2 = stock_clips[2].subclipped(0, CLIP_2_DURATION)

    # --- Clip 3 (6s): Stock clip 4 first part ---
    clip3 = stock_clips[3].subclipped(0, CLIP_3_DURATION)

    # --- Outro (5s): Stock clip 4 second part with CTA overlay ---
    outro_clip = stock_clips[3].subclipped(CLIP_3_DURATION, CLIP_3_DURATION + OUTRO_DURATION)
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
    # Mix stock clip audio (muted) with voiceover
    final_video = final_video.without_audio()
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
    for sc in stock_clips:
        sc.close()
    final_video.close()
    vo_audio.close()

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"  Done: {output_path.name} ({size_mb:.1f} MB)")
    return output_path
