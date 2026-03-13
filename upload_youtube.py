#!/usr/bin/env python3
"""YouTube Shorts uploader via YouTube Data API v3.

Uploads MP4 videos as YouTube Shorts with captions and hashtags.
Uses OAuth 2.0 with stored refresh token for unattended uploads.

Setup:
    1. Create OAuth credentials at https://console.cloud.google.com
    2. Download client_secrets.json to this directory
    3. Run: python3 upload_youtube.py --auth   (one-time authorization)
    4. Run: python3 upload_youtube.py --upload --limit 5

Usage:
    python3 upload_youtube.py --auth                          # Authorize
    python3 upload_youtube.py --upload --limit 5              # Upload 5 videos
    python3 upload_youtube.py --upload --dry-run --limit 10   # Preview
    python3 upload_youtube.py --upload --retry-failed         # Retry failures
    python3 upload_youtube.py --status                        # Check stats
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httplib2
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_DIR = Path(__file__).parent
CLIENT_SECRETS_FILE = PROJECT_DIR / "client_secrets.json"
TOKEN_FILE = PROJECT_DIR / ".youtube_token.json"
TRACKER_FILE = PROJECT_DIR / "uploaded_youtube.json"

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# YouTube category IDs
CATEGORY_ENTERTAINMENT = "24"
CATEGORY_TRAVEL = "19"
CATEGORY_EDUCATION = "27"

# Shorts must be <= 60 seconds and vertical (9:16) ideally
# But horizontal works too — YouTube auto-detects Shorts by duration + #Shorts tag

UPLOAD_DELAY = 15  # seconds between uploads
MAX_RETRIES = 3

# Reuse landmark data from TikTok uploader
try:
    from upload_tiktok import LANDMARKS, _extract_landmark_id
except ImportError:
    LANDMARKS = {}
    def _extract_landmark_id(stem: str) -> tuple[str, bool]:
        for suffix in ("_travel_a", "_travel_b", "_stock_a", "_stock_b"):
            if stem.endswith(suffix):
                return stem[:-len(suffix)], "travel" in suffix
        return stem, False

# Phase 2+3 landmarks not in upload_tiktok.py
EXTRA_LANDMARKS = {
    "acropolis_athens": {"name": "Acropolis of Athens", "location": "Athens", "tags": ["acropolis", "athens", "greece"]},
    "amalfi_coast": {"name": "Amalfi Coast", "location": "Italy", "tags": ["amalficoast", "italy", "travel"]},
    "amsterdam_canals": {"name": "Amsterdam Canals", "location": "Amsterdam", "tags": ["amsterdam", "canals", "netherlands"]},
    "antelope_canyon": {"name": "Antelope Canyon", "location": "Arizona", "tags": ["antelopecanyon", "arizona", "nature"]},
    "bagan_temples": {"name": "Bagan Temples", "location": "Myanmar", "tags": ["bagan", "myanmar", "temples"]},
    "blue_mosque": {"name": "Blue Mosque", "location": "Istanbul", "tags": ["bluemosque", "istanbul", "turkey"]},
    "bora_bora": {"name": "Bora Bora", "location": "French Polynesia", "tags": ["borabora", "paradise", "travel"]},
    "borobudur": {"name": "Borobudur Temple", "location": "Java", "tags": ["borobudur", "indonesia", "temple"]},
    "bruges_medieval": {"name": "Bruges", "location": "Belgium", "tags": ["bruges", "belgium", "medieval"]},
    "burj_khalifa": {"name": "Burj Khalifa", "location": "Dubai", "tags": ["burjkhalifa", "dubai", "skyscraper"]},
    "cappadocia": {"name": "Cappadocia", "location": "Turkey", "tags": ["cappadocia", "turkey", "balloons"]},
    "charles_bridge": {"name": "Charles Bridge", "location": "Prague", "tags": ["charlesbridge", "prague", "czechia"]},
    "duomo_florence": {"name": "Florence Cathedral", "location": "Florence", "tags": ["duomo", "florence", "italy"]},
    "easter_island": {"name": "Easter Island", "location": "Chile", "tags": ["easterisland", "moai", "chile"]},
    "edinburgh_old_town": {"name": "Edinburgh Old Town", "location": "Scotland", "tags": ["edinburgh", "scotland", "oldtown"]},
    "fushimi_inari": {"name": "Fushimi Inari Shrine", "location": "Kyoto", "tags": ["fushimiinari", "kyoto", "japan"]},
    "golden_temple_amritsar": {"name": "Golden Temple", "location": "Amritsar", "tags": ["goldentemple", "amritsar", "india"]},
    "gyeongbokgung": {"name": "Gyeongbokgung Palace", "location": "Seoul", "tags": ["gyeongbokgung", "seoul", "korea"]},
    "hoi_an": {"name": "Hoi An Ancient Town", "location": "Vietnam", "tags": ["hoian", "vietnam", "lanterns"]},
    "iguazu_falls": {"name": "Iguazu Falls", "location": "Argentina/Brazil", "tags": ["iguazufalls", "waterfall", "nature"]},
    "matterhorn": {"name": "Matterhorn", "location": "Switzerland", "tags": ["matterhorn", "switzerland", "alps"]},
    "meteora": {"name": "Meteora", "location": "Greece", "tags": ["meteora", "greece", "monasteries"]},
    "mont_saint_michel": {"name": "Mont Saint-Michel", "location": "France", "tags": ["montsaintmichel", "france", "island"]},
    "monument_valley": {"name": "Monument Valley", "location": "Arizona/Utah", "tags": ["monumentvalley", "arizona", "desert"]},
    "niagara_falls": {"name": "Niagara Falls", "location": "US/Canada", "tags": ["niagarafalls", "waterfall", "nature"]},
    "northern_lights_iceland": {"name": "Northern Lights", "location": "Iceland", "tags": ["northernlights", "iceland", "aurora"]},
    "nyhavn": {"name": "Nyhavn", "location": "Copenhagen", "tags": ["nyhavn", "copenhagen", "denmark"]},
    "petronas_towers": {"name": "Petronas Towers", "location": "Kuala Lumpur", "tags": ["petronastowers", "malaysia", "skyline"]},
    "plitvice_lakes": {"name": "Plitvice Lakes", "location": "Croatia", "tags": ["plitvicelakes", "croatia", "nature"]},
    "rothenburg": {"name": "Rothenburg ob der Tauber", "location": "Germany", "tags": ["rothenburg", "germany", "medieval"]},
    "seville_alcazar": {"name": "Royal Alcazar of Seville", "location": "Seville", "tags": ["alcazar", "seville", "spain"]},
    "sugarloaf_rio": {"name": "Sugarloaf Mountain", "location": "Rio de Janeiro", "tags": ["sugarloaf", "rio", "brazil"]},
    "sydney_opera": {"name": "Sydney Opera House", "location": "Sydney", "tags": ["sydneyopera", "australia", "sydney"]},
    "table_mountain": {"name": "Table Mountain", "location": "Cape Town", "tags": ["tablemountain", "capetown", "southafrica"]},
    "tikal": {"name": "Tikal", "location": "Guatemala", "tags": ["tikal", "guatemala", "maya"]},
    "tower_of_london": {"name": "Tower of London", "location": "London", "tags": ["toweroflondon", "london", "castle"]},
    "trolltunga": {"name": "Trolltunga", "location": "Norway", "tags": ["trolltunga", "norway", "cliff"]},
    "uluru": {"name": "Uluru", "location": "Australia", "tags": ["uluru", "australia", "outback"]},
    "victoria_falls": {"name": "Victoria Falls", "location": "Zambia/Zimbabwe", "tags": ["victoriafalls", "waterfall", "africa"]},
    "wadi_rum": {"name": "Wadi Rum", "location": "Jordan", "tags": ["wadirum", "jordan", "desert"]},
    "yellowstone": {"name": "Yellowstone", "location": "Wyoming", "tags": ["yellowstone", "nationalpark", "nature"]},
    "zhangjiajie": {"name": "Zhangjiajie", "location": "China", "tags": ["zhangjiajie", "china", "avatar"]},
}


# ---------------------------------------------------------------------------
# Caption builder
# ---------------------------------------------------------------------------

COMMON_TAGS = ["fineart", "artprint", "homedecor", "wallart", "moderndesignconcept", "shorts"]
TRAVEL_TAGS = ["travelfacts", "history", "didyouknow", "worldwonders", "moderndesignconcept", "shorts"]


def build_youtube_metadata(landmark_id: str, *, is_travel: bool = False) -> dict:
    """Build YouTube title, description, and tags for a video."""
    info = LANDMARKS.get(landmark_id) or EXTRA_LANDMARKS.get(landmark_id, {})
    name = info.get("name", landmark_id.replace("_", " ").title())
    location = info.get("location", "")
    specific_tags = info.get("tags", [])

    if is_travel:
        title = f"Incredible facts about {name}"
        if location:
            title += f" | {location}"
        description = (
            f"Incredible facts about the {name}"
            f"{f' in {location}' if location else ''}.\n\n"
            f"More art and travel content at moderndesignconcept.com\n\n"
            f"#Shorts #travel #history #landmarks #didyouknow"
        )
        tags = specific_tags + TRAVEL_TAGS
        category = CATEGORY_TRAVEL
    else:
        title = f"{name} reimagined as fine art"
        if location:
            title += f" | {location}"
        description = (
            f"{name} reimagined through classic art styles using neural style transfer.\n\n"
            f"Shop prints, posters & tees: https://moderndesignconcept.com\n\n"
            f"#Shorts #fineart #artprint #wallart #homedecor"
        )
        tags = specific_tags + COMMON_TAGS
        category = CATEGORY_ENTERTAINMENT

    # YouTube title max 100 chars
    title = title[:100]

    return {
        "title": title,
        "description": description,
        "tags": tags[:15],
        "category": category,
    }


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def run_auth_flow() -> None:
    """Run OAuth 2.0 authorization flow."""
    if not CLIENT_SECRETS_FILE.exists():
        print(f"Error: {CLIENT_SECRETS_FILE} not found.")
        print(f"\nTo create it:")
        print(f"  1. Go to https://console.cloud.google.com/apis/credentials")
        print(f"  2. Create OAuth 2.0 Client ID (Desktop app)")
        print(f"  3. Download JSON and save as {CLIENT_SECRETS_FILE}")
        return

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CLIENT_SECRETS_FILE), SCOPES
    )
    credentials = flow.run_local_server(port=8090, open_browser=True)

    # Save token
    token_data = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
        "saved_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)

    print(f"\nAuthorization successful! Token saved to {TOKEN_FILE.name}")


def get_youtube_service():
    """Build authenticated YouTube API service."""
    if not TOKEN_FILE.exists():
        print("No token found. Run: python3 upload_youtube.py --auth")
        sys.exit(1)

    with open(TOKEN_FILE) as f:
        token_data = json.load(f)

    credentials = Credentials(
        token=token_data["token"],
        refresh_token=token_data["refresh_token"],
        token_uri=token_data["token_uri"],
        client_id=token_data["client_id"],
        client_secret=token_data["client_secret"],
    )

    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


# ---------------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------------

def upload_single(youtube, video_path: Path, metadata: dict) -> str:
    """Upload a single video to YouTube. Returns video ID."""
    body = {
        "snippet": {
            "title": metadata["title"],
            "description": metadata["description"],
            "tags": metadata["tags"],
            "categoryId": metadata["category"],
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(
        str(video_path),
        mimetype="video/mp4",
        resumable=True,
        chunksize=1024 * 1024 * 10,  # 10MB chunks
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    # Resumable upload with retry
    response = None
    retry = 0
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                pct = int(status.progress() * 100)
                print(f"  Uploading... {pct}%")
        except HttpError as e:
            if e.resp.status in [500, 502, 503, 504]:
                retry += 1
                if retry > MAX_RETRIES:
                    raise
                wait = random.uniform(1, 2 ** retry)
                print(f"  Retrying in {wait:.0f}s (attempt {retry}/{MAX_RETRIES})")
                time.sleep(wait)
            else:
                raise

    video_id = response["id"]
    return video_id


# ---------------------------------------------------------------------------
# Tracker
# ---------------------------------------------------------------------------

def load_tracker() -> dict:
    if TRACKER_FILE.exists():
        with open(TRACKER_FILE) as f:
            return json.load(f)
    return {}


def save_tracker(tracker: dict) -> None:
    with open(TRACKER_FILE, "w") as f:
        json.dump(tracker, f, indent=2)


def record(tracker: dict, key: str, status: str, video_id: str = "", error: str = "") -> None:
    tracker[key] = {
        "status": status,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
    }
    if video_id:
        tracker[key]["video_id"] = video_id
    if error:
        tracker[key]["error"] = error
    save_tracker(tracker)


# ---------------------------------------------------------------------------
# Video discovery
# ---------------------------------------------------------------------------

def discover_videos(source_dirs: list[Path]) -> list[tuple[Path, str, bool]]:
    """Find all MP4 videos across source directories."""
    videos = []
    for d in source_dirs:
        if not d.is_dir():
            continue
        for mp4 in sorted(d.glob("*.mp4")):
            landmark_id, is_travel = _extract_landmark_id(mp4.stem)
            videos.append((mp4, landmark_id, is_travel))
    return videos


# ---------------------------------------------------------------------------
# Main upload loop
# ---------------------------------------------------------------------------

def run_upload(args: argparse.Namespace) -> None:
    """Main upload flow."""
    youtube = get_youtube_service()

    source_dirs = [
        PROJECT_DIR / "output" / "videos",
        PROJECT_DIR / "output" / "videos_travel",
        PROJECT_DIR / "output" / "videos_stock",
    ]
    if args.source_dir:
        source_dirs = [Path(args.source_dir)]

    all_videos = discover_videos(source_dirs)
    print(f"Found {len(all_videos)} total videos\n")

    tracker = load_tracker()
    to_upload = []
    for video_path, landmark_id, is_travel in all_videos:
        key = f"youtube/{video_path.stem}"
        entry = tracker.get(key, {})
        status = entry.get("status")

        if args.retry_failed and status == "failed":
            to_upload.append((video_path, landmark_id, is_travel, key))
        elif status == "success":
            continue
        elif not args.retry_failed:
            to_upload.append((video_path, landmark_id, is_travel, key))

    if not to_upload:
        print("Nothing to upload.")
        return

    limit = args.limit if args.limit and args.limit > 0 else len(to_upload)
    to_upload = to_upload[:limit]

    print(f"Will {'preview' if args.dry_run else 'upload'} {len(to_upload)} videos\n")

    if args.dry_run:
        for i, (vp, lid, it, key) in enumerate(to_upload, 1):
            meta = build_youtube_metadata(lid, is_travel=it)
            print(f"  [{i}] {key}")
            print(f"       Title: {meta['title']}")
            print(f"       Tags: {', '.join(meta['tags'][:8])}...")
            print()
        return

    uploaded = 0
    failed = 0

    for i, (video_path, landmark_id, is_travel, key) in enumerate(to_upload, 1):
        metadata = build_youtube_metadata(landmark_id, is_travel=is_travel)
        vtype = "travel" if is_travel else "promo"
        print(f"[{i}/{len(to_upload)}] {video_path.name} ({vtype})")
        print(f"  Title: {metadata['title']}")

        try:
            video_id = upload_single(youtube, video_path, metadata)
            record(tracker, key, "success", video_id=video_id)
            uploaded += 1
            print(f"  -> Success! https://youtube.com/shorts/{video_id}")
        except HttpError as e:
            error_msg = str(e)
            record(tracker, key, "failed", error=error_msg)
            failed += 1
            print(f"  -> Failed: {error_msg[:100]}")

            # Check for quota exceeded
            if e.resp.status == 403 and "quotaExceeded" in error_msg:
                print(f"\n=== YouTube daily quota exceeded — stopping ===")
                break
        except Exception as e:
            record(tracker, key, "failed", error=str(e))
            failed += 1
            print(f"  -> Failed: {e}")

        if i < len(to_upload):
            print(f"  Waiting {UPLOAD_DELAY}s...")
            time.sleep(UPLOAD_DELAY)

    print(f"\n=== YouTube upload complete ===")
    print(f"  Uploaded: {uploaded}/{len(to_upload)}")
    if failed:
        print(f"  Failed: {failed}")


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

def show_status() -> None:
    """Show upload stats."""
    tracker = load_tracker()
    yt_entries = {k: v for k, v in tracker.items() if k.startswith("youtube/")}
    success = sum(1 for v in yt_entries.values() if v.get("status") == "success")
    failed = sum(1 for v in yt_entries.values() if v.get("status") == "failed")
    print(f"\nYouTube upload stats:")
    print(f"  Total tracked: {len(yt_entries)}")
    print(f"  Success: {success}")
    print(f"  Failed: {failed}")

    if TOKEN_FILE.exists():
        with open(TOKEN_FILE) as f:
            token = json.load(f)
        print(f"\nToken saved: {token.get('saved_at', 'N/A')}")
    else:
        print(f"\nNo token found. Run --auth first.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    global UPLOAD_DELAY

    parser = argparse.ArgumentParser(
        description="YouTube Shorts uploader via Data API v3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--auth", action="store_true", help="Run OAuth authorization")
    parser.add_argument("--upload", action="store_true", help="Upload videos")
    parser.add_argument("--status", action="store_true", help="Show upload stats")
    parser.add_argument("--source-dir", type=str, help="Video source directory")
    parser.add_argument("--limit", type=int, default=0, help="Max videos to upload")
    parser.add_argument("--delay", type=float, default=UPLOAD_DELAY, help="Seconds between uploads")
    parser.add_argument("--dry-run", action="store_true", help="Preview without uploading")
    parser.add_argument("--retry-failed", action="store_true", help="Retry failed uploads")

    args = parser.parse_args()

    if args.auth:
        run_auth_flow()
    elif args.upload:
        UPLOAD_DELAY = args.delay
        run_upload(args)
    elif args.status:
        show_status()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
