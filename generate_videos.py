#!/usr/bin/env python3
"""Generate TikTok/Reels videos for landmark art products.

Creates 30-60s vertical videos with Ken Burns camera effects and AI voiceover.

Usage:
    python3 generate_videos.py --landmark eiffel_tower     # One video
    python3 generate_videos.py --all                        # All 25
    python3 generate_videos.py --batch 5                    # First 5
    python3 generate_videos.py --list                       # Show landmarks
    python3 generate_videos.py --landmark taj_mahal --styles starry_night,great_wave,the_scream
    python3 generate_videos.py --all --force                # Overwrite existing
    python3 generate_videos.py --all --dry-run              # Preview only
"""

from __future__ import annotations

import argparse
import sys
import time

from pathlib import Path

from video_gen.compositor import compose_video
from video_gen.config import DEFAULT_STYLE_TRIPLET, LANDMARKS, OUTPUT_DIR, POSTER_SOURCE_DIR, STYLES


def list_landmarks() -> None:
    """Print all available landmarks."""
    print(f"\n{'ID':<25} {'Name':<30} {'Location'}")
    print("-" * 80)
    for lid, info in sorted(LANDMARKS.items()):
        print(f"{lid:<25} {info['display_name']:<30} {info['location']}")
    print(f"\nTotal: {len(LANDMARKS)} landmarks")
    print(f"\nAvailable styles: {', '.join(sorted(STYLES.keys()))}")
    print(f"Default triplet: {', '.join(DEFAULT_STYLE_TRIPLET)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate TikTok/Reels videos for landmark art products."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--landmark", type=str, help="Generate video for one landmark")
    group.add_argument("--all", action="store_true", help="Generate all 25 videos")
    group.add_argument("--batch", type=int, metavar="N", help="Generate first N videos")
    group.add_argument("--list", action="store_true", help="List available landmarks")

    parser.add_argument(
        "--styles",
        type=str,
        help="Comma-separated style IDs (default: starry_night,great_wave,water_lilies)",
    )
    parser.add_argument("--source-dir", type=str, help="Override poster source directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing videos")
    parser.add_argument("--dry-run", action="store_true", help="Preview without generating")

    args = parser.parse_args()

    if args.list:
        list_landmarks()
        return

    # Parse styles
    style_ids = None
    if args.styles:
        style_ids = [s.strip() for s in args.styles.split(",")]
        for sid in style_ids:
            if sid not in STYLES:
                print(f"Error: Unknown style '{sid}'")
                print(f"Available: {', '.join(sorted(STYLES.keys()))}")
                sys.exit(1)
        if len(style_ids) != 3:
            print(f"Error: Need exactly 3 styles, got {len(style_ids)}")
            sys.exit(1)

    # Build landmark list
    if args.landmark:
        if args.landmark not in LANDMARKS:
            print(f"Error: Unknown landmark '{args.landmark}'")
            print(f"Use --list to see available landmarks.")
            sys.exit(1)
        landmark_ids = [args.landmark]
    elif args.all:
        landmark_ids = sorted(LANDMARKS.keys())
    else:
        landmark_ids = sorted(LANDMARKS.keys())[: args.batch]

    # Source dir override
    source_dir = Path(args.source_dir) / "poster" if args.source_dir else None

    # Filter to landmarks that have images in the source dir
    if source_dir:
        check_style = (style_ids or DEFAULT_STYLE_TRIPLET)[0]
        available = [lid for lid in landmark_ids
                     if (source_dir / f"{lid}_{check_style}_poster.png").exists()]
        skipped = len(landmark_ids) - len(available)
        landmark_ids = available
        if skipped:
            print(f"Filtered to {len(landmark_ids)} landmarks with images in source dir ({skipped} skipped)")

    styles_display = ", ".join(style_ids or DEFAULT_STYLE_TRIPLET)
    print(f"\nVideo Generator")
    print(f"===============")
    print(f"Landmarks: {len(landmark_ids)}")
    print(f"Styles:    {styles_display}")
    print(f"Source:    {source_dir or POSTER_SOURCE_DIR}")
    print(f"Output:    {OUTPUT_DIR}")
    print(f"Force:     {args.force}")
    print()

    if args.dry_run:
        print("DRY RUN — would generate:")
        for lid in landmark_ids:
            lm = LANDMARKS[lid]
            status = "OVERWRITE" if (OUTPUT_DIR / f"{lid}.mp4").exists() and args.force else \
                     "SKIP (exists)" if (OUTPUT_DIR / f"{lid}.mp4").exists() else "NEW"
            print(f"  {lid:<25} {lm['display_name']:<25} [{status}]")
        return

    # Generate
    start_time = time.time()
    success = 0
    errors = []

    for i, lid in enumerate(landmark_ids, 1):
        lm = LANDMARKS[lid]
        print(f"[{i}/{len(landmark_ids)}] {lm['display_name']} ({lid})")
        try:
            compose_video(lid, style_ids, force=args.force, source_dir=source_dir)
            success += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            errors.append((lid, str(e)))

    elapsed = time.time() - start_time
    print(f"\nComplete: {success}/{len(landmark_ids)} videos in {elapsed:.0f}s")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for lid, err in errors:
            print(f"  {lid}: {err}")


if __name__ == "__main__":
    main()
