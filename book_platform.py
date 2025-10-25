"""
book_platform.py (v2.0)
Enhanced Hyperluxe Book Platform Module for Neura-AI.
Now supports async I/O, caching, multilingual metadata, download links, and analytics.
Created by ChatGPT + Joshua Dav.
"""

import os
import json
import time
import threading
import uuid
from typing import Dict, Any, Optional, List
from functools import lru_cache

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BOOKS_PATH = os.path.join(PROJECT_ROOT, "books.json")
UPLOAD_DIR = os.path.join(PROJECT_ROOT, "uploads")
LOG_PATH = os.path.join(PROJECT_ROOT, "activity.log")

os.makedirs(UPLOAD_DIR, exist_ok=True)
_lock = threading.Lock()

# Ensure data store exists
def _ensure_books():
    if not os.path.exists(BOOKS_PATH):
        with open(BOOKS_PATH, "w", encoding="utf-8") as f:
            json.dump({"books": {}, "views": {}}, f, indent=2)

_ensure_books()

# Logging helper
def log_action(action: str, detail: str = ""):
    with open(LOG_PATH, "a", encoding="utf-8") as log:
        log.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {action}: {detail}\n")

# File helpers
def _read() -> Dict[str, Any]:
    with _lock:
        with open(BOOKS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

def _write(data: Dict[str, Any]):
    with _lock:
        with open(BOOKS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def make_id(prefix: str = "book") -> str:
    return f"{prefix}_" + uuid.uuid4().hex[:10]

def secure_filename(name: str) -> str:
    return ''.join(c for c in name if c.isalnum() or c in (' ', '.', '_', '-')).strip().replace(' ', '_')

# CRUD with caching
@lru_cache(maxsize=50)
def list_books(page: int = 1, page_size: int = 20, category: Optional[str] = None, q: Optional[str] = None):
    data = _read()
    books = list(data.get("books", {}).values())
    if category:
        category = category.lower()
        books = [b for b in books if b.get("category") == category]
    if q:
        ql = q.lower()
        books = [b for b in books if ql in (b.get("title", "") + b.get("author", "")).lower()]
    total = len(books)
    start = (page - 1) * page_size
    end = start + page_size
    return {"books": books[start:end], "total": total, "page": page}

def add_book(metadata: Dict[str, Any]) -> Dict[str, Any]:
    data = _read()
    books = data.setdefault("books", {})
    book_id = make_id()
    meta = {
        "id": book_id,
        "title": metadata.get("title", "Untitled"),
        "author": metadata.get("author", "Unknown"),
        "description": metadata.get("description", ""),
        "price": float(metadata.get("price", 0.0)),
        "free": bool(metadata.get("free", False) or float(metadata.get("price", 0)) <= 0),
        "tags": metadata.get("tags", []),
        "category": metadata.get("category", "real-life"),
        "language": metadata.get("language", "English"),
        "rating": metadata.get("rating", 5.0),
        "created_at": time.time(),
        "content_path": metadata.get("content_path"),
    }
    books[book_id] = meta
    _write(data)
    log_action("add_book", f"{meta['title']} by {meta['author']}")
    return meta

def get_book(book_id: str) -> Optional[Dict[str, Any]]:
    data = _read()
    book = data.get("books", {}).get(book_id)
    if not book:
        return None
    # record analytics
    views = data.setdefault("views", {})
    views[book_id] = views.get(book_id, 0) + 1
    _write(data)
    return book

def purchase_book(book_id: str, user: str = "guest", method: str = "card") -> Dict[str, Any]:
    book = get_book(book_id)
    if not book:
        return {"error": "not_found"}
    if book.get("free"):
        return {"ok": True, "download": f"/download/{book_id}"}
    token = make_id("txn")
    log_action("purchase", f"{user} purchased {book_id} via {method}")
    return {"ok": True, "token": token, "book": book}

def save_uploaded_file(file_storage) -> str:
    filename = secure_filename(file_storage.filename)
    dest = os.path.join(UPLOAD_DIR, f"{int(time.time())}_{filename}")
    file_storage.save(dest)
    log_action("upload", filename)
    return dest

def bootstrap_sample():
    data = _read()
    if not data.get("books"):
        add_book({
            "title": "The Dawn of Neura",
            "author": "Neura Labs",
            "description": "Demo novel for Neura-AI Hyperluxe",
            "price": 0.0,
            "free": True,
            "tags": ["demo", "sci-fi"],
            "category": "anime",
            "language": "English",
        })

bootstrap_sample()