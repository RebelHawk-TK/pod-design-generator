"""Shopify Admin REST API client with pagination and rate-limit handling."""

from __future__ import annotations

import re
import time

import requests

from .config import get_config


class ShopifyAPI:
    """Thin wrapper around the Shopify Admin REST API."""

    def __init__(self):
        config = get_config()
        self.shop_domain = config["shop_domain"]
        self.api_version = config.get("api_version", "2024-01")
        self.base_url = f"https://{self.shop_domain}/admin/api/{self.api_version}"
        self.session = requests.Session()
        self.session.headers.update({
            "X-Shopify-Access-Token": config["api_token"],
            "Content-Type": "application/json",
        })

    def _request(self, endpoint: str, params: dict | None = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        resp = self.session.get(url, params=params, timeout=30)

        if resp.status_code == 429:
            retry_after = float(resp.headers.get("Retry-After", 2))
            time.sleep(retry_after)
            resp = self.session.get(url, params=params, timeout=30)

        resp.raise_for_status()
        return resp

    def _paginate(self, endpoint: str, resource_key: str, params: dict | None = None) -> list:
        """Fetch all pages using Link-header cursor pagination."""
        params = dict(params or {})
        params.setdefault("limit", 250)
        all_items = []

        while True:
            resp = self._request(endpoint, params)
            data = resp.json()
            all_items.extend(data.get(resource_key, []))

            # Parse Link header for next page
            link = resp.headers.get("Link", "")
            match = re.search(r'<([^>]+)>;\s*rel="next"', link)
            if not match:
                break

            # Extract page_info from the next URL
            next_url = match.group(1)
            info_match = re.search(r'page_info=([^&]+)', next_url)
            if not info_match:
                break

            params = {"limit": params["limit"], "page_info": info_match.group(1)}

        return all_items

    def get_orders(self, status: str = "any") -> list[dict]:
        """Fetch all orders."""
        return self._paginate(
            "/orders.json",
            "orders",
            {"status": status, "fields": "id,name,created_at,total_price,line_items,financial_status"},
        )

    def get_products(self) -> list[dict]:
        """Fetch all products."""
        return self._paginate(
            "/products.json",
            "products",
            {"fields": "id,title,product_type,tags,variants,images"},
        )
