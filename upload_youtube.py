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

from video_captions import (
    extract_video_info,
    build_youtube_metadata,
)


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

def discover_videos(source_dirs: list[Path]) -> list[tuple[Path, str, str]]:
    """Find all MP4 videos across source directories."""
    videos = []
    for d in source_dirs:
        if not d.is_dir():
            continue
        for mp4 in sorted(d.glob("*.mp4")):
            landmark_id, video_type = extract_video_info(mp4.stem)
            videos.append((mp4, landmark_id, video_type))
    return videos


# ---------------------------------------------------------------------------
# Main upload loop
# ---------------------------------------------------------------------------

def run_upload(args: argparse.Namespace) -> None:
    """Main upload flow."""
    youtube = get_youtube_service()

    source_dirs = [
        PROJECT_DIR / "output" / "videos_music",
        PROJECT_DIR / "output" / "videos_travel_music",
        PROJECT_DIR / "output" / "videos_stock_music",
    ]
    if args.source_dir:
        source_dirs = [Path(args.source_dir)]

    all_videos = discover_videos(source_dirs)
    print(f"Found {len(all_videos)} total videos\n")

    tracker = load_tracker()
    to_upload = []
    for video_path, landmark_id, video_type in all_videos:
        key = f"youtube/{video_path.stem}"
        entry = tracker.get(key, {})
        status = entry.get("status")

        if args.retry_failed and status == "failed":
            to_upload.append((video_path, landmark_id, video_type, key))
        elif status == "success":
            continue
        elif not args.retry_failed:
            to_upload.append((video_path, landmark_id, video_type, key))

    if not to_upload:
        print("Nothing to upload.")
        return

    limit = args.limit if args.limit and args.limit > 0 else len(to_upload)
    to_upload = to_upload[:limit]

    print(f"Will {'preview' if args.dry_run else 'upload'} {len(to_upload)} videos\n")

    if args.dry_run:
        for i, (vp, lid, vt, key) in enumerate(to_upload, 1):
            meta = build_youtube_metadata(lid, video_type=vt)
            print(f"  [{i}] {key}")
            print(f"       Title: {meta['title']}")
            print(f"       Tags: {', '.join(meta['tags'][:8])}...")
            print()
        return

    uploaded = 0
    failed = 0

    for i, (video_path, landmark_id, video_type, key) in enumerate(to_upload, 1):
        metadata = build_youtube_metadata(landmark_id, video_type=video_type)
        print(f"[{i}/{len(to_upload)}] {video_path.name} ({video_type})")
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
