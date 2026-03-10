"""Load Shopify API configuration from .shopify_config.json."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from keychain_config import load_config as _load_keychain_config


def load_config() -> dict | None:
    """Load Shopify config from Keychain."""
    try:
        return _load_keychain_config("shopify")
    except FileNotFoundError:
        return None


def get_config() -> dict:
    """Load config or raise with setup instructions."""
    config = load_config()
    if config is None:
        raise FileNotFoundError("Missing shopify config in Keychain")
    for key in ("shop_domain", "api_token", "api_version"):
        if key not in config:
            raise ValueError(f"Missing '{key}' in shopify config")
    return config
