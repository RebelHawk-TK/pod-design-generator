"""Flask app factory for the Shopify Sales Analytics Dashboard."""

from __future__ import annotations

from flask import Flask

from .config import load_config


def create_app() -> Flask:
    app = Flask(__name__)

    # Check config availability at startup
    config = load_config()
    app.config["SHOPIFY_CONFIGURED"] = config is not None

    from .routes.views import views_bp
    from .routes.api import api_bp

    app.register_blueprint(views_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
