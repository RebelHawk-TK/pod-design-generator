#!/usr/bin/env python3
"""Redbubble analytics scraper.

Scrapes portfolio stats, per-design views/favorites, and sales history
from your Redbubble account using Playwright browser automation.
Reuses the existing .redbubble_session/ for authentication.

Usage:
    python3 scrape_redbubble_stats.py                  # Full scrape
    python3 scrape_redbubble_stats.py --works-only     # Just designs list
    python3 scrape_redbubble_stats.py --format json     # JSON only
    python3 scrape_redbubble_stats.py --format csv      # CSV only
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from upload_common import launch_browser, wait_for_cloudflare

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SESSION_DIR = Path(__file__).parent / ".redbubble_session"
STATS_DIR = Path(__file__).parent / "stats"

BASE_URL = "https://www.redbubble.com"
PORTFOLIO_URL = f"{BASE_URL}/portfolio"
MANAGE_WORKS_URL = f"{BASE_URL}/portfolio/manage_works"

# ---------------------------------------------------------------------------
# Session check
# ---------------------------------------------------------------------------

def check_session(page) -> bool:
    """Check if we're logged in to Redbubble."""
    try:
        page.goto(PORTFOLIO_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)
        wait_for_cloudflare(page)
        url = page.url.lower()
        if "login" in url or "sign_in" in url or "auth" in url:
            return False
        return True
    except Exception:
        return False


def wait_for_login(page) -> None:
    """Prompt user to log in manually."""
    print("\n=== Manual login required ===")
    print("  1. Log in to Redbubble in the browser window.")
    print("  2. Press ENTER here when done.")
    input("  Press ENTER when logged in... ")
    time.sleep(2)


# ---------------------------------------------------------------------------
# Works scraper (XHR intercept + DOM fallback)
# ---------------------------------------------------------------------------

def scrape_works(page) -> list[dict]:
    """Scrape all designs from the manage works page."""
    print("\nScraping designs...")

    # Try XHR interception first
    captured_json = []

    def handle_response(response):
        url = response.url.lower()
        if ("works" in url or "manage" in url) and response.status == 200:
            content_type = response.headers.get("content-type", "")
            if "json" in content_type:
                try:
                    captured_json.append(response.json())
                except Exception:
                    pass

    page.on("response", handle_response)
    page.goto(MANAGE_WORKS_URL, wait_until="networkidle", timeout=45000)
    wait_for_cloudflare(page)
    time.sleep(5)
    page.off("response", handle_response)

    # If we captured JSON data, parse it
    if captured_json:
        print(f"  Captured {len(captured_json)} JSON responses via XHR")
        return _parse_xhr_works(captured_json)

    # Fallback: DOM scraping
    print("  Falling back to DOM scraping...")
    return _scrape_works_dom(page)


def _parse_xhr_works(responses: list) -> list[dict]:
    """Parse works from intercepted XHR JSON responses."""
    works = []
    for resp in responses:
        # Try common Redbubble JSON structures
        items = []
        if isinstance(resp, list):
            items = resp
        elif isinstance(resp, dict):
            items = resp.get("works", resp.get("items", resp.get("data", [])))
            if isinstance(items, dict):
                items = items.get("works", items.get("items", []))

        for item in items:
            if isinstance(item, dict) and ("title" in item or "name" in item):
                works.append({
                    "id": str(item.get("id", "")),
                    "title": item.get("title", item.get("name", "")),
                    "url": item.get("url", item.get("href", "")),
                    "status": item.get("status", ""),
                    "views": item.get("views", item.get("view_count", 0)),
                    "favorites": item.get("favorites", item.get("favorite_count", 0)),
                    "created_at": item.get("created_at", item.get("publishedAt", "")),
                })

    return works


def _scrape_works_dom(page) -> list[dict]:
    """Scrape works from the DOM as fallback."""
    works = page.evaluate("""() => {
        const results = [];
        // Try multiple selector patterns
        const cards = document.querySelectorAll(
            '[class*="work-card"], [class*="WorkCard"], [class*="manage-work"], ' +
            'tr[class*="work"], [data-work-id], .works-list-item'
        );

        cards.forEach(card => {
            const titleEl = card.querySelector(
                'a[class*="title"], h3, h4, [class*="title"], [class*="name"]'
            );
            const title = titleEl?.textContent?.trim() || '';
            const url = titleEl?.href || '';
            const id = card.getAttribute('data-work-id') || card.getAttribute('data-id') || '';

            // Try to find stats
            const statsEls = card.querySelectorAll('[class*="stat"], [class*="count"], [class*="view"]');
            let views = 0, favorites = 0;
            statsEls.forEach(el => {
                const text = el.textContent?.trim()?.toLowerCase() || '';
                const num = parseInt(el.textContent?.replace(/[^0-9]/g, '')) || 0;
                if (text.includes('view')) views = num;
                else if (text.includes('fav') || text.includes('heart')) favorites = num;
            });

            if (title) {
                results.push({ id, title, url, views, favorites, status: '', created_at: '' });
            }
        });

        return results;
    }""")

    # If card selectors failed, try table rows
    if not works:
        works = page.evaluate("""() => {
            const results = [];
            const rows = document.querySelectorAll('table tbody tr');
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                if (cells.length >= 2) {
                    const titleEl = cells[0]?.querySelector('a') || cells[1]?.querySelector('a');
                    results.push({
                        id: '',
                        title: titleEl?.textContent?.trim() || cells[0]?.textContent?.trim() || '',
                        url: titleEl?.href || '',
                        views: 0,
                        favorites: 0,
                        status: '',
                        created_at: '',
                    });
                }
            });
            return results;
        }""")

    print(f"  Found {len(works)} designs via DOM")
    return works


# ---------------------------------------------------------------------------
# Account summary scraper
# ---------------------------------------------------------------------------

def scrape_account_summary(page) -> dict:
    """Scrape high-level account stats from the portfolio page."""
    print("\nScraping account summary...")

    page.goto(PORTFOLIO_URL, wait_until="networkidle", timeout=45000)
    wait_for_cloudflare(page)
    time.sleep(5)

    summary = page.evaluate("""() => {
        const result = {};
        const body = document.body.textContent || '';

        // Look for stat blocks with numbers
        const statEls = document.querySelectorAll(
            '[class*="stat"], [class*="Stat"], [class*="metric"], [class*="Metric"], ' +
            '[class*="summary"], [class*="Summary"], [class*="count"], [class*="Count"], ' +
            '[class*="earning"], [class*="Earning"], [class*="balance"], [class*="Balance"]'
        );

        statEls.forEach(el => {
            const text = el.textContent?.trim() || '';
            if (text.length < 200) {
                // Try to identify label + value pairs
                const parts = text.split(/\\n/).map(s => s.trim()).filter(Boolean);
                if (parts.length >= 2) {
                    result[parts[0]] = parts[1];
                } else if (parts.length === 1) {
                    const key = el.getAttribute('class') || 'unknown';
                    result[key.slice(0, 50)] = parts[0];
                }
            }
        });

        // Also grab any visible numbers near known labels
        const labels = ['views', 'favorites', 'sales', 'earnings', 'balance', 'designs', 'works'];
        labels.forEach(label => {
            const regex = new RegExp(label + '[:\\\\s]*([$\\\\d,\\\\.]+)', 'i');
            const match = body.match(regex);
            if (match) result[label] = match[1];
        });

        return result;
    }""")

    print(f"  Found {len(summary)} summary stats")
    return summary


# ---------------------------------------------------------------------------
# Sales scraper
# ---------------------------------------------------------------------------

def scrape_sales(page) -> list[dict]:
    """Scrape sales/order history."""
    print("\nScraping sales history...")

    # Try multiple possible sales URLs
    sales_urls = [
        f"{BASE_URL}/portfolio/sales",
        f"{BASE_URL}/portfolio/earnings",
        f"{BASE_URL}/account/order_history",
    ]

    for url in sales_urls:
        try:
            page.goto(url, wait_until="networkidle", timeout=30000)
            wait_for_cloudflare(page)
            time.sleep(3)

            if "login" not in page.url.lower():
                break
        except Exception:
            continue

    sales = page.evaluate("""() => {
        const results = [];

        // Try table rows
        const rows = document.querySelectorAll('table tbody tr, [class*="sale-row"], [class*="order-row"]');
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            if (cells.length >= 3) {
                results.push({
                    date: cells[0]?.textContent?.trim() || '',
                    title: cells[1]?.textContent?.trim() || '',
                    product: cells.length > 3 ? cells[2]?.textContent?.trim() || '' : '',
                    quantity: cells.length > 4 ? cells[3]?.textContent?.trim() || '' : '',
                    earnings: cells[cells.length - 1]?.textContent?.trim() || '',
                });
            }
        });

        // Try card/list layouts
        if (results.length === 0) {
            const cards = document.querySelectorAll('[class*="sale"], [class*="order"], [class*="transaction"]');
            cards.forEach(card => {
                const text = card.textContent?.trim() || '';
                if (text.length > 5 && text.length < 500) {
                    results.push({
                        date: '',
                        title: text.slice(0, 200),
                        product: '',
                        quantity: '',
                        earnings: '',
                    });
                }
            });
        }

        return results;
    }""")

    print(f"  Found {len(sales)} sales records")
    return sales


# ---------------------------------------------------------------------------
# Page info scraper (grab whatever is visible)
# ---------------------------------------------------------------------------

def scrape_page_stats(page, url: str, label: str) -> dict:
    """Generic scraper that extracts visible stats from any page."""
    print(f"\nScraping {label}...")

    try:
        page.goto(url, wait_until="networkidle", timeout=45000)
        wait_for_cloudflare(page)
        time.sleep(5)
    except Exception as e:
        print(f"  Error loading page: {e}")
        return {}

    stats = page.evaluate("""() => {
        const result = {};

        // Grab all visible number elements
        const allEls = document.querySelectorAll('h1, h2, h3, h4, strong, b, [class*="number"], [class*="count"], [class*="stat"], [class*="value"]');
        let idx = 0;
        allEls.forEach(el => {
            const text = el.textContent?.trim() || '';
            const rect = el.getBoundingClientRect();
            if (text && rect.width > 0 && rect.height > 0 && text.length < 100) {
                // Check if parent has a label
                const parent = el.parentElement;
                const siblings = parent?.querySelectorAll('span, p, label, div');
                let label = '';
                siblings?.forEach(sib => {
                    if (sib !== el && sib.textContent?.trim()?.length < 50) {
                        label = sib.textContent.trim();
                    }
                });
                const key = label || `stat_${idx}`;
                result[key] = text;
                idx++;
            }
        });

        return result;
    }""")

    print(f"  Found {len(stats)} stats")
    return stats


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def save_json(data: dict, output_dir: Path) -> Path:
    """Save full stats as JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    path = output_dir / f"redbubble_stats_{date_str}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path


def save_csv(works: list[dict], output_dir: Path) -> Path:
    """Save per-design stats as CSV."""
    output_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    path = output_dir / f"redbubble_works_{date_str}.csv"
    if not works:
        return path
    fieldnames = list(works[0].keys())
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(works)
    return path


def print_summary(data: dict) -> None:
    """Print a human-readable summary to terminal."""
    est = ZoneInfo("America/New_York")
    now = datetime.now(est).strftime("%Y-%m-%d %I:%M %p EST")

    print(f"\n{'=' * 50}")
    print(f"  Redbubble Stats — {now}")
    print(f"{'=' * 50}")

    summary = data.get("account_summary", {})
    if summary:
        print(f"\n  Account Summary:")
        for k, v in summary.items():
            print(f"    {k}: {v}")

    works = data.get("works", [])
    print(f"\n  Designs: {len(works)}")

    if works:
        total_views = sum(w.get("views", 0) for w in works if isinstance(w.get("views"), (int, float)))
        total_favs = sum(w.get("favorites", 0) for w in works if isinstance(w.get("favorites"), (int, float)))
        print(f"  Total views: {total_views:,}")
        print(f"  Total favorites: {total_favs:,}")

        # Top designs by views
        sorted_by_views = sorted(works, key=lambda w: w.get("views", 0), reverse=True)
        if sorted_by_views and sorted_by_views[0].get("views", 0) > 0:
            print(f"\n  Top designs by views:")
            for w in sorted_by_views[:10]:
                print(f"    {w['views']:>6} views  |  {w.get('favorites', 0):>3} favs  |  {w['title'][:50]}")

    sales = data.get("sales", [])
    print(f"\n  Sales records: {len(sales)}")
    if sales:
        for s in sales[:10]:
            print(f"    {s.get('date', 'N/A'):>12}  |  {s.get('earnings', 'N/A'):>8}  |  {s.get('title', '')[:40]}")

    print(f"\n{'=' * 50}\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape Redbubble portfolio analytics and stats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python3 scrape_redbubble_stats.py                  # Full scrape
  python3 scrape_redbubble_stats.py --works-only     # Just designs
  python3 scrape_redbubble_stats.py --format json     # JSON only
""",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=STATS_DIR,
        help=f"Output directory (default: {STATS_DIR})",
    )
    parser.add_argument(
        "--format", choices=["json", "csv", "both"], default="both",
        help="Output format (default: both)",
    )
    parser.add_argument(
        "--works-only", action="store_true",
        help="Only scrape designs list (skip sales)",
    )
    args = parser.parse_args()

    # Launch browser with existing session
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        context, page = launch_browser(p, SESSION_DIR)

        try:
            # Check session
            if not check_session(page):
                wait_for_login(page)
                if not check_session(page):
                    print("Error: still not logged in. Exiting.")
                    context.close()
                    return

            print("Session valid — starting scrape\n")

            # Collect data
            data = {
                "scraped_at": datetime.now(ZoneInfo("America/New_York")).isoformat(),
                "shop_url": f"{BASE_URL}/people/ModernDesignCo/shop",
            }

            # Account summary
            data["account_summary"] = scrape_account_summary(page)

            # Works/designs
            data["