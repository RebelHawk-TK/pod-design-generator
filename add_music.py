#!/usr/bin/env python3
"""Overlay regional traditional music onto landmark videos.

Maps each landmark to a cultural region, then uses ffmpeg to mix
the appropriate royalty-free music track at low volume under the
existing video audio.

Usage:
    python3 add_music.py --dry-run                    # Preview mapping
    python3 add_music.py --limit 5                    # Process 5 videos
    python3 add_music.py                              # Process all
    python3 add_music.py --source-dir output/videos   # Specific folder
    python3 add_music.py --volume 0.15                # Adjust music volume
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from video_captions import extract_video_info

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_DIR = Path(__file__).parent
MUSIC_DIR = PROJECT_DIR / "music" / "regional"

VIDEO_DIRS = [
    PROJECT_DIR / "output" / "videos",
    PROJECT_DIR / "output" / "videos_travel",
    PROJECT_DIR / "output" / "videos_stock",
]

# Output directories mirror input with _music suffix
OUTPUT_SUFFIX = "_music"

# Audio settings
DEFAULT_VOLUME = 0.12  # Music volume (0.0-1.0), low so it doesn't overpower
FADE_IN = 2.0          # seconds
FADE_OUT = 2.0         # seconds

# ---------------------------------------------------------------------------
# Region -> music file mapping
# ---------------------------------------------------------------------------

MUSIC_FILES = {
    "indian": "kalsstockmedia-free-soul-indian-sitar-tabla-flute-396347.mp3",
    "french": "vibehorn-french-paris-romantic-music-464386.mp3",
    "italian": "mohamed_hassan-italian-romantic-367371.mp3",
    "greek": "chrisdjyogi-greek-aegean-sunshine-bouzouki-groove-421454.mp3",
    "middle_east": "sigmamusicart-ramadan-islamic-arabic-middle-east-background-music-303476.mp3",
    "egyptian": "hitslab-egyptian-egypt-desert-music-502005.mp3",
    "moroccan": "djovan-medina-night-dance-502569.mp3",
    "latin": "the_mountain-latin-487015.mp3",
    "chinese": "kaazoom-smooth-as-silk-full-version-traditional-chinese-music-383307.mp3",
    "japanese_se_asian": "music_for_videos-asian-cinematic-122770.mp3",
    "nordic_celtic": "juliush-epic-eagle-flight-celtic-medieval-nordic-background-music-440117.mp3",
    "central_european": "viacheslavstarostin-classical-orchestral-strings-music-423202.mp3",
    "spanish": "nickpanekaiassets-classical-guitar-piece-with-flamenco-flair-253103.mp3",
    "african": "alec_koff-african-drums-tribal-492178.mp3",
    "oceania": "surprising_media-tribal-drums-fantasy-with-didgeridoo-and-handpan-442639.mp3",
    "north_american": "sonican-cinematic-western-loop-duel-adventure-297474.mp3",
    "polynesian": "brilsmurfmusiceditions-isa-isa-variations-on-a-polynesian-poem-no3-359572.mp3",
    "balkan": "artmanzh-battonya-balkan-music-330439.mp3",
    "russian": "muzaproduction-russian-folk-kalinka-108671.mp3",
    "ambient": "surprising_media-oriental-style-ambient-299347.mp3",
}

# ---------------------------------------------------------------------------
# Landmark -> region mapping
# ---------------------------------------------------------------------------

LANDMARK_REGION = {
    # Indian
    "taj_mahal": "indian",
    "golden_temple_amritsar": "indian",
    "hawa_mahal": "indian",
    "mysore_palace": "indian",
    "sigiriya": "indian",
    # French
    "eiffel_tower": "french",
    "notre_dame": "french",
    "mont_saint_michel": "french",
    # Italian
    "colosseum": "italian",
    "duomo_florence": "italian",
    "tower_of_pisa": "italian",
    "ponte_vecchio": "italian",
    "rialto_bridge": "italian",
    "amalfi_coast": "italian",
    # Greek
    "santorini": "greek",
    "parthenon": "greek",
    "acropolis_athens": "greek",
    "meteora": "greek",
    # Turkish / Middle East
    "hagia_sophia": "middle_east",
    "blue_mosque": "middle_east",
    "cappadocia": "middle_east",
    "petra": "middle_east",
    "wadi_rum": "middle_east",
    "sheikh_zayed_mosque": "middle_east",
    "burj_khalifa": "middle_east",
    # Egyptian
    "pyramids_giza": "egyptian",
    # Moroccan
    "chefchaouen": "moroccan",
    "djemaa_el_fna": "moroccan",
    # Latin America
    "machu_picchu": "latin",
    "chichen_itza": "latin",
    "christ_redeemer": "latin",
    "sugarloaf_rio": "latin",
    "guanajuato": "latin",
    "tikal": "latin",
    "havana_vieja": "latin",
    # Chinese
    "great_wall": "chinese",
    "zhangjiajie": "chinese",
    "li_river_guilin": "chinese",
    "terracotta_warriors": "chinese",
    "potala_palace": "chinese",
    # Japanese / Southeast Asian
    "mount_fuji": "japanese_se_asian",
    "fushimi_inari": "japanese_se_asian",
    "meiji_shrine": "japanese_se_asian",
    "angkor_wat": "japanese_se_asian",
    "borobudur": "japanese_se_asian",
    "hoi_an": "japanese_se_asian",
    "banaue_rice_terraces": "japanese_se_asian",
    "halong_bay": "japanese_se_asian",
    "gyeongbokgung": "japanese_se_asian",
    "petronas_towers": "japanese_se_asian",
    # Nordic / Celtic
    "stonehenge": "nordic_celtic",
    "big_ben": "nordic_celtic",
    "edinburgh_old_town": "nordic_celtic",
    "tower_of_london": "nordic_celtic",
    "giants_causeway": "nordic_celtic",
    "hapenny_bridge": "nordic_celtic",
    "temple_bar": "nordic_celtic",
    "trolltunga": "nordic_celtic",
    "hallgrimskirkja": "nordic_celtic",
    "northern_lights_iceland": "nordic_celtic",
    # Central European
    "neuschwanstein": "central_european",
    "charles_bridge": "central_european",
    "rothenburg": "central_european",
    "bruges_medieval": "central_european",
    "amsterdam_canals": "central_european",
    "nyhavn": "central_european",
    "rijksmuseum": "central_european",
    # Spanish
    "sagrada_familia": "spanish",
    "seville_alcazar": "spanish",
    # African
    "victoria_falls": "african",
    "table_mountain": "african",
    "serengeti": "african",
    "lalibela_churches": "african",
    "zanzibar_stone_town": "african",
    # Oceania
    "sydney_opera": "oceania",
    "uluru": "oceania",
    "great_barrier_reef": "oceania",
    "twelve_apostles": "oceania",
    "milford_sound": "oceania",
    "tongariro": "oceania",
    # North American
    "statue_of_liberty": "north_american",
    "golden_gate": "north_american",
    "monument_valley": "north_american",
    "yellowstone": "north_american",
    "antelope_canyon": "north_american",
    "lake_louise": "north_american",
    "moraine_lake": "north_american",
    # Polynesian
    "moai": "polynesian",
    "easter_island": "polynesian",
    "bora_bora": "polynesian",
    # Balkan
    "dubrovnik_walls": "balkan",
    "plitvice_lakes": "balkan",
    # Russian
    "st_basils": "russian",
}


def get_region(landmark_id: str) -> str:
    """Get the cultural region for a landmark, defaulting to ambient."""
    return LANDMARK_REGION.get(landmark_id, "ambient")


def get_music_path(landmark_id: str) -> Path:
    """Get the music file path for a landmark."""
    region = get_region(landmark_id)
    filename = MUSIC_FILES.get(region, MUSIC_FILES["ambient"])
    return MUSIC_DIR / filename


# ---------------------------------------------------------------------------
# ffmpeg overlay
# ---------------------------------------------------------------------------

def get_duration(path: Path) -> float:
    """Get media duration in seconds."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, timeout=30,
    )
    return float(result.stdout.strip())


def overlay_music(
    video_path: Path,
    music_path: Path,
    output_path: Path,
    *,
    volume: float = DEFAULT_VOLUME,
    fade_in: float = FADE_IN,
    fade_out: float = FADE_OUT,
) -> bool:
    """Mix music track under video audio using ffmpeg.

    - Trims music to video length
    - Applies fade in/out to music
    - Mixes at specified volume level
    - Preserves original video audio at full volume
    """
    try:
        video_duration = get_duration(video_path)
    except Exception as e:
        print(f"  Error getting duration: {e}")
        return False

    fade_out_start = max(0, video_duration - fade_out)

    # Build ffmpeg filter:
    # [1:a] = music track, trim to video length, apply volume + fades
    # [0:a] = original video audio at full volume
    # amix = combine both
    filter_complex = (
        f"[1:a]atrim=0:{video_duration},asetpts=PTS-STARTPTS,"
        f"volume={volume},"
        f"afade=t=in:st=0:d={fade_in},"
        f"afade=t=out:st={fade_out_start}:d={fade_out}[music];"
        f"[0:a][music]amix=inputs=2:duration=first:dropout_transition=2[out]"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-i", str(music_path),
        "-filter_complex", filter_complex,
        "-map", "0:v",
        "-map", "[out]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_path),
    ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            print(f"  ffmpeg error: {result.stderr[-200:]}")
            return False
        return True
    except subprocess.TimeoutExpired:
        print(f"  ffmpeg timed out")
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def discover_videos(source_dirs: list[Path]) -> list[tuple[Path, str, str, Path]]:
    """Find all videos and compute output paths.

    Returns: (video_path, landmark_id, region, output_path) tuples.
    """
    videos = []
    for source_dir in source_dirs:
        if not source_dir.is_dir():
            continue

        # Output dir: videos -> videos_music, videos_travel -> videos_travel_music
        out_dir = source_dir.parent / (source_dir.name + OUTPUT_SUFFIX)

        for mp4 in sorted(source_dir.glob("*.mp4")):
            landmark_id, _ = extract_video_info(mp4.stem)
            region = get_region(landmark_id)
            output_path = out_dir / mp4.name
            videos.append((mp4, landmark_id, region, output_path))

    return videos


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Overlay regional traditional music onto landmark videos.",
    )
    parser.add_argument("--source-dir", help="Process a specific video directory")
    parser.add_argument("--limit", type=int, default=0, help="Max videos to process (0=all)")
    parser.add_argument("--volume", type=float, default=DEFAULT_VOLUME,
                        help=f"Music volume 0.0-1.0 (default: {DEFAULT_VOLUME})")
    parser.add_argument("--dry-run", action="store_true", help="Preview mapping without processing")
    parser.add_argument("--skip-existing", action="store_true", default=True,
                        help="Skip videos that already have music overlaid (default: true)")
    parser.add_argument("--force", action="store_true",
                        help="Re-process even if output exists")
    args = parser.parse_args()

    source_dirs = VIDEO_DIRS
    if args.source_dir:
        source_dirs = [Path(args.source_dir)]

    # Validate music files exist
    missing = []
    for region, filename in MUSIC_FILES.items():
        if not (MUSIC_DIR / filename).exists():
            missing.append(f"  {region}: {filename}")
    if missing:
        print(f"Missing music files in {MUSIC_DIR}:")
        for m in missing:
            print(m)
        sys.exit(1)

    all_videos = discover_videos(source_dirs)
    print(f"Found {len(all_videos)} total videos\n")

    # Filter already processed
    to_process = []
    for item in all_videos:
        video_path, landmark_id, region, output_path = item
        if not args.force and output_path.exists():
            continue
        to_process.append(item)

    if not to_process:
        print("All videos already have music overlaid. Use --force to re-process.")
        return

    if args.limit and args.limit > 0:
        to_process = to_process[:args.limit]

    print(f"Will {'preview' if args.dry_run else 'process'} {len(to_process)} videos\n")

    if args.dry_run:
        # Show region distribution
        from collections import Counter
        regions = Counter(r for _, _, r, _ in to_process)
        print("Region distribution:")
        for region, count in sorted(regions.items(), key=lambda x: -x[1]):
            music_file = MUSIC_FILES.get(region, "???")
            print(f"  {region:20s} {count:3d} videos  <- {music_file[:50]}")
        print()
        for i, (vp, lid, region, op) in enumerate(to_process[:20], 1):
            print(f"  [{i}] {vp.name} -> {region}")
        if len(to_process) > 20:
            print(f"  ... and {len(to_process) - 20} more")
        return

    # Process videos
    success = 0
    failed = 0

    for i, (video_path, landmark_id, region, output_path) in enumerate(to_process, 1):
        music_path = get_music_path(landmark_id)
        print(f"[{i}/{len(to_process)}] {video_path.name} ({region})")
        print(f"  Music: {music_path.name[:60]}")

        if overlay_music(video_path, music_path, output_path, volume=args.volume):
            success += 1
            print(f"  -> OK ({output_path.parent.name}/{output_path.name})")
        else:
            failed += 1
            print(f"  -> FAILED")

    print(f"\n=== Music overlay complete ===")
    print(f"  Success: {success}/{len(to_process)}")
    if failed:
        print(f"  Failed: {failed}")

    # Show output directories
    out_dirs = set(op.parent for _, _, _, op in to_process)
    for d in sorted(out_dirs):
        count = len(list(d.glob("*.mp4"))) if d.exists() else 0
        print(f"  {d.name}/: {count} videos")


if __name__ == "__main__":
    main()
