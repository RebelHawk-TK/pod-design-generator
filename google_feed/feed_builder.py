"""Build Google Shopping XML feed from Shopify product data."""

from __future__ import annotations

import re
from xml.etree.ElementTree import Element, SubElement, ElementTree, indent, register_namespace

from .category_map import get_category

BRAND = "Modern Design Concept"
STORE_URL = "https://modern-design-concept-2.myshopify.com"
G_NS = "http://base.google.com/ns/1.0"

# Colors that appear in Printify variant titles
KNOWN_COLORS = [
    "Black", "White", "Navy", "Dark Heather", "Sport Grey",
    "Royal", "Red", "Sand", "Forest Green", "Maroon",
]

# Sizes that appear in variant titles
KNOWN_SIZES = ["S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL"]


def _strip_html(html: str) -> str:
    """Remove HTML tags and decode common entities."""
    if not html:
        return ""
    text = re.sub(r"<[^>]+>", " ", html)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", " ")
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _parse_color(variant_title: str) -> str | None:
    """Extract color from variant title like 'Black / L'."""
    for color in KNOWN_COLORS:
        if color.lower() in variant_title.lower():
            return color
    return None


def _parse_size(variant_title: str) -> str | None:
    """Extract size from variant title like 'Black / L'."""
    parts = [p.strip() for p in variant_title.split("/")]
    for part in parts:
        if part.upper() in KNOWN_SIZES:
            return part.upper()
    return None


def _g_elem(parent: Element, tag: str, text: str) -> Element:
    """Add a Google-namespaced sub-element."""
    elem = SubElement(parent, f"{{{G_NS}}}{tag}")
    elem.text = text
    return elem


def build_feed(products: list[dict], output_path: str) -> dict:
    """Generate Google Shopping XML feed.

    Args:
        products: List of Shopify product dicts.
        output_path: Path to write the XML file.

    Returns:
        Stats dict with product_count, variant_count, category_breakdown.
    """
    register_namespace("g", G_NS)
    rss = Element("rss", attrib={"version": "2.0"})
    channel = SubElement(rss, "channel")
    SubElement(channel, "title").text = "Modern Design Concept"
    SubElement(channel, "link").text = STORE_URL
    SubElement(channel, "description").text = (
        "Art-inspired posters, t-shirts, and stickers featuring world landmarks "
        "in classic painting styles."
    )

    stats = {"product_count": 0, "variant_count": 0, "categories": {}}

    for product in products:
        product_id = product.get("id")
        title = product.get("title", "")
        handle = product.get("handle", "")
        body_html = product.get("body_html", "")
        product_type = product.get("product_type", "")
        tags = product.get("tags", "")
        images = product.get("images", [])
        variants = product.get("variants", [])

        if not variants or not handle:
            continue

        description = _strip_html(body_html)
        if not description:
            description = title

        product_url = f"{STORE_URL}/products/{handle}"
        image_url = images[0]["src"] if images else ""
        additional_images = [img["src"] for img in images[1:10]] if len(images) > 1 else []

        category = get_category(product_type)
        cat_name = category["product_type"]
        stats["categories"][cat_name] = stats["categories"].get(cat_name, 0) + 1
        stats["product_count"] += 1

        for variant in variants:
            variant_id = variant.get("id")
            price = variant.get("price", "0.00")
            sku = variant.get("sku", "")
            variant_title = variant.get("title", "Default Title")

            item = SubElement(channel, "item")

            _g_elem(item, "id", str(variant_id))
            _g_elem(item, "title", title)
            _g_elem(item, "description", description)
            _g_elem(item, "link", product_url)
            if image_url:
                _g_elem(item, "image_link", image_url)
            for extra_img in additional_images:
                _g_elem(item, "additional_image_link", extra_img)
            _g_elem(item, "price", f"{price} USD")
            _g_elem(item, "availability", "in_stock")
            _g_elem(item, "condition", "new")
            _g_elem(item, "brand", BRAND)
            _g_elem(item, "google_product_category", category["name"])
            _g_elem(item, "product_type", category["product_type"])
            _g_elem(item, "item_group_id", str(product_id))

            if sku:
                _g_elem(item, "mpn", sku)

            _g_elem(item, "shipping_weight", category["shipping_weight"])

            # Color and size from variant title
            color = _parse_color(variant_title)
            if color:
                _g_elem(item, "color", color)

            size = _parse_size(variant_title)
            if size:
                _g_elem(item, "size", size)

            stats["variant_count"] += 1

    tree = ElementTree(rss)
    indent(tree, space="  ")
    tree.write(output_path, encoding="unicode", xml_declaration=True)

    return stats
