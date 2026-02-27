"""Shopify Blog API client — create and manage blog articles."""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

import requests

CONFIG_PATH = Path(__file__).parent.parent / ".shopify_config.json"


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


class ShopifyBlogAPI:
    """Client for Shopify Blog/Article endpoints."""

    def __init__(self):
        config = _load_config()
        self.base_url = (
            f"https://{config['shop_domain']}/admin/api/"
            f"{config.get('api_version', '2024-01')}"
        )
        self.session = requests.Session()
        self.session.headers.update({
            "X-Shopify-Access-Token": config["api_token"],
            "Content-Type": "application/json",
        })

    def _request(self, method: str, endpoint: str, json_data=None, params=None) -> requests.Response:
        """Make API request with rate limit handling."""
        url = f"{self.base_url}{endpoint}"
        resp = self.session.request(method, url, json=json_data, params=params, timeout=30)

        if resp.status_code == 429:
            retry_after = float(resp.headers.get("Retry-After", 2))
            print(f"Rate limited — retrying after {retry_after}s")
            time.sleep(retry_after)
            resp = self.session.request(method, url, json=json_data, params=params, timeout=30)

        resp.raise_for_status()
        return resp

    def get_or_create_blog(self, title: str = "Art & Travel") -> int:
        """Find existing blog by title or create new one. Returns blog_id."""
        resp = self._request("GET", "/blogs.json")
        blogs = resp.json().get("blogs", [])
        for blog in blogs:
            if blog["title"] == title:
                print(f"Found blog '{title}' (id: {blog['id']})")
                return blog["id"]

        resp = self._request("POST", "/blogs.json", json_data={
            "blog": {"title": title}
        })
        blog = resp.json()["blog"]
        print(f"Created blog '{title}' (id: {blog['id']})")
        return blog["id"]

    def create_article(
        self,
        blog_id: int,
        title: str,
        body_html: str,
        tags: str = "",
        summary: str = "",
        published: bool = True,
    ) -> dict:
        """Create a blog article. Returns the created article dict."""
        article_data: dict = {
            "title": title,
            "body_html": body_html,
            "tags": tags,
            "published": published,
        }
        if summary:
            article_data["summary_html"] = summary

        resp = self._request("POST", f"/blogs/{blog_id}/articles.json", json_data={
            "article": article_data,
        })
        article = resp.json()["article"]
        print(f"Created article '{title}' (id: {article['id']})")
        return article

    def update_article(self, blog_id: int, article_id: int, **fields) -> dict:
        """Update a blog article. Returns the updated article dict."""
        resp = self._request("PUT", f"/blogs/{blog_id}/articles/{article_id}.json", json_data={
            "article": fields,
        })
        article = resp.json()["article"]
        return article

    def list_articles(self, blog_id: int) -> list:
        """List all articles in a blog with pagination."""
        params: dict = {"limit": 250}
        all_articles: list = []

        endpoint = f"/blogs/{blog_id}/articles.json"
        while True:
            resp = self._request("GET", endpoint, params=params)
            data = resp.json()
            all_articles.extend(data.get("articles", []))

            link = resp.headers.get("Link", "")
            match = re.search(r'<([^>]+)>;\s*rel="next"', link)
            if not match:
                break

            next_url = match.group(1)
            info_match = re.search(r"page_info=([^&]+)", next_url)
            if not info_match:
                break

            params = {"limit": 250, "page_info": info_match.group(1)}

        return all_articles
