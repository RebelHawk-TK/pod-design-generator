"""Upload progress service — ports upload_status.py logic to data-returning functions."""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"

PLATFORMS = {
    "redbubble": {
        "tracker": PROJECT_ROOT / "uploaded_redbubble.json",
        "legacy_tracker": PROJECT_ROOT / "uploaded.json",
        "type": "browser",
    },
    "teepublic": {
        "tracker": PROJECT_ROOT / "uploaded_teepublic.json",
        "type": "browser",
    },
    "society6": {
        "tracker": PROJECT_ROOT / "uploaded_society6.json",
        "type": "browser",
    },
    "pinterest": {
        "tracker": PROJECT_ROOT / "uploaded_pinterest.json",
        "type": "api",
    },
    "etsy": {
        "tracker": PROJECT_ROOT / "uploaded_etsy.json",
        "type": "api",
    },
    "printify": {
        "tracker": PROJECT_ROOT / "uploaded_printify.json",
        "type": "api",
        "key_prefix": "printify:",
    },
}

FOLDERS = ["tshirt", "sticker", "poster"]


def _load_tracker(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def count_designs() -> dict[str, int]:
    """Count available designs per folder."""
    counts = {}
    for folder in FOLDERS:
        folder_path = OUTPUT_DIR / folder
        if folder_path.is_dir():
            counts[folder] = len(list(folder_path.glob("*.png")))
        else:
            counts[folder] = 0
    return counts


def platform_stats(platform: str, info: dict) -> dict:
    """Get upload stats for a single platform."""
    tracker = _load_tracker(info["tracker"])

    if not tracker and "legacy_tracker" in info:
        tracker = _load_tracker(info["legacy_tracker"])

    success = sum(1 for v in tracker.values() if v.get("status") == "success")
    failed = sum(1 for v in tracker.values() if v.get("status") == "failed")

    key_prefix = info.get("key_prefix", "")
    by_folder = {}
    for folder in FOLDERS:
        folder_keys = [k for k in tracker if f"{folder}/" in k]
        if key_prefix:
            folder_keys = [k for k in tracker if k.startswith(f"{key_prefix}{folder}/")]
        else:
            folder_keys = [k for k in tracker if k.startswith(f"{folder}/") or f"/{folder}/" in k]
        folder_success = sum(1 for k in folder_keys if tracker[k].get("status") == "success")
        folder_failed = sum(1 for k in folder_keys if tracker[k].get("status") == "failed")
        by_folder[folder] = {"success": folder_success, "failed": folder_failed}

    return {
        "platform": platform,
        "success": success,
        "failed": failed,
        "total_tracked": len(tracker),
        "by_folder": by_folder,
        "type": info["type"],
    }


def get_all_upload_stats() -> dict:
    """Return full upload progress data for all platforms."""
    design_counts = count_designs()
    total_designs = sum(design_counts.values())

    platforms = {}
    grand_success = 0
    grand_failed = 0

    for name, info in PLATFORMS.items():
        stats = platform_stats(name, info)
        stats["remaining"] = total_designs - stats["success"]
        stats["pct"] = (stats["success"] / total_designs * 100) if total_designs else 0
        platforms[name] = stats
        grand_success += stats["success"]
        grand_failed += stats["failed"]

    grand_total = total_designs * len(PLATFORMS)

    return {
        "design_counts": design_counts,
        "total_designs": total_designs,
        "platforms": platforms,
        "grand_success": grand_success,
        "grand_failed": grand_failed,
        "grand_total": grand_total,
        "grand_pct": (grand_success / grand_total * 100) if grand_total else 0,
    }
