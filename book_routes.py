# book_routes.py (public version)
"""
Flask blueprint for NeuraAI v10k Hyperluxe book platform
Completely free access for everyone
"""

from flask import Blueprint, jsonify, request
from book_platform import list_books, get_book

books_bp = Blueprint("books_bp", __name__)

@books_bp.route("/books", methods=["GET"])
def all_books():
    """List all books (free for everyone)"""
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    category = request.args.get("category")
    q = request.args.get("q")
    result = list_books(page=page, page_size=page_size, category=category, q=q)
    # Only include free books
    result["books"] = [b for b in result["books"] if b.get("free", True)]
    return jsonify(result)

@books_bp.route("/books/<book_id>", methods=["GET"])
def book_detail(book_id):
    """Get details of a single book"""
    book = get_book(book_id)
    if not book or not book.get("free", True):
        return jsonify({"error": "Book not available"}), 404
    return jsonify(book)

@books_bp.route("/books/<book_id>/download", methods=["GET"])
def download_book(book_id):
    """Download a free book (simulated URL)"""
    book = get_book(book_id)
    if not book or not book.get("free", True):
        return jsonify({"error": "Book not available"}), 404
    return jsonify({"ok": True, "download_url": f"/uploads/{book.get('content_path', '')}"})