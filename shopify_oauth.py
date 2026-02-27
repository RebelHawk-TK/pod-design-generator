#!/usr/bin/env python3
"""One-time OAuth flow to get a Shopify Admin API access token from a dev dashboard app.

Usage:
    python3 shopify_oauth.py

Requires client_id and client_secret in .shopify_config.json.
Opens a browser for authorization, then saves the access token back to the config.
"""

from __future__ import annotations

import json
import secrets
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlencode, urlparse, parse_qs

import requests

CONFIG_PATH = Path(__file__).parent / ".shopify_config.json"
REDIRECT_URI = "http://localhost:9877/callback"
SCOPES = "read_content,write_content,read_products,read_orders"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError("Missing .shopify_config.json")
    return json.loads(CONFIG_PATH.read_text())


def save_config(config: dict) -> None:
    CONFIG_PATH.write_text(json.dumps(config, indent=2))


class OAuthHandler(BaseHTTPRequestHandler):
    """Handle the OAuth callback."""

    auth_code = None

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if "code" in params:
            OAuthHandler.auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Authorization successful!</h1><p>You can close this tab.</p>")
        else:
            self.send_response(400)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            error = params.get("error", ["unknown"])[0]
            self.wfile.write(f"<h1>Error: {error}</h1>".encode())

    def log_message(self, format, *args):
        pass  # Suppress request logging


def main():
    config = load_config()
    shop_domain = config["shop_domain"]
    client_id = config.get("client_id")
    client_secret = config.get("client_secret")

    if not client_id or not client_secret:
        print("Missing client_id or client_secret in .shopify_config.json")
        print("Add them from the dev dashboard Settings > Credentials page:")
        print('  "client_id": "<Client ID>"')
        print('  "client_secret": "<Secret>"')
        return

    if config.get("api_token", "").startswith("shpat_"):
        print(f"Already have a valid access token: {config['api_token'][:12]}...")
        print("Delete api_token from .shopify_config.json to re-authorize.")
        return

    # Step 1: Build authorization URL
    nonce = secrets.token_urlsafe(16)
    auth_params = urlencode({
        "client_id": client_id,
        "scope": SCOPES,
        "redirect_uri": REDIRECT_URI,
        "state": nonce,
    })
    auth_url = f"https://{shop_domain}/admin/oauth/authorize?{auth_params}"

    print(f"Opening browser for authorization...")
    print(f"URL: {auth_url}\n")
    webbrowser.open(auth_url)

    # Step 2: Wait for callback
    server = HTTPServer(("localhost", 9877), OAuthHandler)
    print("Waiting for authorization callback on http://localhost:9877 ...")
    while OAuthHandler.auth_code is None:
        server.handle_request()

    auth_code = OAuthHandler.auth_code
    print(f"Got authorization code: {auth_code[:8]}...")

    # Step 3: Exchange code for access token
    token_url = f"https://{shop_domain}/admin/oauth/access_token"
    resp = requests.post(token_url, json={
        "client_id": client_id,
        "client_secret": client_secret,
        "code": auth_code,
    })
    resp.raise_for_status()
    data = resp.json()
    access_token = data["access_token"]

    print(f"Got access token: {access_token[:12]}...")

    # Step 4: Save to config
    config["api_token"] = access_token
    save_config(config)
    print(f"\nSaved access token to {CONFIG_PATH}")
    print("You can now run: python3 generate_blog_posts.py --upload --draft")


if __name__ == "__main__":
    main()
