"""View routes — serves the dashboard HTML page."""

from __future__ import annotations

from flask import Blueprint, current_app, render_template

views_bp = Blueprint("views", __name__)


@views_bp.route("/")
def index():
    if not current_app.config.get("SHOPIFY_CONFIGURED"):
        return render_template("setup.html"), 200
    return render_template("dashboard.html")
