#!/usr/bin/env python3
"""Monitor MDC email inbox via Microsoft Graph API and forward new emails to Telegram.

Polls the inbox every 2 minutes and sends a Telegram notification for each new email.

Setup:
    1. Register Azure AD app with Mail.Read Application permission
    2. Grant admin consent in Azure portal
    3. Add credentials to .email_monitor_config
    4. Run: python3 email_monitor.py --once  (to test)
    5. Enable launchd service for continuous monitoring

Usage:
    python3 email_monitor.py              # Run continuously
    python3 email_monitor.py --once       # Check once and exit
    python3 email_monitor.py --interval 60  # Poll every 60 seconds
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
STATE_FILE = SCRIPT_DIR / ".email_monitor_state"

from keychain_config import load_config as _load_keychain_config

DEFAULT_INTERVAL = 120  # 2 minutes
GRAPH_BASE = "https://graph.microsoft.com/v1.0"

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
log = logging.getLogger(__name__)


def load_telegram_config() -> dict:
    return _load_keychain_config("telegram")


def load_email_config() -> dict:
    return _load_keychain_config("email_monitor")


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state) + "\n")


def get_access_token(config: dict) -> str:
    """Get OAuth2 access token using client credentials flow."""
    url = f"https://login.microsoftonline.com/{config['tenant_id']}/oauth2/v2.0/token"
    resp = requests.post(url, data={
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials",
    }, timeout=15)

    if resp.status_code != 200:
        log.error(f"Token request failed: {resp.status_code} {resp.text}")
        raise RuntimeError("Failed to get access token")

    return resp.json()["access_token"]


def check_new_emails(token: str, user_email: str, last_check: str | None) -> list[dict]:
    """Fetch unread emails from inbox via Microsoft Graph API."""
    headers = {"Authorization": f"Bearer {token}"}

    # Get unread messages, newest first
    params = {
        "$filter": "isRead eq false",
        "$orderby": "receivedDateTime desc",
        "$top": "20",
        "$select": "id,subject,from,receivedDateTime,bodyPreview,isRead",
    }

    url = f"{GRAPH_BASE}/users/{user_email}/mailFolders/inbox/messages"
    resp = requests.get(url, headers=headers, params=params, timeout=15)

    if resp.status_code != 200:
        log.error(f"Graph API error: {resp.status_code} {resp.text}")
        return []

    messages = resp.json().get("value", [])
    if not messages:
        return []

    # Filter to only messages we haven't seen
    state = load_state()
    seen_ids = set(state.get("seen_ids", []))

    new_emails = []
    for msg in messages:
        msg_id = msg["id"]
        if msg_id in seen_ids:
            continue

        from_info = msg.get("from", {}).get("emailAddress", {})
        from_name = from_info.get("name", "")
        from_addr = from_info.get("address", "Unknown")
        from_display = f"{from_name} <{from_addr}>" if from_name else from_addr

        new_emails.append({
            "id": msg_id,
            "subject": msg.get("subject", "(No Subject)"),
            "from": from_display,
            "date": msg.get("receivedDateTime", ""),
            "preview": msg.get("bodyPreview", "")[:200],
        })

    return new_emails


def send_telegram_message(token: str, chat_id: int, text: str) -> bool:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        resp = requests.post(url, json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }, timeout=10)
        return resp.status_code == 200
    except Exception as e:
        log.error(f"Telegram send error: {e}")
        return False


def format_notification(email_info: dict) -> str:
    subject = email_info.get("subject", "(No Subject)")
    from_addr = email_info.get("from", "Unknown")
    preview = email_info.get("preview", "")[:200]
    date_str = email_info.get("date", "")

    # Format date if present
    date_display = ""
    if date_str:
        try:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            date_display = dt.strftime("%b %d, %I:%M %p")
        except Exception:
            date_display = date_str

    # Escape HTML special chars
    for old, new in [("&", "&amp;"), ("<", "&lt;"), (">", "&gt;")]:
        subject = subject.replace(old, new)
        from_addr = from_addr.replace(old, new)
        preview = preview.replace(old, new)

    msg = f"\U0001f4e7 <b>New Email</b>\n"
    msg += f"<b>From:</b> {from_addr}\n"
    msg += f"<b>Subject:</b> {subject}\n"
    if date_display:
        msg += f"<b>Date:</b> {date_display}\n"
    if preview:
        msg += f"\n{preview}"

    return msg


def run_check(email_config: dict, tg_token: str, chat_id: int) -> int:
    log.info("Checking for new emails...")

    try:
        access_token = get_access_token(email_config)
    except RuntimeError:
        return 0

    state = load_state()
    last_check = state.get("last_check")

    new_emails = check_new_emails(access_token, email_config["email"], last_check)

    if not new_emails:
        log.info("No new emails")
        state["last_check"] = datetime.now(timezone.utc).isoformat()
        save_state(state)
        return 0

    log.info(f"Found {len(new_emails)} new email(s)")
    seen_ids = set(state.get("seen_ids", []))
    sent = 0

    for em in new_emails:
        msg = format_notification(em)
        if send_telegram_message(tg_token, chat_id, msg):
            sent += 1
            seen_ids.add(em["id"])
            log.info(f"  Notified: {em['subject'][:60]}")
        time.sleep(1)

    # Keep only last 200 IDs
    recent = sorted(seen_ids)[-200:]
    state["seen_ids"] = recent
    state["last_check"] = datetime.now(timezone.utc).isoformat()
    save_state(state)
    return sent


def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor MDC email and notify via Telegram")
    parser.add_argument("--once", action="store_true", help="Check once and exit")
    parser.add_argument("--interval", type=int, default=DEFAULT_INTERVAL,
                        help=f"Poll interval in seconds (default: {DEFAULT_INTERVAL})")
    args = parser.parse_args()

    tg_config = load_telegram_config()
    tg_token = tg_config["token"]
    allowed = tg_config.get("allowed_user_ids", [])
    if not allowed:
        log.error("No allowed_user_ids in telegram config")
        sys.exit(1)
    chat_id = allowed[0]

    email_config = load_email_config()

    log.info(f"Email monitor started (interval={args.interval}s, account={email_config['email']})")
    log.info("Using Microsoft Graph API with OAuth2 client credentials")

    if args.once:
        count = run_check(email_config, tg_token, chat_id)
        log.info(f"Done — {count} notification(s) sent")
        return

    while True:
        try:
            run_check(email_config, tg_token, chat_id)
        except Exception as e:
            log.error(f"Check failed: {e}")
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
