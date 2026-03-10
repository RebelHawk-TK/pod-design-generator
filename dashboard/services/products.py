"""Product performance service — revenue breakdowns by type, landmark, and style."""

from __future__ import annotations

from collections import defaultdict

LANDMARKS = [
    "eiffel tower", "taj mahal", "colosseum", "great wall", "notre dame",
    "neuschwanstein", "mount fuji", "golden gate", "sydney opera", "santorini",
    "angkor wat", "machu picchu", "sagrada familia", "parthenon", "stonehenge",
    "moai", "pyramids giza", "petra", "st basils", "chichen itza",
    "christ redeemer", "hagia sophia", "tower of pisa", "big ben", "statue of liberty",
]

ART_STYLES = [
    "starry night", "great wave", "water lilies", "the scream",
    "cafe terrace", "composition vii",
]


def _build_product_revenue(orders: list[dict], products: list[dict]) -> dict[str, float]:
    """Map product_id -> total revenue from order line items."""
    revenue = defaultdict(float)
    for order in orders:
        if order.get("financial_status") in ("voided", "refunded"):
            continue
        for item in order.get("line_items", []):
            revenue[item.get("product_id")] += float(item.get("price", 0)) * item.get("quantity", 1)
    return revenue


def _product_map(products: list[dict]) -> dict:
    """Build product_id -> product dict."""
    return {p["id"]: p for p in products}


def get_top_products(orders: list[dict], products: list[dict], limit: int = 20) -> list[dict]:
    """Top N products by revenue."""
    revenue = _build_product_revenue(orders, products)
    pmap = _product_map(products)

    ranked = sorted(revenue.items(), key=lambda x: x[1], reverse=True)[:limit]
    result = []
    for pid, rev in ranked:
        p = pmap.get(pid, {})
        result.append({
            "title": p.get("title", f"Product {pid}"),
            "revenue": round(rev, 2),
            "product_type": p.get("product_type", ""),
        })
    return result


def get_revenue_by_type(orders: list[dict], products: list[dict]) -> dict:
    """Revenue grouped by product_type (poster, tshirt, sticker, etc.)."""
    revenue = _build_product_revenue(orders, products)
    pmap = _product_map(products)

    by_type = defaultdict(float)
    for pid, rev in revenue.items():
        p = pmap.get(pid, {})
        ptype = p.get("product_type", "Other") or "Other"
        by_type[ptype] += rev

    labels = sorted(by_type.keys())
    return {
        "labels": labels,
        "values": [round(by_type[l], 2) for l in labels],
    }


def _match_tags(tags_str: str, keywords: list[str]) -> list[str]:
    """Find which keywords appear in the comma-separated tags string."""
    tags_lower = tags_str.lower()
    return [kw for kw in keywords if kw in tags_lower]


def get_revenue_by_landmark(orders: list[dict], products: list[dict]) -> dict:
    """Revenue grouped by landmark (matched from product tags)."""
    revenue = _build_product_revenue(orders, products)
    pmap = _product_map(products)

    by_landmark = defaultdict(float)
    for pid, rev in revenue.items():
        p = pmap.get(pid, {})
        tags = p.get("tags", "")
        matches = _match_tags(tags, LANDMARKS)
        for lm in matches:
            by_landmark[lm] += rev

    # Top 15 by revenue
    ranked = sorted(by_landmark.items(), key=lambda x: x[1], reverse=True)[:15]
    labels = [r[0].title() for r in ranked]
    values = [round(r[1], 2) for r in ranked]

    return {"labels": labels, "values": values}


def get_revenue_by_style(orders: list[dict], products: list[dict]) -> dict:
    """Revenue grouped by art style (matched from product tags)."""
    revenue = _build_product_revenue(orders, products)
    pmap = _product_map(products)

    by_style = defaultdict(float)
    for pid, rev in revenue.items():
        p = pmap.get(pid, {})
        tags = p.get("tags", "")
        matches = _match_tags(tags, ART_STYLES)
        for s in matches:
            by_style[s] += rev

    labels = [s.title() for s in ART_STYLES]
    values = [round(by_style.get(s, 0), 2) for s in ART_STYLES]

    return {"labels": labels, "values": values}
