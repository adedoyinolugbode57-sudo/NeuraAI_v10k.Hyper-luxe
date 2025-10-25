"""
neura_router.py
Auto-registers all NeuraAI routes.
"""

from flask import Flask
from ai_engine import app as base_app
from voice_routes import voice_bp
from book_platform import add_book, list_books, get_book
import json

def create_app():
    app = base_app

    # Register blueprints
    app.register_blueprint(voice_bp, url_prefix="/api")

    # Example API routes from other modules
    @app.route("/api/books/list")
    def api_list_books():
        data = list_books()
        return json.dumps(data, indent=2)

    @app.route("/api/books/<book_id>")
    def api_get_book(book_id):
        book = get_book(book_id)
        return json.dumps(book or {"error": "not_found"}, indent=2)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=10000)