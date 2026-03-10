"""JSON API endpoints for the dashboard charts."""

from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

from ..cache import bust_cache, get_cached, set_cached
from ..services.uploads import get_all_upload_stats

api_bp = Blueprint("api", __name__)

ORDERS_TTL = 900   # 15 minutes
PRODUCTS_TTL = 3600  # 1 hour


def _get_shopify_data(resource: str) -> list[dict]:
    """Fetch Shopify data with caching. Returns [] if not configured."""
    if not current_app.config.get("SHOPIFY_CONFIGURED"):
        return []

    ttl = ORDERS_TTL if resource == "orders" else PRODUCTS_TTL
    cached = get_cached(resource, ttl)
    if cached is not None:
        return cached

    from ..shopify_api import ShopifyAPI
    api = ShopifyAPI()

    if resource == "orders":
        data = api.get_orders()
    else:
        data = api.get_products()

    set_cached(resource, data)
    return data


@api_bp.route("/overview")
def overview():
    from ..services.sales import get_sales_overview

    days_param = request.args.get("days")
    days = int(days_param) if days_param else None

    orders = _get_shopify_data("orders")
    if not orders:
        return jsonify({
            "total_revenue": 0, "total_orders": 0, "aov": 0,
            "orders_this_week": 0,
            "daily_labels": [], "daily_revenue": [], "daily_orders": [],
            "empty": True,
        })

    data = get_sales_overview(orders, days=days)
    data["empty"] = False
    return jsonify(data)


@api_bp.route("/products/top")
def products_top():
    from ..services.products import get_top_products

    orders = _get_shopify_data("orders")
    products = _get_shopify_data("products")
    if not orders:
        return jsonify({"products": [], "empty": True})

    return jsonify({"products": get_top_products(orders, products), "empty": False})


@api_bp.route("/products/by-type")
def products_by_type():
    from ..services.products import get_revenue_by_type

    orders = _get_shopify_data("orders")
    products = _get_shopify_data("products")
    if not orders:
        return jsonify({"labels": [], "values": [], "empty": True})

    data = get_revenue_by_type(orders, products)
    data["empty"] = False
    return jsonify(data)


@api_bp.route("/products/by-landmark")
def products_by_landmark():
    from ..services.products import get_revenue_by_landmark

    orders = _get_shopify_data("orders")
    products = _get_shopify_data("products")
    if not orders:
        return jsonify({"labels": [], "values": [], "empty": True})

    data = get_revenue_by_landmark(orders, products)
    data["empty"] = False
    return jsonify(data)


@api_bp.route("/products/by-style")
def products_by_style():
    from ..services.products import get_revenue_by_style

    orders = _get_shopify_data("orders")
    products = _get_shopify_data("products")
    if not orders:
        return jsonify({"labels": [], "values": [], "empty": True})

    data = get_revenue_by_style(orders, products)
    data["empty"] = False
    return jsonify(data)


@api_bp.route("/uploads")
def uploads():
    return jsonify(get_all_upload_stats())


@api_bp.route("/refresh", methods=["POST"])
def refresh():
    count = bust_cache()
    return jsonify({"status": "ok", "files_cleared": count})
