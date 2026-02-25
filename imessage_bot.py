#!/usr/bin/env python3
"""
iMessage Bot powered by Claude API.

Polls the macOS Messages database for new incoming messages from a specific
contact and replies using the Anthropic Claude API via iMessage (AppleScript).

Setup:
    1. Grant Full Disk Access to your terminal app:
       System Settings > Privacy & Security > Full Disk Access > [your terminal]
    2. Install the Anthropic SDK:
       pip install anthropic
    3. Set your API key (pick one):
       - Environment variable: export ANTHROPIC_API_KEY="sk-ant-..."
       - CLI flag: python3 imessage_bot.py --api-key "sk-ant-..."
       - Config file: stored automatically in .imessage_bot_config
    4. Start the bot with a contact:
       python3 imessage_bot.py --contact "+15551234567"
    5. Send an iMessage to yourself from the target contact's device, or
       have the contact message you. The bot replies automatically.

CLI Usage:
    python3 imessage_bot.py                         # start (prompts if needed)
    python3 imessage_bot.py --contact "+15551234567" # set contact
    python3 imessage_bot.py --api-key "sk-ant-..."   # set API key
    python3 imessage_bot.py --model "claude-haiku-4-5-20251001"  # cheaper model
    python3 imessage_bot.py --test                   # send test message and exit

Dependencies:
    pip install anthropic
"""

import argparse
import json
import os
import pathlib
import sqlite3
import subprocess
import sys
import textwrap
import time
from datetime import datetime

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / ".imessage_bot_config"
MESSAGES_DB = pathlib.Path.home() / "Library" / "Messages" / "chat.db"
POLL_INTERVAL_SECONDS = 2
MAX_HISTORY_TURNS = 20
MAX_BUBBLE_CHARS = 1500
DEFAULT_MODEL = "claude-sonnet-4-20250514"

SYSTEM_PROMPT = (
    "You are a helpful assistant communicating via iMessage. "
    "Keep your responses concise and conversational. "
    "Do NOT use markdown formatting (no **, ##, ```, bullet points, etc.) -- "
    "plain text only, since this is a text message conversation. "
    "Use short paragraphs. Be friendly but direct."
)

# ---------------------------------------------------------------------------
# Logging helper
# ---------------------------------------------------------------------------

def log(message: str) -> None:
    """Print a timestamped log line to the terminal."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


# ---------------------------------------------------------------------------
# Config management
# ---------------------------------------------------------------------------

def load_config() -> dict:
    """Load bot config from the JSON config file."""
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except (json.JSONDecodeError, OSError) as exc:
            log(f"Warning: could not read config ({exc}), starting fresh")
    return {}


def save_config(config: dict) -> None:
    """Persist bot config to the JSON config file."""
    CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n")
    # Restrict permissions -- file contains an API key
    CONFIG_PATH.chmod(0o600)
    log(f"Config saved to {CONFIG_PATH}")


def resolve_api_key(args_key: str | None, config: dict) -> str | None:
    """Return the API key from CLI > env var > config, in priority order."""
    if args_key:
        return args_key
    env_key = os.environ.get("ANTHROPIC_API_KEY")
    if env_key:
        return env_key
    return config.get("api_key")


# ---------------------------------------------------------------------------
# Messages database helpers
# ---------------------------------------------------------------------------

def check_db_access() -> bool:
    """Verify the Messages database exists and is readable."""
    if not MESSAGES_DB.exists():
        log(f"ERROR: Messages database not found at {MESSAGES_DB}")
        return False
    try:
        conn = sqlite3.connect(f"file:{MESSAGES_DB}?mode=ro", uri=True)
        conn.execute("SELECT 1 FROM message LIMIT 1")
        conn.close()
        return True
    except sqlite3.OperationalError as exc:
        log(f"ERROR: Cannot read Messages database: {exc}")
        log(
            "You likely need to grant Full Disk Access to your terminal app.\n"
            "  -> System Settings > Privacy & Security > Full Disk Access\n"
            "  -> Toggle ON for Terminal / iTerm / your terminal emulator\n"
            "Then restart your terminal and try again."
        )
        return False


def get_max_rowid() -> int:
    """Return the current maximum ROWID in the message table."""
    conn = sqlite3.connect(f"file:{MESSAGES_DB}?mode=ro", uri=True)
    cursor = conn.execute("SELECT MAX(ROWID) FROM message")
    row = cursor.fetchone()
    conn.close()
    return row[0] or 0


def fetch_new_messages(contact: str, since_rowid: int) -> list[tuple[int, str]]:
    """
    Fetch new incoming messages from *contact* with ROWID > since_rowid.

    Returns a list of (rowid, message_text) tuples sorted by ROWID ascending.
    Only returns messages where is_from_me = 0 (incoming).
    """
    conn = sqlite3.connect(f"file:{MESSAGES_DB}?mode=ro", uri=True)
    query = """
        SELECT m.ROWID, m.text
        FROM message m
        JOIN chat_message_join cmj ON cmj.message_id = m.ROWID
        JOIN chat c ON c.ROWID = cmj.chat_id
        WHERE m.ROWID > ?
          AND m.is_from_me = 0
          AND m.text IS NOT NULL
          AND m.text != ''
          AND (
              c.chat_identifier = ?
              OR c.chat_identifier LIKE '%' || ? || '%'
          )
        ORDER BY m.ROWID ASC
    """
    cursor = conn.execute(query, (since_rowid, contact, contact))
    results = cursor.fetchall()
    conn.close()
    return results


# ---------------------------------------------------------------------------
# iMessage sending via AppleScript
# ---------------------------------------------------------------------------

def send_imessage(contact: str, text: str) -> bool:
    """
    Send an iMessage to *contact* using AppleScript.

    Tries three strategies in order:
      1. iMessage service
      2. SMS service
      3. Generic send (no service specified)

    Returns True if any strategy succeeded.
    """
    # Escape backslashes and double-quotes for AppleScript string literals
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')

    strategies = [
        # Strategy 1: explicit iMessage service
        f'''
        tell application "Messages"
            set targetService to 1st service whose service type = iMessage
            set targetBuddy to buddy "{contact}" of targetService
            send "{escaped}" to targetBuddy
        end tell
        ''',
        # Strategy 2: explicit SMS service
        f'''
        tell application "Messages"
            set targetService to 1st service whose service type = SMS
            set targetBuddy to buddy "{contact}" of targetService
            send "{escaped}" to targetBuddy
        end tell
        ''',
        # Strategy 3: generic — let Messages.app figure it out
        f'''
        tell application "Messages"
            set targetBuddy to a reference to buddy "{contact}" of (1st account whose service type = iMessage)
            send "{escaped}" to targetBuddy
        end tell
        ''',
    ]

    for i, script in enumerate(strategies, start=1):
        try:
            subprocess.run(
                ["osascript", "-e", script.strip()],
                capture_output=True,
                text=True,
                timeout=15,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            log(f"  AppleScript strategy {i}/3 failed: {exc}")

    log("ERROR: All AppleScript send strategies failed.")
    return False


def send_long_message(contact: str, text: str) -> bool:
    """
    Send a potentially long message, splitting it into multiple iMessage
    bubbles of roughly MAX_BUBBLE_CHARS each.

    Splits on paragraph boundaries when possible, otherwise hard-wraps.
    Returns True if all parts sent successfully.
    """
    if len(text) <= MAX_BUBBLE_CHARS:
        return send_imessage(contact, text)

    # Split on double-newlines (paragraphs) first
    paragraphs = text.split("\n\n")
    chunks: list[str] = []
    current_chunk = ""

    for para in paragraphs:
        candidate = f"{current_chunk}\n\n{para}".strip() if current_chunk else para
        if len(candidate) <= MAX_BUBBLE_CHARS:
            current_chunk = candidate
        else:
            if current_chunk:
                chunks.append(current_chunk)
            # If a single paragraph exceeds the limit, hard-wrap it
            if len(para) > MAX_BUBBLE_CHARS:
                wrapped = textwrap.wrap(para, width=MAX_BUBBLE_CHARS)
                chunks.extend(wrapped)
                current_chunk = ""
            else:
                current_chunk = para

    if current_chunk:
        chunks.append(current_chunk)

    all_ok = True
    for idx, chunk in enumerate(chunks, start=1):
        log(f"  Sending part {idx}/{len(chunks)} ({len(chunk)} chars)")
        if not send_imessage(contact, chunk):
            all_ok = False
        if idx < len(chunks):
            time.sleep(0.5)  # small gap between bubbles
    return all_ok


# ---------------------------------------------------------------------------
# Claude API interaction
# ---------------------------------------------------------------------------

def get_claude_response(
    api_key: str,
    model: str,
    conversation_history: list[dict],
    user_message: str,
) -> str:
    """
    Send the conversation to the Anthropic API and return the assistant reply.

    Appends the user_message to conversation_history in-place, then trims
    to MAX_HISTORY_TURNS (most recent messages kept).
    """
    try:
        import anthropic
    except ImportError:
        return (
            "[Bot error] The 'anthropic' package is not installed. "
            "Run: pip install anthropic"
        )

    # Append user turn
    conversation_history.append({"role": "user", "content": user_message})

    # Trim to last N turns
    if len(conversation_history) > MAX_HISTORY_TURNS:
        conversation_history[:] = conversation_history[-MAX_HISTORY_TURNS:]

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=conversation_history,
        )
        assistant_text = response.content[0].text

        # Append assistant turn
        conversation_history.append({"role": "assistant", "content": assistant_text})

        # Trim again after assistant turn
        if len(conversation_history) > MAX_HISTORY_TURNS:
            conversation_history[:] = conversation_history[-MAX_HISTORY_TURNS:]

        return assistant_text

    except Exception as exc:
        error_msg = f"[Bot error] Claude API error: {exc}"
        log(error_msg)
        return error_msg


# ---------------------------------------------------------------------------
# Test mode
# ---------------------------------------------------------------------------

def run_test(contact: str) -> None:
    """Send a single test message and exit."""
    test_text = "Hello! This is a test message from the iMessage bot."
    log(f"Sending test message to {contact}...")
    if send_long_message(contact, test_text):
        log("Test message sent successfully.")
    else:
        log("Test message FAILED. Check AppleScript permissions.")
    sys.exit(0)


# ---------------------------------------------------------------------------
# Main polling loop
# ---------------------------------------------------------------------------

def run_bot(api_key: str, contact: str, model: str) -> None:
    """Main loop: poll for new messages, call Claude, reply via iMessage."""
    if not check_db_access():
        sys.exit(1)

    # Capture current max ROWID so we only process messages arriving *after*
    # the bot starts.
    last_rowid = get_max_rowid()
    log(f"Starting ROWID baseline: {last_rowid}")
    log(f"Bot is running. Watching for messages from: {contact}")
    log(f"Model: {model}")
    log(f"Polling every {POLL_INTERVAL_SECONDS}s. Press Ctrl+C to stop.\n")

    conversation_history: list[dict] = []

    try:
        while True:
            new_messages = fetch_new_messages(contact, last_rowid)

            for rowid, text in new_messages:
                last_rowid = rowid
                log(f"RECEIVED (ROWID {rowid}): {text}")

                # Get Claude's reply
                reply = get_claude_response(api_key, model, conversation_history, text)
                log(f"REPLY: {reply}")

                # Send reply back via iMessage
                if send_long_message(contact, reply):
                    log("  -> Sent OK")
                else:
                    log("  -> SEND FAILED")

            time.sleep(POLL_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        log("\nShutting down gracefully. Goodbye!")
        sys.exit(0)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="iMessage bot powered by Claude API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python3 imessage_bot.py --contact "+15551234567"
              python3 imessage_bot.py --api-key "sk-ant-..." --model "claude-haiku-4-5-20251001"
              python3 imessage_bot.py --test
        """),
    )
    parser.add_argument(
        "--contact",
        help="Phone number (e.g. +15551234567) or email of the contact to watch",
    )
    parser.add_argument(
        "--api-key",
        help="Anthropic API key (overrides env var and config file)",
    )
    parser.add_argument(
        "--model",
        help=f"Claude model to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Send a test message to the contact and exit",
    )
    args = parser.parse_args()

    # ---- Load / update config ----
    config = load_config()
    dirty = False

    if args.api_key:
        config["api_key"] = args.api_key
        dirty = True

    if args.contact:
        config["contact"] = args.contact
        dirty = True

    if args.model:
        config["model"] = args.model
        dirty = True

    if dirty:
        save_config(config)

    # ---- Resolve values ----
    api_key = resolve_api_key(args.api_key, config)
    contact = config.get("contact")
    model = config.get("model", DEFAULT_MODEL)

    # ---- Prompt for missing required values ----
    if not contact:
        contact = input("Enter the contact phone number or email: ").strip()
        if not contact:
            log("ERROR: A contact is required.")
            sys.exit(1)
        config["contact"] = contact
        save_config(config)

    if args.test:
        run_test(contact)
        return

    if not api_key:
        log(
            "ERROR: No API key found. Provide one via:\n"
            "  --api-key flag\n"
            "  ANTHROPIC_API_KEY environment variable\n"
            "  or store it in the config file"
        )
        sys.exit(1)

    # ---- Validate anthropic package ----
    try:
        import anthropic  # noqa: F401
    except ImportError:
        log("ERROR: 'anthropic' package not installed. Run: pip install anthropic")
        sys.exit(1)

    # ---- Go ----
    run_bot(api_key, contact, model)


if __name__ == "__main__":
    main()
