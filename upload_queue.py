#!/usr/bin/env python3
"""Randomized upload queue for all video types (promo, travel, stock).

Scans all video directories, shuffles into one queue, and uploads one at a
time to TikTok and/or Instagram. Tracks position so it resumes where it left off.

Usage:
    python3 upload_queue.py --rebuild                     # Build/rebuild shuffled queue
    python3 upload_queue.py --status                      # Show queue stats
    python3 upload_queue.py --dry-run --limit 5           # Preview next 5
    python3 upload_queue.py --limit 1                     # Upload next 1 video
    python3 upload_queue.py --limit 1 --platform tiktok   # TikTok only
"""

from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
QUEUE_FILE = PROJECT_DIR / "upload_queue.json"

# Video directories to scan
VIDEO_DIRS = {
    "promo": PROJECT_DIR / "output" / "videos_music",
    "travel": PROJECT_DIR / "output" / "videos_travel_music",
    "stock": PROJECT_DIR / "output" / "videos_stock_music",
}

# Reproducible shuffle seed
SHUFFLE_SEED = 42


def _classify_video(path: Path, video_type: str) -> dict:
    """Build a queue entry for a video file."""
    stem = path.stem

    # Extract landmark ID from filename
    landmark = stem
    for suffix in ("_travel_a", "_travel_b", "_stock_a", "_stock_b"):
        if stem.endswith(suffix):
            landmark = stem[: -len(suffix)]
            break

    return {
        "path": str(path.relative_to(PROJECT_DIR)),
        "type": video_type,
        "landmark": landmark,
        "filename": path.name,
    }


def build_queue(*, seed: int = SHUFFLE_SEED) -> dict:
    """Scan all video dirs and build a shuffled queue."""
    videos = []
    for vtype, vdir in VIDEO_DIRS.items():
        if not vdir.exists():
            continue
        for mp4 in sorted(vdir.glob("*.mp4")):
            videos.append(_classify_video(mp4, vtype))

    if not videos:
        print("No videos found in any directory.")
        sys.exit(1)

    rng = random.Random(seed)
    rng.shuffle(videos)

    queue = {
        "version": 1,
        "created": datetime.now(timezone.utc).isoformat(),
        "seed": seed,
        "position": 0,
        "total": len(videos),
        "videos": videos,
    }

    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)

    return queue


def load_queue() -> dict:
    """Load existing queue from disk."""
    if not QUEUE_FILE.exists():
        print(f"No queue file found. Run with --rebuild first.")
        sys.exit(1)
    with open(QUEUE_FILE) as f:
        return json.load(f)


def save_queue(queue: dict) -> None:
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)


def show_status(queue: dict) -> None:
    """Display queue statistics."""
    total = queue["total"]
    pos = queue["position"]
    remaining = total - pos

    # Count by type
    by_type = {}
    remaining_by_type = {}
    for i, v in enumerate(queue["videos"]):
        vtype = v["type"]
        by_type[vtype] = by_type.get(vtype, 0) + 1
        if i >= pos:
            remaining_by_type[vtype] = remaining_by_type.get(vtype, 0) + 1

    print(f"\nUpload Queue Status")
    print(f"====================")
    print(f"Queue file:  {QUEUE_FILE.name}")
    print(f"Created:     {queue['created'][:19]}")
    print(f"Total:       {total} videos")
    print(f"Completed:   {pos}")
    print(f"Remaining:   {remaining}")
    print(f"Progress:    {pos}/{total} ({100 * pos / total:.0f}%)" if total > 0 else "")
    print()
    print(f"By type (total / remaining):")
    for vtype in sorted(by_type.keys()):
        t = by_type[vtype]
        r = remaining_by_type.get(vtype, 0)
        print(f"  {vtype:<8} {t:>3} total / {r:>3} remaining")

    if remaining > 0:
        next_v = queue["videos"][pos]
        print(f"\nNext up: {next_v['filename']} ({next_v['type']}, {next_v['landmark']})")


def show_dry_run(queue: dict, limit: int) -> None:
    """Preview the next N videos in the queue."""
    pos = queue["position"]
    total = queue["total"]
    remaining = total - pos

    count = min(limit, remaining) if limit > 0 else remaining
    print(f"\nNext {count} videos in queue (position {pos}/{total}):\n")

    for i in range(count):
        idx = pos + i
        v = queue["videos"][idx]
        print(f"  [{idx + 1}] {v['filename']}")
        print(f"       Type: {v['type']}, Landmark: {v['landmark']}")
        print(f"       Path: {v['path']}")
        print()


def upload_video(video_entry: dict, platform: str) -> bool:
    """Upload a single video to one platform. Returns True on success."""
    video_path = PROJECT_DIR / video_entry["path"]
    if not video_path.exists():
        print(f"  File not found: {video_path}")
        return False

    source_dir = str(video_path.parent)

    # Build the uploader command
    if platform == "tiktok":
        cmd = [
            sys.executable, str(PROJECT_DIR / "upload_tiktok.py"),
            "--source-dir", source_dir,
            "--limit", "1",
        ]
    elif platform == "instagram":
        cmd = [
            sys.executable, str(PROJECT_DIR / "upload_instagram_api.py"),
            "--source-dir", source_dir,
            "--limit", "1",
        ]
    else:
        print(f"  Unknown platform: {platform}")
        return False

    print(f"  -> Uploading to {platform}...")
    try:
        result = subprocess.run(cmd, cwd=str(PROJECT_DIR), timeout=600)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"  -> {platform} upload timed out")
        return False
    except Exception as e:
        print(f"  -> {platform} upload error: {e}")
        return False


def run_uploads(queue: dict, *, limit: int = 1, platform: str = "both") -> None:
    """Upload the next N videos from the queue."""
    pos = queue["position"]
    total = queue["total"]
    remaining = total - pos

    if remaining == 0:
        print("Queue exhausted! All videos have been uploaded.")
        print("Run with --rebuild to reshuffle and start over.")
        return

    count = min(limit, remaining) if limit > 0 else remaining
    platforms = ["tiktok", "instagram"] if platform == "both" else [platform]

    print(f"\nUploading {count} video(s) to {', '.join(platforms)}")
    print(f"Queue position: {pos}/{total}\n")

    uploaded = 0
    for i in range(count):
        idx = pos + i
        v = queue["videos"][idx]
        print(f"[{idx + 1}/{total}] {v['filename']} ({v['type']}, {v['landmark']})")

        all_ok = True
        for plat in platforms:
            ok = upload_video(v, plat)
            if not ok:
                all_ok = False
                print(f"  Warning: {plat} upload may have failed")

        # Advance position regardless (tracker files handle individual retry)
        queue["position"] = idx + 1
        save_queue(queue)
        uploaded += 1
        print(f"  Queue advanced to position {idx + 1}")

        if i < count - 1:
            print()

    print(f"\nSession complete: {uploaded} video(s) processed")
    new_remaining = total - queue["position"]
    print(f"Queue: {queue['position']}/{total} done, {new_remaining} remaining")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Randomized upload queue for all video types.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--rebuild", action="store_true", help="Build/rebuild shuffled queue")
    parser.add_argument("--status", action="store_true", help="Show queue statistics")
    parser.add_argument("--dry-run", action="store_true", help="Preview next videos without uploading")
    parser.add_argument("--limit", type=int, default=1, help="Number of videos to upload (default: 1)")
    parser.add_argument(
        "--platform", choices=["tiktok", "instagram", "both"],
        default="both", help="Platform to upload to (default: both)",
    )

    args = parser.parse_args()

    if args.rebuild:
        queue = build_queue()
        print(f"Queue built: {queue['total']} videos shuffled (seed={SHUFFLE_SEED})")
        show_status(queue)
        return

    if args.status:
        queue = load_queue()
        show_status(queue)
        return

    if args.dry_run:
        queue = load_queue()
        show_dry_run(queue, args.limit)
        return

    # Default: upload
    queue = load_queue()
    run_uploads(queue, limit=args.limit, platform=args.platform)


if __name__ == "__main__":
    main()
