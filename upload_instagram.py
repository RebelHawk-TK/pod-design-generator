#!/usr/bin/env python3
"""Instagram Reels uploader via browser automation (Playwright).

Uploads MP4 videos as Instagram Reels with captions and hashtags.
Uses a persistent browser session so you only log in once.

Setup:
    1. First run will open Chrome — log into Instagram manually
    2. Subsequent runs reuse the saved session

Usage:
    python3 upload_instagram.py --source-dir output/videos --limit 1     # Test one
    python3 upload_instagram.py --source-dir output/videos --dry-run      # Preview
    python3 upload_instagram.py --source-dir output/videos --limit 5      # Batch
    python3 upload_instagram.py --source-dir output/videos --retry-failed # Retry
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from upload_common import (
    load_tracker,
    save_tracker,
    record_upload,
    jittered_delay,
    CONSECUTIVE_FAILURE_LIMIT,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_DIR = Path(__file__).parent
TRACKER_FILE = PROJECT_DIR / "uploaded_instagram.json"
VIDEO_DIR = PROJECT_DIR / "output" / "videos"

CHROME_PROFILE_DIR = PROJECT_DIR / ".chrome_profile"

INSTAGRAM_CREATE_URL = "https://www.instagram.com/"
INSTAGRAM_DEFAULT_DELAY = 120  # 2 min between uploads

# Landmark metadata for captions
LANDMARKS = {
    "eiffel_tower": {"name": "Eiffel Tower", "location": "Paris, France", "tags": ["eiffeltower", "paris", "parisart"]},
    "taj_mahal": {"name": "Taj Mahal", "location": "Agra, India", "tags": ["tajmahal", "india", "incredibleindia"]},
    "colosseum": {"name": "Colosseum", "location": "Rome, Italy", "tags": ["colosseum", "rome", "italyart"]},
    "great_wall": {"name": "Great Wall", "location": "China", "tags": ["greatwallofchina", "china", "wonderoftheworld"]},
    "notre_dame": {"name": "Notre-Dame", "location": "Paris, France", "tags": ["notredame", "paris", "gothicart"]},
    "neuschwanstein": {"name": "Neuschwanstein", "location": "Bavaria, Germany", "tags": ["neuschwanstein", "bavaria", "fairytalecastle"]},
    "mount_fuji": {"name": "Mount Fuji", "location": "Japan", "tags": ["mountfuji", "japan", "fujisan"]},
    "golden_gate": {"name": "Golden Gate Bridge", "location": "San Francisco", "tags": ["goldengatebridge", "sanfrancisco", "california"]},
    "sydney_opera": {"name": "Sydney Opera House", "location": "Sydney, Australia", "tags": ["sydneyoperahouse", "sydney", "australia"]},
    "santorini": {"name": "Santorini", "location": "Greece", "tags": ["santorini", "greece", "greekislands"]},
    "angkor_wat": {"name": "Angkor Wat", "location": "Cambodia", "tags": ["angkorwat", "cambodia", "ancienttemple"]},
    "machu_picchu": {"name": "Machu Picchu", "location": "Peru", "tags": ["machupicchu", "peru", "incatrail"]},
    "sagrada_familia": {"name": "Sagrada Familia", "location": "Barcelona, Spain", "tags": ["sagradafamilia", "barcelona", "gaudi"]},
    "parthenon": {"name": "Parthenon", "location": "Athens, Greece", "tags": ["parthenon", "athens", "greekhistory"]},
    "stonehenge": {"name": "Stonehenge", "location": "England", "tags": ["stonehenge", "england", "ancientmonument"]},
    "moai": {"name": "Moai Statues", "location": "Easter Island", "tags": ["moai", "easterisland", "rapanui"]},
    "pyramids_giza": {"name": "Pyramids of Giza", "location": "Egypt", "tags": ["pyramidsofgiza", "egypt", "ancientegypt"]},
    "petra": {"name": "Petra", "location": "Jordan", "tags": ["petra", "jordan", "rosecity"]},
    "st_basils": {"name": "St. Basil's Cathedral", "location": "Moscow", "tags": ["stbasils", "moscow", "russianart"]},
    "chichen_itza": {"name": "Chichén Itzá", "location": "Mexico", "tags": ["chichenitza", "mexico", "mayanruins"]},
    "christ_redeemer": {"name": "Christ the Redeemer", "location": "Rio de Janeiro", "tags": ["christtheredeemer", "riodejaneiro", "brazil"]},
    "hagia_sophia": {"name": "Hagia Sophia", "location": "Istanbul, Turkey", "tags": ["hagiasophia", "istanbul", "turkeytravel"]},
    "tower_of_pisa": {"name": "Tower of Pisa", "location": "Pisa, Italy", "tags": ["towerofpisa", "pisa", "leaningtower"]},
    "big_ben": {"name": "Big Ben", "location": "London, England", "tags": ["bigben", "london", "unitedkingdom"]},
    "statue_of_liberty": {"name": "Statue of Liberty", "location": "New York", "tags": ["statueofliberty", "newyork", "nyc"]},
}

COMMON_TAGS = [
    "fineart", "artprint", "wallart", "homedecor", "artlovers",
    "moderndesignconcept", "reelsart", "artreels", "travelart",
]
TRAVEL_TAGS = [
    "travelfacts", "history", "didyouknow", "travelhistory", "worldwonders",
    "traveltiktok", "learnontiktok", "moderndesignconcept", "reelsart", "travelart",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_landmark_id(filename_stem: str) -> tuple[str, bool]:
    """Extract landmark ID from filename, detecting travel videos.

    Returns:
        (landmark_id, is_travel) tuple.
        e.g. "eiffel_tower_travel_a" -> ("eiffel_tower", True)
             "eiffel_tower"          -> ("eiffel_tower", False)
    """
    for suffix in ("_travel_a", "_travel_b"):
        if filename_stem.endswith(suffix):
            return filename_stem[: -len(suffix)], True
    return filename_stem, False


# ---------------------------------------------------------------------------
# Caption builder
# ---------------------------------------------------------------------------

def build_caption(landmark_id: str, *, is_travel: bool = False) -> str:
    """Build an Instagram caption with hashtags for a landmark video."""
    info = LANDMARKS.get(landmark_id, {})
    name = info.get("name", landmark_id.replace("_", " ").title())
    location = info.get("location", "")
    specific_tags = info.get("tags", [])

    if is_travel:
        caption = f"Incredible facts about the {name}"
        if location:
            caption += f"\n📍 {location}"
        caption += "\n\nMore art inspired by world landmarks → moderndesignconcept.com (link in bio)"
        all_tags = specific_tags + TRAVEL_TAGS
    else:
        caption = f"{name} reimagined as fine art 🎨"
        if location:
            caption += f"\n📍 {location}"
        caption += "\n\nShop the full collection → moderndesignconcept.com (link in bio)"
        all_tags = specific_tags + COMMON_TAGS

    hashtags = " ".join(f"#{t}" for t in all_tags[:20])
    caption += f"\n\n{hashtags}"

    return caption[:2200]  # Instagram caption limit


# ---------------------------------------------------------------------------
# Video discovery
# ---------------------------------------------------------------------------

def discover_videos(source_dir: Path) -> list[tuple[Path, str, bool]]:
    """Find MP4 videos and extract landmark IDs from filenames.

    Returns list of (video_path, landmark_id, is_travel) tuples.
    """
    if not source_dir.is_dir():
        print(f"Error: video directory not found: {source_dir}")
        sys.exit(1)

    videos = []
    for mp4 in sorted(source_dir.glob("*.mp4")):
        landmark_id, is_travel = _extract_landmark_id(mp4.stem)
        videos.append((mp4, landmark_id, is_travel))

    return videos


# ---------------------------------------------------------------------------
# Browser session
# ---------------------------------------------------------------------------

def check_session(page) -> bool:
    """Check if we're logged into Instagram."""
    try:
        page.goto("https://www.instagram.com/", wait_until="domcontentloaded", timeout=30000)
        time.sleep(4)

        url = page.url
        if "/accounts/login" in url:
            return False

        # Look for elements that indicate we're logged in
        logged_in_indicators = [
            'svg[aria-label="New post"]',
            'svg[aria-label="Home"]',
            'a[href="/direct/inbox/"]',
            '[aria-label="Search"]',
        ]
        for sel in logged_in_indicators:
            if page.query_selector(sel):
                return True

        return False
    except Exception:
        return False


def wait_for_login(page) -> None:
    """Navigate to Instagram login and wait for user to log in."""
    print("\n=== Instagram Login Required ===")
    print("  Log into your Instagram account in the browser window.")
    print("  Waiting up to 5 minutes...\n")

    page.goto("https://www.instagram.com/accounts/login/", wait_until="domcontentloaded", timeout=30000)

    deadline = time.time() + 300
    while time.time() < deadline:
        time.sleep(5)
        url = page.url
        if "/accounts/login" not in url and "instagram.com" in url:
            print("  Login detected!")
            time.sleep(3)
            return

    print("  Login timeout — please try again.")


# ---------------------------------------------------------------------------
# Upload single video
# ---------------------------------------------------------------------------

def upload_single(page, video_path: Path, caption: str) -> None:
    """Upload a single video as an Instagram Reel."""
    # Go to Instagram home
    page.goto("https://www.instagram.com/", wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)

    # Click the "New post" / Create button
    create_selectors = [
        'svg[aria-label="New post"]',
        '[aria-label="New post"]',
        'a[href="/create/style/"]',
        'span:has-text("Create")',
    ]

    create_btn = None
    for sel in create_selectors:
        try:
            el = page.wait_for_selector(sel, timeout=10000)
            if el:
                create_btn = el
                break
        except Exception:
            continue

    if not create_btn:
        raise RuntimeError("Could not find Create/New Post button")

    create_btn.click()
    time.sleep(2)

    # Instagram hides the file input — use locator to set files on hidden input
    file_input = page.locator('input[type="file"][accept*="video"]')
    if file_input.count() == 0:
        # Try clicking "Select from computer" button first
        select_selectors = [
            'button:has-text("Select from computer")',
            'button:has-text("Select From Computer")',
            'button:has-text("Select from")',
        ]
        for sel in select_selectors:
            try:
                btn = page.wait_for_selector(sel, timeout=5000)
                if btn:
                    btn.click()
                    time.sleep(1)
                    break
            except Exception:
                continue

        file_input = page.locator('input[type="file"]')

    if file_input.count() == 0:
        raise RuntimeError("Could not find file input for video upload")

    file_input.first.set_input_files(str(video_path))
    print(f"  Video file selected, waiting for processing...")
    time.sleep(5)

    # Instagram shows crop/edit screens — click Next/Continue using JS click
    # to avoid overlay interception from video preview controls
    def js_click(selector, timeout=15000):
        """Click via JavaScript to bypass overlay interception."""
        try:
            el = page.wait_for_selector(selector, timeout=timeout)
            if el:
                page.evaluate("el => el.click()", el)
                return True
        except Exception:
            return False
        return False

    # May need to click Next multiple times (crop → filter → caption)
    for step in range(3):
        time.sleep(3)
        clicked = False
        for sel in ['div[role="button"]:has-text("Next")', 'button:has-text("Next")', '[aria-label="Next"]']:
            if js_click(sel, timeout=10000):
                clicked = True
                print(f"  Clicked Next (step {step + 1})")
                break
        if not clicked:
            break

    time.sleep(2)

    # Now we should be on the caption screen
    caption_selectors = [
        'textarea[aria-label="Write a caption..."]',
        'textarea[aria-label*="caption"]',
        'div[role="textbox"][aria-label*="caption"]',
        'div[contenteditable="true"][role="textbox"]',
        'textarea[placeholder*="caption"]',
    ]

    caption_el = None
    for sel in caption_selectors:
        try:
            caption_el = page.wait_for_selector(sel, timeout=10000)
            if caption_el:
                break
        except Exception:
            continue

    if caption_el:
        caption_el.click()
        time.sleep(0.5)
        page.keyboard.type(caption, delay=10)
        print(f"  Caption entered")
    else:
        print(f"  Warning: Could not find caption field")

    time.sleep(2)

    # Click Share/Post via JS to bypass overlay
    share_clicked = False
    for sel in ['div[role="button"]:has-text("Share")', 'button:has-text("Share")', 'button:has-text("Post")']:
        if js_click(sel, timeout=10000):
            share_clicked = True
            break

    if not share_clicked:
        raise RuntimeError("Could not find Share/Post button")

    print(f"  Share button clicked, waiting for upload...")

    # Wait for success confirmation — Instagram shows "Your reel has been shared"
    success_selectors = [
        'text="Your reel has been shared."',
        'text="Reel shared"',
        'img[alt="Animated checkmark"]',
        'span:has-text("Your reel has been shared")',
        'span:has-text("shared")',
    ]

    # Poll for up to 60 seconds for success confirmation
    deadline = time.time() + 60
    while time.time() < deadline:
        for sel in success_selectors:
            try:
                if page.query_selector(sel):
                    print(f"  Upload confirmed!")
                    time.sleep(2)
                    return
            except Exception:
                continue
        time.sleep(3)

    # If we didn't see a confirmation, check if we're back on the feed (also success)
    url = page.url
    if "/create" not in url and "/upload" not in url:
        print(f"  Upload likely succeeded (returned to feed)")
        return

    raise RuntimeError("Upload not confirmed — no success message seen after 60s")


# ---------------------------------------------------------------------------
# Main upload loop
# ---------------------------------------------------------------------------

def run_instagram_upload(args: argparse.Namespace) -> None:
    """Main Instagram upload flow."""
    source_dir = Path(args.source_dir) if args.source_dir else VIDEO_DIR

    videos = discover_videos(source_dir)
    if not videos:
        print(f"No videos found in {source_dir}")
        return

    print(f"Found {len(videos)} videos in {source_dir}")

    # Load tracker and filter
    tracker = load_tracker(TRACKER_FILE)

    to_upload = []
    for video_path, landmark_id, is_travel in videos:
        tracker_name = video_path.stem
        key = f"instagram/{tracker_name}"
        entry = tracker.get(key, {})
        status = entry.get("status")

        if args.retry_failed and status == "failed":
            to_upload.append((video_path, landmark_id, key, is_travel))
        elif status == "success":
            continue
        elif not args.retry_failed:
            to_upload.append((video_path, landmark_id, key, is_travel))

    if not to_upload:
        print("No videos to upload (all already uploaded or no failures to retry).")
        return

    if args.limit and args.limit > 0:
        to_upload = to_upload[:args.limit]

    print(f"Will {'preview' if args.dry_run else 'upload'} {len(to_upload)} videos\n")

    # Dry run
    if args.dry_run:
        for i, (video_path, landmark_id, key, is_travel) in enumerate(to_upload, 1):
            caption = build_caption(landmark_id, is_travel=is_travel)
            vtype = "travel" if is_travel else "promo"
            print(f"  [{i}] {key} ({vtype})")
            print(f"       File: {video_path.name}")
            print(f"       Caption: {caption[:80]}...")
            print()
        print("Dry run complete — no uploads performed.")
        return

    # Launch browser using real Chrome profile
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(CHROME_PROFILE_DIR),
            channel="chrome",
            headless=False,
            slow_mo=100,
            viewport={"width": 1280, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
            ignore_default_args=["--enable-automation"],
        )
        page = context.pages[0] if context.pages else context.new_page()

        if not check_session(page):
            wait_for_login(page)
            if not check_session(page):
                print("Error: still not logged in. Exiting.")
                context.close()
                return

        print("Session valid — starting uploads\n")

        consecutive_failures = 0
        uploaded_count = 0

        for i, (video_path, landmark_id, key, is_travel) in enumerate(to_upload, 1):
            caption = build_caption(landmark_id, is_travel=is_travel)
            vtype = "travel" if is_travel else "promo"
            print(f"[{i}/{len(to_upload)}] Uploading: {video_path.name} ({vtype})")
            print(f"  Landmark: {landmark_id}")

            try:
                upload_single(page, video_path, caption)
                record_upload(tracker, TRACKER_FILE, key, "success")
                consecutive_failures = 0
                uploaded_count += 1
                print(f"  -> Success")

            except Exception as e:
                record_upload(tracker, TRACKER_FILE, key, "failed", str(e))
                consecutive_failures += 1
                print(f"  -> Failed: {e}")

            if consecutive_failures >= CONSECUTIVE_FAILURE_LIMIT:
                print(f"\n=== {CONSECUTIVE_FAILURE_LIMIT} consecutive failures — stopping ===")
                break

            # Delay between uploads
            if i < len(to_upload):
                wait_time = jittered_delay(args.delay)
                print(f"  Waiting {wait_time:.0f}s before next upload...")
                time.sleep(wait_time)

        # Summary
        print(f"\n=== Instagram upload session complete ===")
        print(f"  Uploaded: {uploaded_count}/{len(to_upload)}")
        failed = sum(1 for _, _, k, _ in to_upload if tracker.get(k, {}).get("status") == "failed")
        if failed:
            print(f"  Failed: {failed}")
            print(f"  Re-run with --retry-failed to retry")

        context.close()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Upload videos as Instagram Reels via browser automation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python3 upload_instagram.py --source-dir output/videos --limit 1       # Test one
  python3 upload_instagram.py --source-dir output/videos --dry-run        # Preview
  python3 upload_instagram.py --source-dir output/videos --limit 5        # Batch
  python3 upload_instagram.py --source-dir output/videos --retry-failed   # Retry
""",
    )
    parser.add_argument(
        "--source-dir", default=str(VIDEO_DIR),
        help=f"Directory containing MP4 video files (default: {VIDEO_DIR})",
    )
    parser.add_argument(
        "--limit", type=int, default=0,
        help="Max videos to upload (0 = all)",
    )
    parser.add_argument(
        "--delay", type=float, default=INSTAGRAM_DEFAULT_DELAY,
        help=f"Seconds between uploads (default: {INSTAGRAM_DEFAULT_DELAY})",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview uploads without actually uploading",
    )
    parser.add_argument(
        "--retry-failed", action="store_true",
        help="Only retry previously failed uploads",
    )
    args = parser.parse_args()

    if args.limit == 0:
        args.limit = None

    run_instagram_upload(args)


if __name__ == "__main__":
    main()
