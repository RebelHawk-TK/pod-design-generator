#!/usr/bin/env python3
"""TikTok video uploader via browser automation (Playwright).

Uploads MP4 videos to TikTok Creator Center with captions and hashtags.
Uses a persistent browser session so you only log in once.

Setup:
    1. First run will open Chrome — log into TikTok manually
    2. Subsequent runs reuse the saved session

Usage:
    python3 upload_tiktok.py --source-dir output/videos --limit 1     # Test one
    python3 upload_tiktok.py --source-dir output/videos --dry-run      # Preview
    python3 upload_tiktok.py --source-dir output/videos --limit 5      # Batch
    python3 upload_tiktok.py --source-dir output/videos --retry-failed # Retry
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
    wait_for_cloudflare,
    CONSECUTIVE_FAILURE_LIMIT,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_DIR = Path(__file__).parent
TRACKER_FILE = PROJECT_DIR / "uploaded_tiktok.json"
VIDEO_DIR = PROJECT_DIR / "output" / "videos"

CHROME_PROFILE_DIR = PROJECT_DIR / ".chrome_profile"

TIKTOK_UPLOAD_URL = "https://www.tiktok.com/tiktokstudio/upload"
TIKTOK_DEFAULT_DELAY = 120  # 2 min between uploads

# Landmark metadata for captions
LANDMARKS = {
    "eiffel_tower": {"name": "Eiffel Tower", "location": "Paris", "tags": ["paris", "eiffeltower", "france"]},
    "taj_mahal": {"name": "Taj Mahal", "location": "India", "tags": ["tajmahal", "india", "agra"]},
    "colosseum": {"name": "Colosseum", "location": "Rome", "tags": ["colosseum", "rome", "italy"]},
    "great_wall": {"name": "Great Wall", "location": "China", "tags": ["greatwall", "china", "wonder"]},
    "notre_dame": {"name": "Notre-Dame", "location": "Paris", "tags": ["notredame", "paris", "gothic"]},
    "neuschwanstein": {"name": "Neuschwanstein", "location": "Bavaria", "tags": ["neuschwanstein", "castle", "germany"]},
    "mount_fuji": {"name": "Mount Fuji", "location": "Japan", "tags": ["mountfuji", "japan", "fujisan"]},
    "golden_gate": {"name": "Golden Gate Bridge", "location": "San Francisco", "tags": ["goldengate", "sanfrancisco", "california"]},
    "sydney_opera": {"name": "Sydney Opera House", "location": "Sydney", "tags": ["sydneyopera", "australia", "sydney"]},
    "santorini": {"name": "Santorini", "location": "Greece", "tags": ["santorini", "greece", "travel"]},
    "angkor_wat": {"name": "Angkor Wat", "location": "Cambodia", "tags": ["angkorwat", "cambodia", "temple"]},
    "machu_picchu": {"name": "Machu Picchu", "location": "Peru", "tags": ["machupicchu", "peru", "inca"]},
    "sagrada_familia": {"name": "Sagrada Familia", "location": "Barcelona", "tags": ["sagradafamilia", "barcelona", "gaudi"]},
    "parthenon": {"name": "Parthenon", "location": "Athens", "tags": ["parthenon", "athens", "greece"]},
    "stonehenge": {"name": "Stonehenge", "location": "England", "tags": ["stonehenge", "england", "ancient"]},
    "moai": {"name": "Moai Statues", "location": "Easter Island", "tags": ["moai", "easterisland", "mystery"]},
    "pyramids_giza": {"name": "Pyramids of Giza", "location": "Egypt", "tags": ["pyramids", "egypt", "giza"]},
    "petra": {"name": "Petra", "location": "Jordan", "tags": ["petra", "jordan", "rosecity"]},
    "st_basils": {"name": "St. Basil's Cathedral", "location": "Moscow", "tags": ["stbasils", "moscow", "russia"]},
    "chichen_itza": {"name": "Chichén Itzá", "location": "Mexico", "tags": ["chichenitza", "mexico", "maya"]},
    "christ_redeemer": {"name": "Christ the Redeemer", "location": "Rio", "tags": ["christredeemer", "rio", "brazil"]},
    "hagia_sophia": {"name": "Hagia Sophia", "location": "Istanbul", "tags": ["hagiasophia", "istanbul", "turkey"]},
    "tower_of_pisa": {"name": "Tower of Pisa", "location": "Italy", "tags": ["towerofpisa", "pisa", "italy"]},
    "big_ben": {"name": "Big Ben", "location": "London", "tags": ["bigben", "london", "england"]},
    "statue_of_liberty": {"name": "Statue of Liberty", "location": "New York", "tags": ["statueofliberty", "newyork", "nyc"]},
}

# Common hashtags for all videos
COMMON_TAGS = ["fineart", "artprint", "homedecor", "wallart", "moderndesignconcept", "shopsmall"]
TRAVEL_TAGS = ["travelfacts", "history", "didyouknow", "travelhistory", "worldwonders", "moderndesignconcept"]


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
    """Build a TikTok caption with hashtags for a landmark video."""
    info = LANDMARKS.get(landmark_id, {})
    name = info.get("name", landmark_id.replace("_", " ").title())
    location = info.get("location", "")
    specific_tags = info.get("tags", [])

    if is_travel:
        caption = f"Incredible facts about the {name}"
        if location:
            caption += f" | {location}"
        caption += "\nMore at moderndesignconcept.com"
        all_tags = specific_tags + TRAVEL_TAGS
    else:
        caption = f"{name} reimagined as fine art 🎨"
        if location:
            caption += f" | {location}"
        caption += "\nShop: moderndesignconcept.com"
        all_tags = specific_tags + COMMON_TAGS

    hashtags = " ".join(f"#{t}" for t in all_tags[:15])
    caption += f"\n{hashtags}"

    return caption[:2200]  # TikTok caption limit


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
    """Check if we're logged into TikTok."""
    try:
        page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=30000)
        time.sleep(5)
        wait_for_cloudflare(page)

        # If redirected to login, not authenticated
        url = page.url
        if "/login" in url:
            return False

        # Check for upload-related elements or URL
        if page.query_selector('input[type="file"]'):
            return True
        if page.query_selector('[class*="upload"]') or page.query_selector('[class*="creator"]'):
            return True

        return "tiktokstudio" in url or "creator" in url or "upload" in url
    except Exception:
        return False


def wait_for_login(page) -> None:
    """Navigate to TikTok login and wait for user to log in."""
    print("\n=== TikTok Login Required ===")
    print("  Log into your TikTok account in the browser window.")
    print("  Waiting up to 5 minutes...\n")

    page.goto("https://www.tiktok.com/login", wait_until="domcontentloaded", timeout=30000)

    deadline = time.time() + 300
    while time.time() < deadline:
        time.sleep(5)
        url = page.url
        if "/login" not in url and "tiktok.com" in url:
            print("  Login detected!")
            time.sleep(3)
            return

    print("  Login timeout — please try again.")


# ---------------------------------------------------------------------------
# Upload single video
# ---------------------------------------------------------------------------

def upload_single(page, video_path: Path, caption: str) -> None:
    """Upload a single video to TikTok via TikTok Studio."""
    # Navigate to upload page
    page.goto(TIKTOK_UPLOAD_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(5)
    wait_for_cloudflare(page)

    # Check if page loaded properly (TikTok sometimes shows error)
    if page.query_selector('text="Something went wrong"'):
        print(f"  TikTok showed error page, retrying...")
        page.reload(wait_until="domcontentloaded", timeout=30000)
        time.sleep(5)
        if page.query_selector('text="Something went wrong"'):
            raise RuntimeError("TikTok upload page failed to load (Something went wrong)")

    # TikTok may have a hidden file input — use locator to set files on it
    file_input = page.locator('input[type="file"]')
    if file_input.count() > 0:
        file_input.first.set_input_files(str(video_path))
        print(f"  Video file selected, waiting for upload...")
    else:
        raise RuntimeError("Could not find video file input on TikTok upload page")

    # Helper: click via JavaScript to bypass modal overlays
    def js_click(selector, timeout=15000):
        try:
            el = page.wait_for_selector(selector, timeout=timeout)
            if el:
                page.evaluate("el => el.click()", el)
                return True
        except Exception:
            return False
        return False

    def js_click_el(el):
        """Click an ElementHandle via JS to bypass overlays."""
        page.evaluate("el => el.click()", el)

    def dismiss_modals():
        """Try to dismiss any modal overlays (cover editor, copyright, etc.)."""
        # Try pressing Escape first
        page.keyboard.press("Escape")
        time.sleep(1)

        # Look for common dismiss buttons inside modals
        dismiss_selectors = [
            'button:has-text("Got it")',
            'button:has-text("OK")',
            'button:has-text("Done")',
            'button:has-text("Skip")',
            'button:has-text("Close")',
            'button:has-text("Confirm")',
            '[aria-label="Close"]',
            '[class*="modal"] button[class*="close"]',
            '[class*="Modal"] button[class*="close"]',
        ]
        for sel in dismiss_selectors:
            try:
                el = page.query_selector(sel)
                if el and el.is_visible():
                    page.evaluate("el => el.click()", el)
                    print(f"  Dismissed modal via: {sel}")
                    time.sleep(2)
                    return True
            except Exception:
                continue
        return False

    # Wait for video to process and editor to appear
    time.sleep(10)

    # Check for and dismiss any modal overlays
    has_modal = page.query_selector('.TUXModal-overlay, [class*="modal-overlay"], [class*="Modal-overlay"]')
    if has_modal:
        print(f"  Modal overlay detected, attempting to dismiss...")
        dismiss_modals()
        time.sleep(2)

    # Wait for the editor/caption area to appear
    caption_selectors = [
        '[data-text="true"]',
        '.DraftEditor-root',
        '[contenteditable="true"]',
        '.public-DraftEditor-content',
        'div[role="textbox"]',
        '[data-e2e="caption-editor"]',
    ]

    caption_el = None
    for attempt in range(3):
        # Dismiss modals each attempt in case they reappear
        if attempt > 0:
            dismiss_modals()
            time.sleep(1)

        for sel in caption_selectors:
            try:
                el = page.wait_for_selector(sel, timeout=10000)
                if el:
                    caption_el = el
                    print(f"  Found caption field via: {sel}")
                    break
            except Exception:
                continue
        if caption_el:
            break
        print(f"  Caption field not found (attempt {attempt+1}/3), waiting...")
        time.sleep(10)

    if caption_el:
        # Click via JS to bypass overlay, then type
        js_click_el(caption_el)
        time.sleep(0.5)
        page.keyboard.press("Meta+A")
        page.keyboard.press("Backspace")
        time.sleep(0.3)

        for line in caption.split("\n"):
            page.keyboard.type(line, delay=30)
            page.keyboard.press("Enter")
        print(f"  Caption entered")
    else:
        print(f"  Warning: Could not find caption field — uploading without caption")

    # Wait for video processing to finish before posting
    time.sleep(5)

    # Dismiss any new modals before clicking Post
    dismiss_modals()
    time.sleep(1)

    # Find and click the Post button via JS
    post_selectors = [
        'button:has-text("Post")',
        'button:has-text("Publish")',
        '[data-e2e="post-button"]',
    ]

    post_clicked = False
    for attempt in range(3):
        # Also try finding via evaluate for more control
        try:
            clicked = page.evaluate("""() => {
                const buttons = document.querySelectorAll('button');
                for (const btn of buttons) {
                    const text = btn.textContent.trim().toLowerCase();
                    if (text === 'post' || text === 'publish') {
                        btn.click();
                        return true;
                    }
                }
                return false;
            }""")
            if clicked:
                post_clicked = True
                break
        except Exception:
            pass

        for sel in post_selectors:
            if js_click(sel, timeout=10000):
                post_clicked = True
                break
        if post_clicked:
            break
        print(f"  Waiting for video processing (attempt {attempt+1}/3)...")
        dismiss_modals()
        time.sleep(15)

    if not post_clicked:
        # Last resort: screenshot for debug
        try:
            page.screenshot(path=str(PROJECT_DIR / "debug_tiktok_post.png"))
            print(f"  Debug screenshot saved to debug_tiktok_post.png")
        except Exception:
            pass
        raise RuntimeError("Could not find Post/Publish button")

    print(f"  Post button clicked, waiting for confirmation...")

    # Wait for success — poll for up to 60s
    success_selectors = [
        'text="Your video has been uploaded"',
        'text="Your video is being uploaded"',
        'text="Uploaded"',
        '[class*="success"]',
        'span:has-text("uploaded")',
    ]

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

    # If no confirmation but no error either, check URL
    url = page.url
    if "upload" not in url:
        print(f"  Upload likely succeeded (left upload page)")
        return

    print(f"  Warning: No explicit success confirmation, but no error detected")
    return


# ---------------------------------------------------------------------------
# Main upload loop
# ---------------------------------------------------------------------------

def run_tiktok_upload(args: argparse.Namespace) -> None:
    """Main TikTok upload flow."""
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
        # Use full filename stem as tracker key for uniqueness
        tracker_name = video_path.stem
        key = f"tiktok/{tracker_name}"
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
        print(f"\n=== TikTok upload session complete ===")
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
        description="Upload videos to TikTok via browser automation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python3 upload_tiktok.py --source-dir output/videos --limit 1       # Test one
  python3 upload_tiktok.py --source-dir output/videos --dry-run        # Preview
  python3 upload_tiktok.py --source-dir output/videos --limit 5        # Batch
  python3 upload_tiktok.py --source-dir output/videos --retry-failed   # Retry
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
        "--delay", type=float, default=TIKTOK_DEFAULT_DELAY,
        help=f"Seconds between uploads (default: {TIKTOK_DEFAULT_DELAY})",
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

    run_tiktok_upload(args)


if __name__ == "__main__":
    main()
