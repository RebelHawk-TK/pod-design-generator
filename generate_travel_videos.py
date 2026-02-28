#!/usr/bin/env python3
"""Generate 30s travel/history videos for TikTok and Instagram Reels.

Creates educational videos with voiceover giving history and fun facts about
25 world landmarks. Each landmark has 2 variants (a + b) = 50 videos total.

Usage:
    python3 generate_travel_videos.py --landmark eiffel_tower              # Both variants
    python3 generate_travel_videos.py --landmark eiffel_tower --variant a  # One variant
    python3 generate_travel_videos.py --all                                # All 50
    python3 generate_travel_videos.py --batch 5                            # First 5 landmarks (10 videos)
    python3 generate_travel_videos.py --list                               # Show landmarks
    python3 generate_travel_videos.py --all --force                        # Overwrite existing
    python3 generate_travel_videos.py --all --dry-run                      # Preview only
"""

from __future__ import annotations

import argparse
import sys
import time

from video_gen_travel.compositor import compose_travel_video
from video_gen_travel.config import LANDMARKS, OUTPUT_DIR, STYLE_SET_A, STYLE_SET_B
from video_gen_travel.scripts import TRAVEL_SCRIPTS


def list_landmarks() -> None:
    """Print all available landmarks and their script status."""
    print(f"\n{'ID':<25} {'Name':<30} {'Location':<20} {'Scripts'}")
    print("-" * 100)
    for lid, info in sorted(LANDMARKS.items()):
        scripts = TRAVEL_SCRIPTS.get(lid, {})
        has_a = "a" if "a" in scripts else "-"
        has_b = "b" if "b" in scripts else "-"
        print(f"{lid:<25} {info['display_name']:<30} {info['location']:<20} [{has_a},{has_b}]")

    total_scripts = sum(len(v) for v in TRAVEL_SCRIPTS.values())
    print(f"\nTotal: {len(LANDMARKS)} landmarks, {total_scripts} scripts")
    print(f"\nStyle Set A: {', '.join(STYLE_SET_A)}")
    print(f"Style Set B: {', '.join(STYLE_SET_B)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate 30s travel/history videos for TikTok and Instagram.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--landmark", type=str, help="Generate videos for one landmark")
    group.add_argument("--all", action="store_true", help="Generate all 50 videos")
    group.add_argument("--batch", type=int, metavar="N", help="Generate first N landmarks (2 videos each)")
    group.add_argument("--list", action="store_true", help="List available landmarks and scripts")

    parser.add_argument(
        "--variant", choices=["a", "b"],
        help="Generate only one variant (default: both a and b)",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing videos")
    parser.add_argument("--dry-run", action="store_true", help="Preview without generating")

    args = parser.parse_args()

    if args.list:
        list_landmarks()
        return

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

    # Build (landmark, variant) pairs
    variants = [args.variant] if args.variant else ["a", "b"]
    jobs: list[tuple[str, str]] = []
    for lid in landmark_ids:
        for v in variants:
            if lid in TRAVEL_SCRIPTS and v in TRAVEL_SCRIPTS[lid]:
                jobs.append((lid, v))

    if not jobs:
        print("No matching landmark/variant combinations found.")
        sys.exit(1)

    print(f"\nTravel Video Generator")
    print(f"======================")
    print(f"Videos:    {len(jobs)}")
    print(f"Variants:  {', '.join(variants)}")
    print(f"Output:    {OUTPUT_DIR}")
    print(f"Force:     {args.force}")
    print()

    if args.dry_run:
        print("DRY RUN — would generate:")
        for lid, v in jobs:
            lm = LANDMARKS[lid]
            filename = f"{lid}_travel_{v}.mp4"
            exists = (OUTPUT_DIR / filename).exists()
            if exists and args.force:
                status = "OVERWRITE"
            elif exists:
                status = "SKIP (exists)"
            else:
                status = "NEW"
            styles = STYLE_SET_A if v == "a" else STYLE_SET_B
            print(f"  {filename:<45} {lm['display_name']:<25} [{status}]")
        return

    # Generate
    start_time = time.time()
    success = 0
    errors = []

    for i, (lid, v) in enumerate(jobs, 1):
        lm = LANDMARKS[lid]
        print(f"[{i}/{len(jobs)}] {lm['display_name']} variant {v} ({lid})")
        try:
            compose_travel_video(lid, v, force=args.force)
            success += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            errors.append((f"{lid}_{v}", str(e)))

    elapsed = time.time() - start_time
    minutes = elapsed / 60
    print(f"\nComplete: {success}/{len(jobs)} videos in {minutes:.1f} min")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for name, err in errors:
            print(f"  {name}: {err}")


if __name__ == "__main__":
    main()
