#!/usr/bin/env python3
"""Entry point for the Shopify Sales Analytics Dashboard.

Usage:
    python3 run_dashboard.py              # http://127.0.0.1:5000
    python3 run_dashboard.py --port 8080  # custom port
"""

import argparse

from dashboard import create_app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shopify Sales Analytics Dashboard")
    parser.add_argument("--port", type=int, default=8050, help="Port to run on (default: 8050)")
    parser.add_argument("--debug", action="store_true", help="Enable Flask debug mode")
    args = parser.parse_args()

    app = create_app()
    print(f"Dashboard starting at http://localhost:{args.port}")
    app.run(host="localhost", port=args.port, debug=args.debug)
