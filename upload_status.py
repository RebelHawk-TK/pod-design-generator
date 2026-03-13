#!/usr/bin/env python3
"""Quick status dashboard for all POD platform uploads.

Usage:
    python3 upload_status.py              # Full dashboard
    python3 upload_status.py --compact    # One-line-per-platform
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "output"

LANDMARK_DIRS = {
    "all": Path.home() / "Documents/Claude/landmark-style-transfer-unified/output",
}

PLATFORMS = {
    "redbubble": {
        "tracker": Path(__file__).parent / "uploaded_redbubble.json",
        "legacy_tracker": Path(__file__).parent / "uploaded.json",
        "type": "browser",
    },
    "teepublic": {
        "tracker": Path(__file__).parent / "uploaded_teepublic.json",
        "type": "browser",
    },
    "society6": {
        "tracker": Path(__file__).parent / "uploaded_society6.json",
        "type": "browser",
    },
    "pinterest": {
        "tracker": Path(__file__).parent / "uploaded_pinterest.json",
        "type": "api",
    },
    "etsy": {
        "tracker": Path(__file__).parent / "uploaded_etsy.json",
        "type": "api",
    },
    "printify": {
        "tracker": Path(__file__).parent / "uploaded_printify.json",
        "type": "api",
        "key_prefix": "printify:",
    },
}

# Video platforms (separate from image/product platforms)
VIDEO_PLATFORMS = {
    "youtube": {
        "tracker": Path(__file__).parent / "uploaded_youtube.json",
        "type": "api",
    },
    "tiktok": {
        "tracker": Path(__file__).parent / "uploaded_tiktok.json",
        "type": "api",
    },
}

VIDEO_DIR = Path(__file__).parent / "output"
VIDEO_FOLDERS = ["videos", "videos_travel", "videos_stock"]

FOLDERS = ["tshirt", "sticker", "poster"]


def count_designs() -> dict[str, int]:
    """Count available designs per folder in default output."""
    counts = {}
    for folder in FOLDERS:
        folder_path = OUTPUT_DIR / folder
        if folder_path.is_dir():
            counts[folder] = len(list(folder_path.glob("*.png")))
        else:
            counts[folder] = 0
    return counts


def count_landmark_designs() -> dict[str, dict[str, int]]:
    """Count landmark designs per phase per folder."""
    counts = {}
    for phase, base_dir in LANDMARK_DIRS.items():
        counts[phase] = {}
        for folder in FOLDERS:
            folder_path = base_dir / folder
            if folder_path.is_dir():
                counts[phase][folder] = len(list(folder_path.glob("*.png")))
            else:
                counts[phase][folder] = 0
    return counts


def load_tracker(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {}


def split_tracker(tracker: dict, key_prefix: str = "") -> tuple[dict, dict]:
    """Split tracker entries into POD (local) and landmark (ext:) groups."""
    pod = {}
    landmark = {}
    for k, v in tracker.items():
        raw_key = k[len(key_prefix):] if key_prefix and k.startswith(key_prefix) else k
        if raw_key.startswith("ext:"):
            landmark[k] = v
        else:
            pod[k] = v
    return pod, landmark


def folder_stats(entries: dict, folder: str, key_prefix: str = "") -> dict:
    """Get success/failed counts for a folder within a set of tracker entries."""
    folder_keys = []
    for k in entries:
        raw = k[len(key_prefix):] if key_prefix and k.startswith(key_prefix) else k
        # ext: keys have format ext:output/{folder}/stem
        if raw.startswith("ext:"):
            parts = raw.split("/")
            if len(parts) >= 3 and parts[1] == folder:
                folder_keys.append(k)
        elif raw.startswith(f"{folder}/"):
            folder_keys.append(k)
    success = sum(1 for k in folder_keys if entries[k].get("status") == "success")
    failed = sum(1 for k in folder_keys if entries[k].get("status") == "failed")
    return {"success": success, "failed": failed}


def niche_counter(entries: dict) -> Counter:
    """Count successful uploads by niche/landmark."""
    by_niche = Counter()
    for k, v in entries.items():
        if v.get("status") == "success":
            stem = k.split("/")[-1]
            niche = stem.split("_")[0]
            by_niche[niche] += 1
    return by_niche


def platform_stats(platform: str, info: dict) -> dict:
    """Get upload stats for a platform."""
    tracker = load_tracker(info["tracker"])

    if not tracker and "legacy_tracker" in info:
        tracker = load_tracker(info["legacy_tracker"])

    key_prefix = info.get("key_prefix", "")
    pod_entries, landmark_entries = split_tracker(tracker, key_prefix)

    pod_success = sum(1 for v in pod_entries.values() if v.get("status") == "success")
    pod_failed = sum(1 for v in pod_entries.values() if v.get("status") == "failed")
    lm_success = sum(1 for v in landmark_entries.values() if v.get("status") == "success")
    lm_failed = sum(1 for v in landmark_entries.values() if v.get("status") == "failed")

    pod_by_folder = {f: folder_stats(pod_entries, f, key_prefix) for f in FOLDERS}
    lm_by_folder = {f: folder_stats(landmark_entries, f, key_prefix) for f in FOLDERS}

    return {
        "pod_success": pod_success,
        "pod_failed": pod_failed,
        "lm_success": lm_success,
        "lm_failed": lm_failed,
        "success": pod_success + lm_success,
        "failed": pod_failed + lm_failed,
        "total_tracked": len(tracker),
        "pod_by_folder": pod_by_folder,
        "lm_by_folder": lm_by_folder,
        "pod_niches": niche_counter(pod_entries),
        "lm_niches": niche_counter(landmark_entries),
        "type": info["type"],
    }


def count_videos() -> dict[str, int]:
    """Count available videos."""
    counts = {}
    for folder in VIDEO_FOLDERS:
        folder_path = VIDEO_DIR / folder
        if folder_path.is_dir():
            counts[folder] = len(list(folder_path.glob("*.mp4")))
        else:
            counts[folder] = 0
    return counts


def video_platform_stats(info: dict) -> dict:
    """Get upload stats for a video platform."""
    tracker = load_tracker(info["tracker"])
    success = sum(1 for v in tracker.values() if v.get("status") == "success")
    failed = sum(1 for v in tracker.values() if v.get("status") == "failed")
    return {"success": success, "failed": failed, "total_tracked": len(tracker), "type": info["type"]}


def print_dashboard(compact: bool = False) -> None:
    """Print the upload status dashboard."""
    pod_counts = count_designs()
    total_pod = sum(pod_counts.values())
    lm_counts = count_landmark_designs()
    total_lm = sum(c for phase in lm_counts.values() for c in phase.values())
    lm_by_folder = {f: sum(lm_counts[p].get(f, 0) for p in lm_counts) for f in FOLDERS}

    if compact:
        print(f"{'Platform':<12} {'Type':<8} {'POD':>6} {'Landmark':>9} {'Failed':>6} {'Progress':>9}")
        print("-" * 58)
        for platform, info in PLATFORMS.items():
            stats = platform_stats(platform, info)
            total = stats["pod_success"] + stats["lm_success"]
            pct = (total / (total_pod + total_lm) * 100) if (total_pod + total_lm) else 0
            print(f"{platform:<12} {stats['type']:<8} {stats['pod_success']:>6} {stats['lm_success']:>9} {stats['failed']:>6} {pct:>8.1f}%")
        return

    print("=" * 66)
    print("  POD UPLOAD STATUS DASHBOARD")
    print("=" * 66)

    print(f"\nDesign Inventory:")
    print(f"  {'':14} {'POD':>7} {'Landmark':>10} {'Total':>7}")
    for folder in FOLDERS:
        lm = lm_by_folder.get(folder, 0)
        print(f"  {folder:<14} {pod_counts.get(folder, 0):>7} {lm:>10} {pod_counts.get(folder, 0) + lm:>7}")
    print(f"  {'TOTAL':<14} {total_pod:>7} {total_lm:>10} {total_pod + total_lm:>7}")

    print(f"\nPlatform Status:")
    print("-" * 66)

    for platform, info in PLATFORMS.items():
        stats = platform_stats(platform, info)
        total_success = stats["success"]
        total_available = total_pod + total_lm
        pct = (total_success / total_available * 100) if total_available else 0

        auto_label = "API (automatable)" if stats["type"] == "api" else "browser (manual)"
        print(f"\n  {platform.upper()} [{auto_label}]")

        # POD section
        if stats["pod_success"] or stats["pod_failed"]:
            remaining = total_pod - stats["pod_success"]
            print(f"    POD Designs:      {stats['pod_success']:>4} done  |  {stats['pod_failed']:>2} failed  |  {remaining:>5} remaining")
            for folder in FOLDERS:
                fs = stats["pod_by_folder"][folder]
                f_total = pod_counts.get(folder, 0)
                f_remaining = f_total - fs["success"]
                if fs["success"] or fs["failed"]:
                    print(f"      {folder:<12} {fs['success']:>4} done  {fs['failed']:>3} failed  {f_remaining:>4} remaining")
            if stats["pod_niches"]:
                top = stats["pod_niches"].most_common(5)
                print(f"      Top niches: {', '.join(f'{n}({c})' for n, c in top)}")
        else:
            print(f"    POD Designs:         — not started ({total_pod} designs)")

        # Landmark section
        if stats["lm_success"] or stats["lm_failed"]:
            remaining = total_lm - stats["lm_success"]
            print(f"    Landmarks:        {stats['lm_success']:>4} done  |  {stats['lm_failed']:>2} failed  |  {remaining:>5} remaining")
            for folder in FOLDERS:
                fs = stats["lm_by_folder"][folder]
                f_total = lm_by_folder.get(folder, 0)
                f_remaining = f_total - fs["success"]
                if fs["success"] or fs["failed"]:
                    print(f"      {folder:<12} {fs['success']:>4} done  {fs['failed']:>3} failed  {f_remaining:>4} remaining")
            if stats["lm_niches"]:
                top = stats["lm_niches"].most_common(5)
                print(f"      Top landmarks: {', '.join(f'{n}({c})' for n, c in top)}")
        else:
            print(f"    Landmarks:           — not started ({total_lm} designs)")

        print(f"    TOTAL: {total_success:>4} / {total_available}  ({pct:.1f}%)")

    # Video platforms
    vid_counts = count_videos()
    total_videos = sum(vid_counts.values())

    print(f"\n{'=' * 66}")
    print(f"  VIDEO UPLOADS")
    print(f"{'=' * 66}")
    print(f"\n  Video Inventory:")
    for folder, count in vid_counts.items():
        print(f"    {folder:<18} {count:>4}")
    print(f"    {'TOTAL':<18} {total_videos:>4}")

    print(f"\n  Platform Status:")
    print("-" * 66)

    for platform, info in VIDEO_PLATFORMS.items():
        stats = video_platform_stats(info)
        remaining = total_videos - stats["success"]
        pct = (stats["success"] / total_videos * 100) if total_videos else 0
        print(f"\n  {platform.upper()} [API]")
        print(f"    Uploaded: {stats['success']:>4} done  |  {stats['failed']:>2} failed  |  {remaining:>5} remaining")
        print(f"    TOTAL: {stats['success']:>4} / {total_videos}  ({pct:.1f}%)")

    print("\n" + "-" * 66)
    grand_done = sum(platform_stats(p, i)["success"] for p, i in PLATFORMS.items())
    grand_total = (total_pod + total_lm) * len(PLATFORMS)
    vid_done = sum(video_platform_stats(i)["success"] for i in VIDEO_PLATFORMS.values())
    vid_total = total_videos * len(VIDEO_PLATFORMS)
    all_done = grand_done + vid_done
    all_total = grand_total + vid_total
    print(f"  PRODUCTS: {grand_done}/{grand_total} uploads ({grand_done/grand_total*100 if grand_total else 0:.1f}%)")
    print(f"  VIDEOS:   {vid_done}/{vid_total} uploads ({vid_done/vid_total*100 if vid_total else 0:.1f}%)")
    print(f"  COMBINED: {all_done}/{all_total} ({all_done/all_total*100 if all_total else 0:.1f}%)")
    print("=" * 66)


def main():
    parser = argparse.ArgumentParser(description="POD upload status dashboard")
    parser.add_argument("--compact", action="store_true", help="Compact one-line-per-platform view")
    args = parser.parse_args()
    print_dashboard(compact=args.compact)


if __name__ == "__main__":
    main()
