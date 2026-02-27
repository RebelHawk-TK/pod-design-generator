"""Fetch all products from Shopify Admin REST API."""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

import requests

CONFIG_PATH = Path(__file__).parent.parent / ".shopify_config.json"

PRODUCT_FIELDS = (
    "id,title,body_html,handle,product_type,vendor,tags,variants,images,published_at"
)


def _load_config() -> dict:
    """Load Shopify config or raise with instructions."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            "Missing .shopify_config.json — create it with shop_domain, api_token, api_version"
        )
    config = json.loads(CONFIG_PATH.read_text())
    for key in ("shop_domain", "api_token", "api_version"):
        if key not in config:
            raise ValueError(f"Missing '{key}' in .shopify_config.json")
    return config


def fetch_all_products(product_type_filter: str | None = None) -> list[dict]:
    """Fetch all products from Shopify with pagination.

    Args:
        product_type_filter: Optional filter like "poster" or "tshirt".
                             Matches case-insensitively against product_type.

    Returns:
        List of product dicts from Shopify API.
    """
    config = _load_config()
    base_url = (
        f"https://{config['shop_domain']}/admin/api/"
        f"{config.get('api_version', '2024-01')}"
    )
    session = requests.Session()
    session.headers.update({
        "X-Shopify-Access-Token": config["api_token"],
        "Content-Type": "application/json",
    })

    params: dict = {"limit": 250, "fields": PRODUCT_FIELDS}
    if product_type_filter:
        params["product_type"] = product_type_filter

    all_products: list[dict] = []
    endpoint = f"{base_url}/products.json"

    while True:
        resp = session.get(endpoint, params=params, timeout=30)

        if resp.status_code == 429:
            retry_after = float(resp.headers.get("Retry-After", 2))
            print(f"  Rate limited — retrying after {retry_after}s")
            time.sleep(retry_after)
            resp = session.get(endpoint, params=params, timeout=30)

        resp.raise_for_status()
        data = resp.json()
        products = data.get("products", [])
        all_products.extend(products)
        print(f"  Fetched {len(products)} products (total: {len(all_products)})")

        # Cursor pagination via Link header
        link = resp.headers.get("Link", "")
        match = re.search(r'<([^>]+)>;\s*rel="next"', link)
        if not match:
            break

        next_url = match.group(1)
        info_match = re.search(r"page_info=([^&]+)", next_url)
        if not info_match:
            break

        params = {"limit": 250, "page_info": info_match.group(1)}

    # Client-side filter if product_type_filter didn't work via API param
    if product_type_filter and all_products:
        ft = product_type_filter.lower()
        all_products = [
            p for p in all_products
            if ft in (p.get("product_type") or "").lower()
        ]

    return all_products
