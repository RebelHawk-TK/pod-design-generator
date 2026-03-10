"""Secure config storage using macOS Keychain.

Stores JSON config values in macOS Keychain via the `security` CLI tool.
Falls back to reading plain-text config files if Keychain entry doesn't exist
(for first-time migration).

Usage:
    from keychain_config import load_config

    config = load_config("printify")
    # Returns dict from Keychain, or migrates from .printify_config.json on first call

    # To manually store/update:
    from keychain_config import save_config
    save_config("printify", {"token": "...", "shop_id": 123})
"""

from __future__ import annotations

import json
import logging
import subprocess
from pathlib import Path

log = logging.getLogger(__name__)

SCRIPT_DIR = Path(__file__).resolve().parent
KEYCHAIN_SERVICE = "com.moderndesignconcept"

# Map of config names to their legacy plain-text file paths
_LEGACY_FILES: dict[str, str] = {
    "printify": ".printify_config.json",
    "shopify": ".shopify_config.json",
    "pinterest": ".pinterest_config.json",
    "pexels": ".pexels_config.json",
    "telegram": ".telegram_bot_config",
    "email_monitor": ".email_monitor_config",
    "pinterest_tokens": ".pinterest_session/tokens.json",
}


def _keychain_account(name: str) -> str:
    return f"{KEYCHAIN_SERVICE}.{name}"


def save_config(name: str, data: dict) -> None:
    """Store config dict in macOS Keychain."""
    account = _keychain_account(name)
    json_str = json.dumps(data)

    # Delete existing entry (ignore errors if not found)
    subprocess.run(
        ["security", "delete-generic-password", "-s", KEYCHAIN_SERVICE, "-a", account],
        capture_output=True,
    )

    # Add new entry
    result = subprocess.run(
        [
            "security", "add-generic-password",
            "-s", KEYCHAIN_SERVICE,
            "-a", account,
            "-w", json_str,
            "-U",  # update if exists
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Failed to save to Keychain: {result.stderr.strip()}")

    log.info(f"Saved config '{name}' to Keychain")


def _read_from_keychain(name: str) -> dict | None:
    """Read config dict from macOS Keychain. Returns None if not found."""
    account = _keychain_account(name)

    result = subprocess.run(
        ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-a", account, "-w"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return None

    try:
        return json.loads(result.stdout.strip())
    except json.JSONDecodeError:
        log.error(f"Keychain entry '{name}' contains invalid JSON")
        return None


def _read_legacy_file(name: str) -> dict | None:
    """Read from legacy plain-text config file."""
    filename = _LEGACY_FILES.get(name)
    if not filename:
        return None

    filepath = SCRIPT_DIR / filename
    if not filepath.exists():
        return None

    try:
        return json.loads(filepath.read_text())
    except (json.JSONDecodeError, OSError) as e:
        log.error(f"Failed to read legacy config {filepath}: {e}")
        return None


def load_config(name: str) -> dict:
    """Load config from Keychain, migrating from file on first access.

    Priority:
        1. macOS Keychain
        2. Legacy plain-text file (auto-migrates to Keychain)
        3. Raises FileNotFoundError
    """
    # Try Keychain first
    data = _read_from_keychain(name)
    if data is not None:
        return data

    # Fall back to legacy file and migrate
    data = _read_legacy_file(name)
    if data is not None:
        log.info(f"Migrating config '{name}' from file to Keychain")
        save_config(name, data)
        return data

    raise FileNotFoundError(
        f"No config found for '{name}' in Keychain or legacy file "
        f"({_LEGACY_FILES.get(name, 'unknown')})"
    )


def migrate_all() -> None:
    """Migrate all legacy config files to Keychain."""
    for name in _LEGACY_FILES:
        try:
            load_config(name)
            print(f"  ✓ {name}")
        except FileNotFoundError:
            print(f"  - {name} (no file found, skipping)")


if __name__ == "__main__":
    print("Migrating configs to macOS Keychain...")
    migrate_all()
    print("\nDone. You can now delete the plain-text config files if desired.")
