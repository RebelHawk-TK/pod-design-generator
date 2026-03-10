"""Assemble final video from Ken Burns clips, text overlays, and voiceover."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import (
    AudioFileClip,
    CompositeAudioClip,
    CompositeVideoClip,
    ImageClip,
    VideoClip,
    concatenate_videoclips,
)

from .config import (
    BODY_FONT,
    CLIP_DURATION,
    CLIPS_PER_VIDEO,
    CROSSFADE,
    DEFAULT_STYLE_TRIPLET,
    FPS,
    HEIGHT,
    INTRO_DURATION,
    LANDMARKS,
    OUTPUT_DIR,
    OUTRO_DURATION,
    POSTER_SOURCE_DIR,
    STYLES,
    TITLE_FONT,
    VOICEOVER_START,
    WIDTH,
)
from .ken_burns import (
    DEFAULT_MOVE_SEQUENCE,
    INTRO_MOVE,
    OUTRO_MOVE,
    make_frame_generator,
)
from .script_gen import generate_script
from .voiceover import generate_voiceover


def _load_font(font_path: Path, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(str(font_path), size)
    except OSError:
        return ImageFont.load_default()


def _render_text_overlay(
    text_lines: list[tuple[str, int, Path]],
    bg_alpha: int = 160,
) -> np.ndarray:
    """Render centered text lines with semi-transparent background strip.

    Args:
        text_lines: List of (text, font_size, font_path) tuples.
        bg_alpha: Background strip transparency (0-255).

    Returns:
        RGBA numpy array (HEIGHT x WIDTH x 4).
    """
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Measure total height
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

    # Draw background strip
    strip_top = (HEIGHT - total_h) // 2 - strip_padding
    strip_bottom = (HEIGHT + total_h) // 2 + strip_padding
    draw.rectangle(
        [(0, strip_top), (WIDTH, strip_bottom)],
        fill=(0, 0, 0, bg_alpha),
    )

    # Draw text lines
    y = (HEIGHT - total_h) // 2
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
) -> ImageClip:
    """Create a text overlay clip with fade in/out."""
    overlay_arr = _render_text_overlay(text_lines)
    clip = ImageClip(overlay_arr, duration=duration)
    clip = clip.with_effects([])  # ensure effects list exists
    if fade_in > 0:
        from moviepy import vfx
        clip = clip.with_effects([vfx.CrossFadeIn(fade_in), vfx.CrossFadeOut(fade_out)])
    return clip


def _get_poster_path(landmark_id: str, style_id: str, source_dir: Path | None = None) -> Path:
    """Get path to a poster image."""
    base = source_dir or POSTER_SOURCE_DIR
    return base / f"{landmark_id}_{style_id}_poster.png"


def compose_video(
    landmark_id: str,
    style_ids: list[str] | None = None,
    *,
    force: bool = False,
    source_dir: Path | None = None,
) -> Path:
    """Compose a full video for a landmark.

    Args:
        landmark_id: Key into LANDMARKS dict.
        style_ids: List of 3 style keys. Defaults to DEFAULT_STYLE_TRIPLET.
        force: Overwrite existing video and regenerate voiceover.
        source_dir: Override poster source directory.

    Returns:
        Path to the output MP4.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{landmark_id}.mp4"

    if output_path.exists() and not force:
        print(f"  Skipping {landmark_id} (exists). Use --force to overwrite.")
        return output_path

    styles = style_ids or DEFAULT_STYLE_TRIPLET
    lm = LANDMARKS[landmark_id]

    print(f"  Generating voiceover...")
    script = generate_script(landmark_id, styles)
    vo_path = generate_voiceover(landmark_id, script, force=force)

    # Load source images (2 for 15s format: main + outro background)
    images: list[Image.Image] = []
    for sid in styles[:2]:
        img_path = _get_poster_path(landmark_id, sid, source_dir)
        if not img_path.exists():
            raise FileNotFoundError(f"Missing poster: {img_path}")
        images.append(Image.open(img_path).convert("RGB"))

    print(f"  Building Ken Burns clips...")

    # --- Intro clip (2s): first image, slow zoom, title overlay ---
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
    )
    intro_clip = CompositeVideoClip([intro_clip, intro_overlay], size=(WIDTH, HEIGHT))

    # --- Main clip (8s): Ken Burns zoom/pan ---
    move = DEFAULT_MOVE_SEQUENCE[0]
    gen = make_frame_generator(images[0], move, CLIP_DURATION)
    main_clip = VideoClip(gen, duration=CLIP_DURATION).with_fps(FPS)

    # --- Outro clip (5s): second image, zoom out, CTA overlay ---
    outro_img = images[1] if len(images) > 1 else images[0]
    outro_gen = make_frame_generator(outro_img, OUTRO_MOVE, OUTRO_DURATION)
    outro_clip = VideoClip(outro_gen, duration=OUTRO_DURATION).with_fps(FPS)

    outro_overlay = _make_overlay_clip(
        [
            ("moderndesignconcept.com", 56, TITLE_FONT),
            ("Shop the Collection", 40, BODY_FONT),
        ],
        duration=OUTRO_DURATION,
        fade_in=0.8,
        fade_out=1.0,
    )
    outro_clip = CompositeVideoClip([outro_clip, outro_overlay], size=(WIDTH, HEIGHT))

    # --- Concatenate with crossfades ---
    print(f"  Compositing video...")
    all_clips = [intro_clip, main_clip, outro_clip]

    from moviepy import vfx
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
    # Pad voiceover to start at the right time
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
