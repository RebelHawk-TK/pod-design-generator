#!/usr/bin/env python3
"""Instagram Reels uploader via Graph API (replaces Playwright browser automation).

Uploads MP4 videos as Instagram Reels using the Instagram Graph API.
Requires a Professional Instagram account linked to a Facebook Page.

Setup:
    1. Credentials stored in Keychain via keychain_config (instagram)
    2. Instagram account must be Professional (Business/Creator)
    3. Facebook Page must be linked to Instagram account

Usage:
    python3 upload_instagram_api.py --source-dir output/videos --limit 1     # Test one
    python3 upload_instagram_api.py --source-dir output/videos --dry-run      # Preview
    python3 upload_instagram_api.py --source-dir output/videos --limit 9      # Batch
    python3 upload_instagram_api.py --source-dir output/videos --retry-failed # Retry
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from keychain_config import load_config, save_config
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

GRAPH_API_VERSION = "v22.0"
GRAPH_API_BASE = f"https://graph.instagram.com/{GRAPH_API_VERSION}"

# Polling config for media container status
POLL_INTERVAL = 10  # seconds
POLL_TIMEOUT = 300  # 5 minutes max wait for processing

# Delay between uploads (Instagram rate limits)
INSTAGRAM_DEFAULT_DELAY = 60  # 1 min between uploads (API is faster than browser)

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
    # Phase 2+3 landmarks
    "acropolis_athens": {"name": "Acropolis of Athens", "location": "Athens, Greece", "tags": ["acropolis", "athens", "ancientgreece"]},
    "alhambra": {"name": "Alhambra", "location": "Granada, Spain", "tags": ["alhambra", "granada", "moorisharchitecture"]},
    "amsterdam_canals": {"name": "Amsterdam Canals", "location": "Amsterdam, Netherlands", "tags": ["amsterdam", "canals", "netherlands"]},
    "antelope_canyon": {"name": "Antelope Canyon", "location": "Arizona, USA", "tags": ["antelopecanyon", "arizona", "slotcanyon"]},
    "banff_national_park": {"name": "Banff National Park", "location": "Alberta, Canada", "tags": ["banff", "canada", "rockymountains"]},
    "blue_mosque": {"name": "Blue Mosque", "location": "Istanbul, Turkey", "tags": ["bluemosque", "istanbul", "ottoman"]},
    "bora_bora": {"name": "Bora Bora", "location": "French Polynesia", "tags": ["borabora", "frenchpolynesia", "paradise"]},
    "borobudur": {"name": "Borobudur", "location": "Java, Indonesia", "tags": ["borobudur", "indonesia", "buddhisttemple"]},
    "brooklyn_bridge": {"name": "Brooklyn Bridge", "location": "New York, USA", "tags": ["brooklynbridge", "nyc", "newyork"]},
    "buckingham_palace": {"name": "Buckingham Palace", "location": "London, England", "tags": ["buckinghampalace", "london", "royalpalace"]},
    "burj_khalifa": {"name": "Burj Khalifa", "location": "Dubai, UAE", "tags": ["burjkhalifa", "dubai", "tallestbuilding"]},
    "cappadocia": {"name": "Cappadocia", "location": "Turkey", "tags": ["cappadocia", "turkey", "hotairballoon"]},
    "cinque_terre": {"name": "Cinque Terre", "location": "Italy", "tags": ["cinqueterre", "italy", "italianriviera"]},
    "dubai_frame": {"name": "Dubai Frame", "location": "Dubai, UAE", "tags": ["dubaiframe", "dubai", "modernarchitecture"]},
    "forbidden_city": {"name": "Forbidden City", "location": "Beijing, China", "tags": ["forbiddencity", "beijing", "imperialpalace"]},
    "grand_canyon": {"name": "Grand Canyon", "location": "Arizona, USA", "tags": ["grandcanyon", "arizona", "naturalwonder"]},
    "great_barrier_reef": {"name": "Great Barrier Reef", "location": "Australia", "tags": ["greatbarrierreef", "australia", "coralreef"]},
    "hallstatt": {"name": "Hallstatt", "location": "Austria", "tags": ["hallstatt", "austria", "alpinevillage"]},
    "iguazu_falls": {"name": "Iguazu Falls", "location": "Argentina/Brazil", "tags": ["iguazufalls", "waterfall", "southamerica"]},
    "kilimanjaro": {"name": "Mount Kilimanjaro", "location": "Tanzania", "tags": ["kilimanjaro", "tanzania", "africa"]},
    "kyoto_bamboo": {"name": "Kyoto Bamboo Grove", "location": "Kyoto, Japan", "tags": ["kyoto", "bamboogrove", "japan"]},
    "lake_bled": {"name": "Lake Bled", "location": "Slovenia", "tags": ["lakebled", "slovenia", "fairytale"]},
    "lofoten": {"name": "Lofoten Islands", "location": "Norway", "tags": ["lofoten", "norway", "arcticbeauty"]},
    "louvre": {"name": "Louvre Museum", "location": "Paris, France", "tags": ["louvre", "paris", "artmuseum"]},
    "maldives": {"name": "Maldives", "location": "Maldives", "tags": ["maldives", "tropicalisland", "overwater"]},
    "meteora": {"name": "Meteora", "location": "Greece", "tags": ["meteora", "greece", "monasteries"]},
    "mont_saint_michel": {"name": "Mont Saint-Michel", "location": "Normandy, France", "tags": ["montsaintmichel", "france", "medieval"]},
    "niagara_falls": {"name": "Niagara Falls", "location": "USA/Canada", "tags": ["niagarafalls", "waterfall", "naturalwonder"]},
    "palace_versailles": {"name": "Palace of Versailles", "location": "France", "tags": ["versailles", "france", "palace"]},
    "plitvice_lakes": {"name": "Plitvice Lakes", "location": "Croatia", "tags": ["plitvicelakes", "croatia", "waterfalls"]},
    "prague_castle": {"name": "Prague Castle", "location": "Prague, Czech Republic", "tags": ["praguecastle", "prague", "medieval"]},
    "rio_carnival": {"name": "Rio Carnival", "location": "Rio de Janeiro, Brazil", "tags": ["riocarnival", "brazil", "samba"]},
    "santorini_blue_domes": {"name": "Santorini Blue Domes", "location": "Santorini, Greece", "tags": ["santorini", "bluedomes", "greece"]},
    "serengeti": {"name": "Serengeti", "location": "Tanzania", "tags": ["serengeti", "safari", "wildlife"]},
    "suez_canal": {"name": "Suez Canal", "location": "Egypt", "tags": ["suezcanal", "egypt", "waterway"]},
    "table_mountain": {"name": "Table Mountain", "location": "Cape Town, South Africa", "tags": ["tablemountain", "capetown", "southafrica"]},
    "temple_heaven": {"name": "Temple of Heaven", "location": "Beijing, China", "tags": ["templeofheaven", "beijing", "china"]},
    "toledo": {"name": "Toledo", "location": "Spain", "tags": ["toledo", "spain", "medievalcity"]},
    "torres_del_paine": {"name": "Torres del Paine", "location": "Patagonia, Chile", "tags": ["torresdelpaine", "patagonia", "chile"]},
    "venice": {"name": "Venice", "location": "Italy", "tags": ["venice", "italy", "gondola"]},
    "victoria_falls": {"name": "Victoria Falls", "location": "Zambia/Zimbabwe", "tags": ["victoriafalls", "africa", "waterfall"]},
    "wat_arun": {"name": "Wat Arun", "location": "Bangkok, Thailand", "tags": ["watarun", "bangkok", "thailand"]},
    "yellowstone": {"name": "Yellowstone", "location": "Wyoming, USA", "tags": ["yellowstone", "nationalpark", "geysers"]},
    "zhangjiajie": {"name": "Zhangjiajie", "location": "Hunan, China", "tags": ["zhangjiajie", "china", "avatarmountains"]},
}

COMMON_TAGS = [
    "fineart", "artprint", "wallart", "homedecor", "artlovers",
    "moderndesignconcept", "reelsart", "artreels", "travelart",
]
TRAVEL_TAGS = [
    "travelfacts", "history", "didyouknow", "travelhistory", "worldwonders",
    "traveltiktok", "learnontiktok", "moderndesignconcept", "reelsart", "travelart",
]
STOCK_TAGS = [
    "travelcinematic", "wanderlust", "explore", "beautifuldestinations",
    "travelgram", "moderndesignconcept", "reelsart", "travelart",
]


# ---------------------------------------------------------------------------
# Graph API helpers
# ---------------------------------------------------------------------------

def _api_request(url: str, method: str = "GET", data: dict | None = None) -> dict:
    """Make a Graph API request. Returns parsed JSON response."""
    if method == "GET" and data:
        url = f"{url}?{urlencode(data)}"
        req = Request(url)
    elif method == "POST" and data:
        encoded = urlencode(data).encode()
        req = Request(url, data=encoded, method="POST")
    else:
        req = Request(url, method=method)

    try:
        with urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"Graph API error {e.code}: {body}") from e


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_video_info(filename_stem: str) -> tuple[str, str]:
    """Extract landmark ID and video type from filename.

    Returns:
        (landmark_id, video_type) where video_type is 'promo', 'travel', or 'stock'.
    """
    for suffix in ("_travel_a", "_travel_b"):
        if filename_stem.endswith(suffix):
            return filename_stem[: -len(suffix)], "travel"
    for suffix in ("_stock_a", "_stock_b"):
        if filename_stem.endswith(suffix):
            return filename_stem[: -len(suffix)], "stock"
    return filename_stem, "promo"


# ---------------------------------------------------------------------------
# Caption builder
# ---------------------------------------------------------------------------

def build_caption(landmark_id: str, *, video_type: str = "promo") -> str:
    """Build an Instagram caption with hashtags for a landmark video."""
    info = LANDMARKS.get(landmark_id, {})
    name = info.get("name", landmark_id.replace("_", " ").title())
    location = info.get("location", "")
    specific_tags = info.get("tags", [])

    if video_type == "travel":
        caption = f"Incredible facts about the {name}"
        if location:
            caption += f"\n📍 {location}"
        caption += "\n\nMore art inspired by world landmarks → moderndesignconcept.com (link in bio)"
        all_tags = specific_tags + TRAVEL_TAGS
    elif video_type == "stock":
        caption = f"The beauty of {name}"
        if location:
            caption += f"\n📍 {location}"
        caption += "\n\nShop art prints inspired by world landmarks → moderndesignconcept.com (link in bio)"
        all_tags = specific_tags + STOCK_TAGS
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

def discover_videos(source_dir: Path) -> list[tuple[Path, str, str]]:
    """Find MP4 videos and extract metadata from filenames.

    Returns list of (video_path, landmark_id, video_type) tuples.
    """
    if not source_dir.is_dir():
        print(f"Error: video directory not found: {source_dir}")
        sys.exit(1)

    videos = []
    for mp4 in sorted(source_dir.glob("*.mp4")):
        landmark_id, video_type = _extract_video_info(mp4.stem)
        videos.append((mp4, landmark_id, video_type))

    return videos


# ---------------------------------------------------------------------------
# Instagram Graph API upload flow (Resumable Upload)
# ---------------------------------------------------------------------------

def _poll_container(container_id: str, access_token: str) -> None:
    """Poll a media container until status is FINISHED."""
    deadline = time.time() + POLL_TIMEOUT
    while time.time() < deadline:
        status_resp = _api_request(
            f"{GRAPH_API_BASE}/{container_id}",
            data={
                "fields": "id,status,status_code",
                "access_token": access_token,
            },
        )
        status_code = status_resp.get("status_code", "UNKNOWN")
        print(f"  Container status: {status_code}")

        if status_code == "FINISHED":
            return
        elif status_code == "ERROR":
            error_msg = status_resp.get("status", "Unknown error")
            raise RuntimeError(f"Container processing failed: {error_msg}")
        elif status_code == "EXPIRED":
            raise RuntimeError("Container expired before publishing")

        time.sleep(POLL_INTERVAL)

    raise RuntimeError(f"Container processing timed out after {POLL_TIMEOUT}s")


def _upload_to_temp_host(video_path: Path) -> str:
    """Upload a video file to a temporary public host and return a direct download URL.

    Uses tmpfiles.org (files auto-expire after 1 hour).
    """
    import subprocess

    file_size_mb = video_path.stat().st_size / 1024 / 1024
    print(f"  Uploading to temp host ({file_size_mb:.1f} MB)...")

    result = subprocess.run(
        ["curl", "-s", "-F", f"file=@{video_path}", "https://tmpfiles.org/api/v1/upload"],
        capture_output=True, text=True, timeout=300,
    )

    if result.returncode != 0:
        raise RuntimeError(f"tmpfiles.org upload failed: {result.stderr}")

    resp = json.loads(result.stdout)
    if resp.get("status") != "success":
        raise RuntimeError(f"tmpfiles.org upload failed: {resp}")

    # Convert page URL to direct download URL by inserting /dl/ after domain
    page_url = resp["data"]["url"]
    direct_url = page_url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
    # Ensure HTTPS
    if direct_url.startswith("http://"):
        direct_url = direct_url.replace("http://", "https://", 1)

    print(f"  Temp URL: {direct_url}")
    return direct_url


def upload_reel_from_file(
    ig_user_id: str,
    access_token: str,
    video_path: Path,
    caption: str,
) -> str:
    """Upload a local video file as an Instagram Reel.

    The Instagram Graph API requires a publicly accessible video_url.
    We upload the video to a temporary file host (file.io) to get a
    public URL, then pass that URL to the Instagram API.

    Flow:
        1. Upload video to temp host for a public URL
        2. Create a media container with the public video_url
        3. Poll until container status is FINISHED
        4. Publish the container

    Returns:
        Published media ID
    """
    # Step 1: Get a public URL for the video
    video_url = _upload_to_temp_host(video_path)

    # Step 2: Create media container
    container_resp = _api_request(
        f"{GRAPH_API_BASE}/{ig_user_id}/media",
        method="POST",
        data={
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "access_token": access_token,
        },
    )
    container_id = container_resp["id"]
    print(f"  Container created: {container_id}")

    # Step 3: Poll container status until FINISHED
    _poll_container(container_id, access_token)

    # Step 4: Publish
    publish_resp = _api_request(
        f"{GRAPH_API_BASE}/{ig_user_id}/media_publish",
        method="POST",
        data={
            "creation_id": container_id,
            "access_token": access_token,
        },
    )
    media_id = publish_resp["id"]
    print(f"  Published: {media_id}")

    return media_id


# ---------------------------------------------------------------------------
# Main upload loop
# ---------------------------------------------------------------------------

def _maybe_refresh_token(config: dict) -> str:
    """Refresh the long-lived token if it's within 7 days of expiry.

    Instagram long-lived tokens last 60 days. We refresh proactively
    so the nightly cron never hits an expired token.
    """
    access_token = config["access_token"]

    try:
        # Try a refresh — only succeeds for valid long-lived tokens
        resp = _api_request(
            "https://graph.instagram.com/refresh_access_token",
            data={
                "grant_type": "ig_refresh_token",
                "access_token": access_token,
            },
        )
        new_token = resp.get("access_token")
        if new_token and new_token != access_token:
            config["access_token"] = new_token
            save_config("instagram", config)
            expires_days = resp.get("expires_in", 0) / 86400
            print(f"  Token refreshed (expires in {expires_days:.0f} days)")
            return new_token
    except Exception:
        pass  # Token still valid, refresh not needed yet

    return access_token


def run_instagram_upload(args: argparse.Namespace) -> None:
    """Main Instagram upload flow via Graph API."""
    # Load credentials and auto-refresh token
    config = load_config("instagram")
    access_token = _maybe_refresh_token(config)
    ig_user_id = config.get("ig_user_id", "26401815412746202")

    source_dir = Path(args.source_dir) if args.source_dir else VIDEO_DIR

    videos = discover_videos(source_dir)
    if not videos:
        print(f"No videos found in {source_dir}")
        return

    print(f"Found {len(videos)} videos in {source_dir}")

    # Load tracker
    tracker = load_tracker(TRACKER_FILE)

    to_upload = []
    for video_path, landmark_id, video_type in videos:
        key = f"instagram/{video_path.stem}"
        entry = tracker.get(key, {})
        status = entry.get("status")

        if args.retry_failed and status == "failed":
            to_upload.append((video_path, landmark_id, key, video_type))
        elif status == "success":
            continue
        elif not args.retry_failed:
            to_upload.append((video_path, landmark_id, key, video_type))

    if not to_upload:
        print("No videos to upload (all already uploaded or no failures to retry).")
        return

    if args.limit and args.limit > 0:
        to_upload = to_upload[:args.limit]

    print(f"Will {'preview' if args.dry_run else 'upload'} {len(to_upload)} videos\n")

    # Dry run
    if args.dry_run:
        for i, (video_path, landmark_id, key, video_type) in enumerate(to_upload, 1):
            caption = build_caption(landmark_id, video_type=video_type)
            print(f"  [{i}] {key} ({video_type})")
            print(f"       File: {video_path.name}")
            print(f"       Caption: {caption[:80]}...")
            print()
        print("Dry run complete — no uploads performed.")
        return

    # Upload loop
    consecutive_failures = 0
    uploaded_count = 0

    for i, (video_path, landmark_id, key, video_type) in enumerate(to_upload, 1):
        caption = build_caption(landmark_id, video_type=video_type)
        print(f"[{i}/{len(to_upload)}] Uploading: {video_path.name} ({video_type})")
        print(f"  Landmark: {landmark_id}")

        try:
            media_id = upload_reel_from_file(
                ig_user_id=ig_user_id,
                access_token=access_token,
                video_path=video_path,
                caption=caption,
            )
            tracker[key] = {
                "status": "success",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "media_id": media_id,
                "error": None,
            }
            save_tracker(tracker, TRACKER_FILE)
            consecutive_failures = 0
            uploaded_count += 1
            print(f"  -> Success (media_id: {media_id})")

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
    print(f"\n=== Instagram API upload session complete ===")
    print(f"  Uploaded: {uploaded_count}/{len(to_upload)}")
    failed = sum(1 for _, _, k, _ in to_upload if tracker.get(k, {}).get("status") == "failed")
    if failed:
        print(f"  Failed: {failed}")
        print(f"  Re-run with --retry-failed to retry")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Upload videos as Instagram Reels via Graph API.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python3 upload_instagram_api.py --source-dir output/videos --limit 1       # Test one
  python3 upload_instagram_api.py --source-dir output/videos --dry-run        # Preview
  python3 upload_instagram_api.py --source-dir output/videos --limit 9        # Batch
  python3 upload_instagram_api.py --source-dir output/videos --retry-failed   # Retry
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
