#!/usr/bin/env python3
"""TikTok Content Posting API uploader.

Uses the official TikTok API (no browser automation) to upload videos.
Requires an approved developer app and OAuth access token.

Setup:
    1. Run: python3 tiktok_api.py --auth   (one-time OAuth flow)
    2. Run: python3 tiktok_api.py --upload --source-dir output/videos --limit 5

Usage:
    python3 tiktok_api.py --auth                          # Get access token
    python3 tiktok_api.py --upload --limit 5              # Upload 5 videos
    python3 tiktok_api.py --upload --dry-run --limit 10   # Preview
    python3 tiktok_api.py --upload --retry-failed         # Retry failures
    python3 tiktok_api.py --status                        # Check token & stats
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_DIR = Path(__file__).parent
TOKEN_FILE = PROJECT_DIR / ".tiktok_token.json"
TRACKER_FILE = PROJECT_DIR / "uploaded_tiktok.json"

TIKTOK_AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/"
TIKTOK_TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
TIKTOK_CREATOR_INFO_URL = "https://open.tiktokapis.com/v2/post/publish/creator_info/query/"
TIKTOK_VIDEO_INIT_URL = "https://open.tiktokapis.com/v2/post/publish/video/init/"
TIKTOK_STATUS_URL = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"

SCOPES = "user.info.basic,video.publish,video.upload"
REDIRECT_URI = "https://moderndesignconcept.com/auth/tiktok/callback"

# Rate limit: 6 requests/min per user
UPLOAD_DELAY = 12  # seconds between uploads (safe margin)


# ---------------------------------------------------------------------------
# Keychain helpers
# ---------------------------------------------------------------------------

def _keychain_get(account: str) -> str:
    """Read a password from macOS Keychain."""
    result = subprocess.run(
        ["security", "find-generic-password", "-a", account,
         "-s", "com.moderndesignconcept", "-w"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Keychain lookup failed for {account}: {result.stderr.strip()}")
    return result.stdout.strip()


def get_client_key() -> str:
    return _keychain_get("tiktok_client_key")


def get_client_secret() -> str:
    return _keychain_get("tiktok_client_secret")


# ---------------------------------------------------------------------------
# Token management
# ---------------------------------------------------------------------------

def load_token() -> dict | None:
    """Load saved token from disk."""
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE) as f:
            return json.load(f)
    return None


def save_token(token_data: dict) -> None:
    """Save token to disk."""
    token_data["saved_at"] = datetime.now(timezone.utc).isoformat()
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)
    print(f"  Token saved to {TOKEN_FILE.name}")


def is_token_valid(token: dict) -> bool:
    """Check if access token is still valid."""
    saved_at = token.get("saved_at", "")
    expires_in = token.get("expires_in", 0)
    if not saved_at or not expires_in:
        return False
    from datetime import datetime, timezone
    saved = datetime.fromisoformat(saved_at)
    elapsed = (datetime.now(timezone.utc) - saved).total_seconds()
    return elapsed < expires_in - 300  # 5 min buffer


def refresh_access_token(token: dict) -> dict:
    """Refresh the access token using refresh_token."""
    client_key = get_client_key()
    client_secret = get_client_secret()
    refresh_token = token.get("refresh_token")
    if not refresh_token:
        raise RuntimeError("No refresh token available. Re-run --auth.")

    data = urllib.parse.urlencode({
        "client_key": client_key,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }).encode()

    req = urllib.request.Request(TIKTOK_TOKEN_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    if "access_token" not in result:
        raise RuntimeError(f"Token refresh failed: {result}")

    save_token(result)
    print("  Access token refreshed!")
    return result


def get_valid_token() -> dict:
    """Get a valid access token, refreshing if needed."""
    token = load_token()
    if not token:
        print("No token found. Run: python3 tiktok_api.py --auth")
        sys.exit(1)

    if not is_token_valid(token):
        print("  Token expired, refreshing...")
        token = refresh_access_token(token)

    return token


# ---------------------------------------------------------------------------
# OAuth flow
# ---------------------------------------------------------------------------

def run_auth_flow() -> None:
    """Run the OAuth authorization flow."""
    client_key = get_client_key()

    # Build authorization URL
    params = urllib.parse.urlencode({
        "client_key": client_key,
        "response_type": "code",
        "scope": SCOPES,
        "redirect_uri": REDIRECT_URI,
        "state": "tiktok_auth",
    })
    auth_url = f"{TIKTOK_AUTH_URL}?{params}"

    print("\n=== TikTok OAuth Authorization ===")
    print(f"\n1. Open this URL in your browser:\n")
    print(f"   {auth_url}\n")
    print("2. Authorize the app")
    print("3. You'll be redirected — copy the 'code' parameter from the URL")
    print("   (It will be in the address bar even if the page doesn't load)\n")

    code = input("Paste the authorization code here: ").strip()
    if not code:
        print("No code provided. Aborting.")
        return

    # Exchange code for access token
    client_secret = get_client_secret()
    data = urllib.parse.urlencode({
        "client_key": client_key,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }).encode()

    req = urllib.request.Request(TIKTOK_TOKEN_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    if "access_token" not in result:
        print(f"Error: {result}")
        return

    save_token(result)
    print(f"\n  Access token obtained!")
    print(f"  Open ID: {result.get('open_id', 'N/A')}")
    print(f"  Expires in: {result.get('expires_in', 0) // 3600} hours")
    print(f"  Refresh token expires in: {result.get('refresh_expires_in', 0) // 86400} days")


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def api_request(url: str, token: str, body: dict | None = None) -> dict:
    """Make an authenticated API request."""
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json; charset=UTF-8")

    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def query_creator_info(token: str) -> dict:
    """Get creator info (privacy options, etc.)."""
    return api_request(TIKTOK_CREATOR_INFO_URL, token)


def check_publish_status(token: str, publish_id: str) -> dict:
    """Check the status of a published video."""
    return api_request(TIKTOK_STATUS_URL, token, {"publish_id": publish_id})


# ---------------------------------------------------------------------------
# Video upload
# ---------------------------------------------------------------------------

def upload_video_file(token: str, video_path: Path, caption: str,
                      privacy: str = "PUBLIC_TO_EVERYONE") -> str:
    """Upload a video file via the Content Posting API.

    Returns publish_id on success.
    """
    video_size = video_path.stat().st_size

    # Step 1: Initialize upload
    init_body = {
        "post_info": {
            "title": caption[:2200],
            "privacy_level": privacy,
            "disable_duet": False,
            "disable_stitch": False,
            "disable_comment": False,
            "is_aigc": True,  # Our content is AI-generated
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": video_size,
            "chunk_size": video_size,  # Single chunk for files under 64MB
            "total_chunk_count": 1,
        },
    }

    init_resp = api_request(TIKTOK_VIDEO_INIT_URL, token, init_body)

    if init_resp.get("error", {}).get("code") != "ok":
        error = init_resp.get("error", {})
        raise RuntimeError(f"Init failed: {error.get('code')} — {error.get('message')}")

    publish_id = init_resp["data"]["publish_id"]
    upload_url = init_resp["data"]["upload_url"]

    # Step 2: Upload video binary
    with open(video_path, "rb") as f:
        video_data = f.read()

    upload_req = urllib.request.Request(upload_url, data=video_data, method="PUT")
    upload_req.add_header("Content-Type", "video/mp4")
    upload_req.add_header("Content-Length", str(video_size))
    upload_req.add_header("Content-Range", f"bytes 0-{video_size - 1}/{video_size}")

    with urllib.request.urlopen(upload_req) as resp:
        if resp.status not in (200, 201):
            raise RuntimeError(f"Upload failed with status {resp.status}")

    print(f"  Video uploaded, publish_id: {publish_id}")

    # Step 3: Poll for publish status
    for attempt in range(6):
        time.sleep(5)
        status_resp = check_publish_status(token, publish_id)
        status = status_resp.get("data", {}).get("status")
        if status == "PUBLISH_COMPLETE":
            print(f"  Published successfully!")
            return publish_id
        elif status in ("FAILED", "PUBLISH_FAILED"):
            fail_reason = status_resp.get("data", {}).get("fail_reason", "unknown")
            raise RuntimeError(f"Publish failed: {fail_reason}")
        print(f"  Status: {status} (checking again...)")

    # If still processing after 30s, assume it's fine
    print(f"  Still processing — assuming success (publish_id: {publish_id})")
    return publish_id


# ---------------------------------------------------------------------------
# Caption builder (reuse from upload_tiktok.py)
# ---------------------------------------------------------------------------

# Import landmarks data
try:
    from upload_tiktok import LANDMARKS, COMMON_TAGS, TRAVEL_TAGS, build_caption, _extract_landmark_id
except ImportError:
    # Fallback if import fails
    LANDMARKS = {}
    COMMON_TAGS = ["fineart", "artprint", "homedecor", "wallart", "moderndesignconcept"]
    TRAVEL_TAGS = ["travelfacts", "history", "didyouknow", "travelhistory", "moderndesignconcept"]

    def _extract_landmark_id(stem: str) -> tuple[str, bool]:
        for suffix in ("_travel_a", "_travel_b", "_stock_a", "_stock_b"):
            if stem.endswith(suffix):
                return stem[:-len(suffix)], "travel" in suffix
        return stem, False

    def build_caption(landmark_id: str, *, is_travel: bool = False) -> str:
        name = landmark_id.replace("_", " ").title()
        if is_travel:
            return f"Incredible facts about {name}\nMore at moderndesignconcept.com\n#travel #history"
        return f"{name} reimagined as fine art 🎨\nShop: moderndesignconcept.com\n#fineart #artprint"


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


def record(tracker: dict, key: str, status: str, error: str = "") -> None:
    tracker[key] = {
        "status": status,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "method": "api",
    }
    if error:
        tracker[key]["error"] = error
    save_tracker(tracker)


# ---------------------------------------------------------------------------
# Upload loop
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


def run_upload(args: argparse.Namespace) -> None:
    """Main upload flow using TikTok API."""
    token_data = get_valid_token()
    access_token = token_data["access_token"]

    # Check creator info
    try:
        creator_info = query_creator_info(access_token)
        print(f"Creator info: {json.dumps(creator_info.get('data', {}), indent=2)[:200]}")
    except Exception as e:
        print(f"Warning: Could not query creator info: {e}")

    # Discover videos
    source_dirs = [
        PROJECT_DIR / "output" / "videos",
        PROJECT_DIR / "output" / "videos_travel",
        PROJECT_DIR / "output" / "videos_stock",
    ]
    if args.source_dir:
        source_dirs = [Path(args.source_dir)]

    all_videos = discover_videos(source_dirs)
    print(f"Found {len(all_videos)} total videos\n")

    # Filter by tracker
    tracker = load_tracker()
    to_upload = []
    for video_path, landmark_id, is_travel in all_videos:
        key = f"tiktok_api/{video_path.stem}"
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
            caption = build_caption(lid, is_travel=it)
            print(f"  [{i}] {key}")
            print(f"       File: {vp.name} ({vp.stat().st_size // 1024}KB)")
            print(f"       Caption: {caption[:80]}...")
            print()
        return

    # Determine privacy level
    privacy = "PUBLIC_TO_EVERYONE"
    if args.private:
        privacy = "SELF_ONLY"

    uploaded = 0
    failed = 0

    for i, (video_path, landmark_id, is_travel, key) in enumerate(to_upload, 1):
        caption = build_caption(landmark_id, is_travel=is_travel)
        vtype = "travel" if is_travel else "promo"
        print(f"[{i}/{len(to_upload)}] {video_path.name} ({vtype})")

        try:
            publish_id = upload_video_file(access_token, video_path, caption, privacy)
            record(tracker, key, "success")
            uploaded += 1
            print(f"  -> Success (publish_id: {publish_id})")
        except Exception as e:
            record(tracker, key, "failed", str(e))
            failed += 1
            print(f"  -> Failed: {e}")

        # Rate limit delay
        if i < len(to_upload):
            print(f"  Waiting {UPLOAD_DELAY}s...")
            time.sleep(UPLOAD_DELAY)

    print(f"\n=== Upload complete ===")
    print(f"  Uploaded: {uploaded}/{len(to_upload)}")
    if failed:
        print(f"  Failed: {failed}")


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

def show_status() -> None:
    """Show token and upload stats."""
    token = load_token()
    if token:
        print(f"\nToken status:")
        print(f"  Open ID: {token.get('open_id', 'N/A')}")
        print(f"  Valid: {is_token_valid(token)}")
        print(f"  Saved: {token.get('saved_at', 'N/A')}")
    else:
        print("\nNo token found. Run --auth first.")

    tracker = load_tracker()
    api_entries = {k: v for k, v in tracker.items() if k.startswith("tiktok_api/")}
    success = sum(1 for v in api_entries.values() if v.get("status") == "success")
    failed = sum(1 for v in api_entries.values() if v.get("status") == "failed")
    print(f"\nAPI upload stats:")
    print(f"  Total tracked: {len(api_entries)}")
    print(f"  Success: {success}")
    print(f"  Failed: {failed}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="TikTok Content Posting API uploader",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--auth", action="store_true", help="Run OAuth authorization flow")
    parser.add_argument("--upload", action="store_true", help="Upload videos")
    parser.add_argument("--status", action="store_true", help="Show token and upload stats")
    parser.add_argument("--source-dir", type=str, help="Video source directory")
    parser.add_argument("--limit", type=int, default=0, help="Max videos to upload")
    parser.add_argument("--delay", type=float, default=UPLOAD_DELAY, help="Seconds between uploads")
    parser.add_argument("--dry-run", action="store_true", help="Preview without uploading")
    parser.add_argument("--retry-failed", action="store_true", help="Retry failed uploads")
    parser.add_argument("--private", action="store_true",
                        help="Post as private (required for unaudited apps)")

    args = parser.parse_args()

    if args.auth:
        run_auth_flow()
    elif args.upload:
        global UPLOAD_DELAY
        UPLOAD_DELAY = args.delay
        run_upload(args)
    elif args.status:
        show_status()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
