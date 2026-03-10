#!/usr/bin/env python3
"""Telegram bot that forwards messages to Claude Code CLI and returns responses.

Setup:
    1. Create bot via @BotFather in Telegram
    2. Add token to .telegram_bot_config
    3. Run: python3 telegram_bot.py
    4. Message the bot — it logs your user ID
    5. Add your user ID to .telegram_bot_config allowed_user_ids
    6. Restart the bot
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

SCRIPT_DIR = Path(__file__).resolve().parent

from keychain_config import load_config as _load_keychain_config, save_config as _save_keychain_config
CLAUDE_PATH = "/Users/rebelhawk/.local/bin/claude"

# Limit concurrent Claude invocations
_claude_semaphore = asyncio.Semaphore(2)

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

# Suppress HTTP client logs that leak bot tokens in URLs
for _logger_name in ("urllib3", "httpx", "httpcore", "telegram.ext", "telegram"):
    logging.getLogger(_logger_name).setLevel(logging.WARNING)


def load_config() -> dict:
    return _load_keychain_config("telegram")


CONFIG = load_config()
TOKEN = CONFIG["token"]
ALLOWED_USER_IDS: set[int] = set(CONFIG.get("allowed_user_ids", []))
MODEL = CONFIG.get("model", "sonnet")
CLAUDE_TIMEOUT = CONFIG.get("claude_timeout", 120)


def _set_model(name: str) -> None:
    global MODEL
    MODEL = name


def is_authorized(user_id: int) -> bool:
    if not ALLOWED_USER_IDS:
        return True  # No restriction if list is empty (first-run mode)
    return user_id in ALLOWED_USER_IDS


async def cmd_start(update: Update, context) -> None:
    user = update.effective_user
    log.info(f"/start from user {user.id} ({user.username})")
    await update.message.reply_text(
        f"Hi {user.first_name}! I'm connected to Claude Code.\n\n"
        f"Your user ID: {user.id}\n"
        f"Send me any message and I'll forward it to Claude.\n\n"
        f"Commands:\n"
        f"/model <name> — switch model (sonnet/opus/haiku)\n"
        f"/help — show this message"
    )


async def cmd_help(update: Update, context) -> None:
    await update.message.reply_text(
        "Send any text message and I'll pass it to Claude Code CLI.\n\n"
        "Commands:\n"
        "/model <name> — switch model (sonnet/opus/haiku)\n"
        "/help — show this message"
    )


async def cmd_model(update: Update, context) -> None:
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("Unauthorized.")
        return

    if not context.args:
        await update.message.reply_text(f"Current model: {MODEL}\nUsage: /model sonnet")
        return

    new_model = context.args[0].lower()
    valid = {"sonnet", "opus", "haiku"}
    if new_model not in valid:
        await update.message.reply_text(f"Invalid model. Choose: {', '.join(valid)}")
        return

    # Update config in Keychain and module-level MODEL
    config = load_config()
    config["model"] = new_model
    _save_keychain_config("telegram", config)

    _set_model(new_model)
    await update.message.reply_text(f"Model switched to: {new_model}")
    log.info(f"Model changed to {new_model} by user {update.effective_user.id}")


async def handle_message(update: Update, context) -> None:
    user_id = update.effective_user.id
    user_text = update.message.text

    if not is_authorized(user_id):
        log.warning(f"Unauthorized message from {user_id}: {user_text[:50]}")
        await update.message.reply_text("Unauthorized.")
        return

    log.info(f"Message from {user_id}: {user_text[:100]}")

    # Send typing indicator
    await update.message.chat.send_action("typing")

    async with _claude_semaphore:
        try:
            # Run claude CLI in a thread to avoid blocking
            env = os.environ.copy()
            env.pop("CLAUDECODE", None)  # Avoid nested-session guard
            env["PATH"] = f"/Users/rebelhawk/.local/bin:/usr/local/bin:/usr/bin:/bin:{env.get('PATH', '')}"

            result = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: subprocess.run(
                    [CLAUDE_PATH, "-p", "--model", MODEL, user_text],
                    capture_output=True,
                    text=True,
                    timeout=CLAUDE_TIMEOUT,
                    env=env,
                    cwd=str(SCRIPT_DIR),
                ),
            )

            response = result.stdout.strip()
            if not response:
                response = f"[No output]\n{result.stderr[:500]}" if result.stderr else "[No output]"

        except subprocess.TimeoutExpired:
            response = f"[Timed out after {CLAUDE_TIMEOUT}s]"
        except Exception as exc:
            response = f"[Error: {exc}]"
            log.error(f"Claude invocation error: {exc}")

    log.info(f"Response length: {len(response)} chars")

    # Telegram 4096 char limit per message
    for i in range(0, len(response), 4096):
        await update.message.reply_text(response[i : i + 4096])


def main() -> None:
    log.info(f"Starting Telegram bot (model={MODEL})")
    if ALLOWED_USER_IDS:
        log.info(f"Authorized users: {ALLOWED_USER_IDS}")
    else:
        log.info("No user restrictions — first-run mode. Check logs for your user ID.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("model", cmd_model))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
