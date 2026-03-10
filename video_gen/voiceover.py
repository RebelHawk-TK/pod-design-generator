"""Edge-TTS wrapper with caching for voiceover generation."""

from __future__ import annotations

import asyncio
from pathlib import Path

import edge_tts

from .config import AUDIO_CACHE_DIR, TTS_VOICE, TTS_RATE


async def _generate_async(text: str, output_path: Path, voice: str, rate: str) -> None:
    """Generate speech audio using edge-tts."""
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(str(output_path))


def generate_voiceover(
    landmark_id: str,
    script: str,
    *,
    force: bool = False,
    voice: str | None = None,
) -> Path:
    """Generate (or load cached) voiceover MP3 for a landmark.

    Args:
        landmark_id: Used for cache filename.
        script: Text to speak.
        force: If True, regenerate even if cached.
        voice: Override TTS voice.

    Returns:
        Path to the MP3 file.
    """
    AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = AUDIO_CACHE_DIR / f"{landmark_id}_voiceover.mp3"

    if cache_path.exists() and not force:
        return cache_path

    v = voice or TTS_VOICE
    asyncio.run(_generate_async(script, cache_path, v, TTS_RATE))
    return cache_path
