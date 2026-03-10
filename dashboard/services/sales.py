"""Sales aggregation service."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone


def get_sales_overview(orders: list[dict], days: int | None = None) -> dict:
    """Compute revenue, order count, AOV, and daily breakdown.

    Args:
        orders: Raw Shopify order dicts.
        days: Filter to last N days. None = all time.
    """
    now = datetime.now(timezone.utc)
    cutoff = (now - timedelta(days=days)) if days else None

    filtered = []
    for o in orders:
        if o.get("financial_status") in ("voided", "refunded"):
            continue
        created = datetime.fromisoformat(o["created_at"].replace("Z", "+00:00"))
        if cutoff and created < cutoff:
            continue
        filtered.append(o)

    total_revenue = sum(float(o.get("total_price", 0)) for o in filtered)
    total_orders = len(filtered)
    aov = (total_revenue / total_orders) if total_orders else 0

    # Orders this week
    week_ago = now - timedelta(days=7)
    orders_this_week = sum(
        1 for o in filtered
        if datetime.fromisoformat(o["created_at"].replace("Z", "+00:00")) >= week_ago
    )

    # Daily revenue/orders
    daily = defaultdict(lambda: {"revenue": 0.0, "orders": 0})
    for o in filtered:
        date_str = o["created_at"][:10]
        daily[date_str]["revenue"] += float(o.get("total_price", 0))
        daily[date_str]["orders"] += 1

    sorted_daily = sorted(daily.items())

    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "aov": round(aov, 2),
        "orders_this_week": orders_this_week,
        "daily_labels": [d[0] for d in sorted_daily],
        "daily_revenue": [round(d[1]["revenue"], 2) for d in sorted_daily],
        "daily_orders": [d[1]["orders"] for d in sorted_daily],
    }
