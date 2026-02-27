"""Product type → Google Shopping category mapping."""

GOOGLE_CATEGORIES = {
    "poster": {
        "id": 500044,
        "name": "Home & Garden > Decor > Wall Art",
        "product_type": "Wall Art > Posters",
        "shipping_weight": "0.5 lb",
    },
    "tshirt": {
        "id": 212,
        "name": "Apparel & Accessories > Clothing > Shirts & Tops > T-Shirts",
        "product_type": "Clothing > T-Shirts",
        "shipping_weight": "0.3 lb",
    },
    "t-shirt": {
        "id": 212,
        "name": "Apparel & Accessories > Clothing > Shirts & Tops > T-Shirts",
        "product_type": "Clothing > T-Shirts",
        "shipping_weight": "0.3 lb",
    },
    "sticker": {
        "id": 500044,
        "name": "Arts & Entertainment > Party & Celebration > Party Supplies > Stickers",
        "product_type": "Stickers > Die-Cut Stickers",
        "shipping_weight": "0.1 lb",
    },
}

# Fallback for unrecognized product types
DEFAULT_CATEGORY = {
    "id": 500044,
    "name": "Home & Garden > Decor > Wall Art",
    "product_type": "Wall Art",
    "shipping_weight": "0.5 lb",
}


def get_category(product_type: str) -> dict:
    """Look up Google category for a Shopify product_type string."""
    key = product_type.strip().lower().replace("-", "").replace(" ", "")
    # Try exact match first
    if key in GOOGLE_CATEGORIES:
        return GOOGLE_CATEGORIES[key]
    # Try substring match (e.g. "Unisex Heavy Cotton Tee" contains "tshirt"? No — check tags)
    for cat_key, cat_val in GOOGLE_CATEGORIES.items():
        if cat_key in key:
            return cat_val
    return DEFAULT_CATEGORY
