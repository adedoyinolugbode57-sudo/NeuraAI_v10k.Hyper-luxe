"""
book_platform.py (v2.1)
Hyperluxe Book Platform Module for Neura-AI.
Now includes cache invalidation, safer file I/O, upload validation, async support, and log rotation.
Created by ChatGPT + Joshua Dav.
"""

import os
import json
import time
import threading
import uuid
import asyncio
import logging
from functools import lru_cache
from typing import Dict, Any, Optional, List

# === PATHS ===
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BOOKS_PATH = os.path.join(PROJECT_ROOT, "books.json")
UPLOAD_DIR = os.path.join(PROJECT_ROOT, "uploads")
LOG_PATH = os.path.join(PROJECT_ROOT, "activity.log")

os.makedirs(UPLOAD_DIR, exist_ok=True)
_lock = threading.Lock()

# === LOGGING SETUP ===
logger = logging.getLogger("book_platform")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# === UTILITIES ===
def _ensure_books():
    """Ensure the books.json file exists and is valid."""
    if not os.path.exists(BOOKS_PATH):
        with open(BOOKS_PATH, "w", encoding="utf-8") as f:
            json.dump({"books": {}, "views": {}}, f, indent=2)

_ensure_books()

def log_action(action: str, detail: str = ""):
    """Simple log writer with rotation."""
    try:
        if os.path.exists(LOG_PATH) and os.path.getsize(LOG_PATH) > 5_000_000:
            # Rotate log when >5MB
            os.rename(LOG_PATH, LOG_PATH.replace(".log", f"_{int(time.time())}.log"))
        logger.info(f"{action}: {detail}")
    except Exception:
        pass  # Silent fail for safety

def _read() -> Dict[str, Any]:
    """Thread-safe read with corruption fallback."""
    with _lock:
        try:
            with open(BOOKS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            log_action("error", "Corrupt or missing books.json — resetting")
            _ensure_books()
            return {"books": {}, "views": {}}

def _write(data: Dict[str, Any]):
    """Thread-safe write to books.json."""
    with _lock:
        with open(BOOKS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def make_id(prefix: str = "book") -> str:
    """Generate a short, unique ID with prefix."""
    return f"{prefix}_{uuid.uuid4().hex[:10]}"

def secure_filename(name: str) -> str:
    """Remove unsafe characters from filenames."""
    return ''.join(c for c in name if c.isalnum() or c in (' ', '.', '_', '-')).strip().replace(' ', '_')

# === CORE FUNCTIONS ===
@lru_cache(maxsize=50)
def list_books(page: int = 1, page_size: int = 20, category: Optional[str] = None, q: Optional[str] = None):
    """List all books with pagination, filtering, and optional query."""
    data = _read()
    books = list(data.get("books", {}).values())
    if category:
        category = category.lower()
        books = [b for b in books if b.get("category", "").lower() == category]
    if q:
        ql = q.lower()
        books = [b for b in books if ql in (b.get("title", "") + b.get("author", "")).lower()]
    total = len(books)
    start = (page - 1) * page_size
    end = start + page_size
    return {"books": books[start:end], "total": total, "page": page}

def add_book(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Add a new book to the library."""
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
    list_books.cache_clear()
    log_action("add_book", f"{meta['title']} by {meta['author']}")
    return meta

def get_book(book_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a book and log its view."""
    data = _read()
    book = data.get("books", {}).get(book_id)
    if not book:
        return None
    views = data.setdefault("views", {})
    views[book_id] = views.get(book_id, 0) + 1
    _write(data)
    return book

def purchase_book(book_id: str, user: str = "guest", method: str = "card") -> Dict[str, Any]:
    """Simulate a purchase transaction."""
    book = get_book(book_id)
    if not book:
        return {"error": "not_found"}
    if book.get("free"):
        return {"ok": True, "download": f"/download/{book_id}"}
    token = make_id("txn")
    log_action("purchase", f"{user} purchased {book_id} via {method}")
    return {"ok": True, "token": token, "book": book}

def save_uploaded_file(file_storage) -> str:
    """Validate and save uploaded book file."""
    if not file_storage or not file_storage.filename:
        raise ValueError("No file uploaded.")
    filename = secure_filename(file_storage.filename)
    if not filename.lower().endswith(('.pdf', '.epub', '.txt')):
        raise ValueError("Unsupported file type. Must be PDF, EPUB, or TXT.")
    dest = os.path.join(UPLOAD_DIR, f"{int(time.time())}_{filename}")
    file_storage.save(dest)
    log_action("upload", filename)
    return dest

# === ASYNC WRAPPERS ===
async def async_get_book(book_id: str):
    return await asyncio.to_thread(get_book, book_id)

async def async_add_book(metadata: Dict[str, Any]):
    return await asyncio.to_thread(add_book, metadata)

# === EXTRAS ===
def get_most_viewed(limit: int = 10) -> List[Dict[str, Any]]:
    """Return top N most-viewed books."""
    data = _read()
    views = data.get("views", {})
    sorted_books = sorted(views.items(), key=lambda x: x[1], reverse=True)[:limit]
    return [data["books"][bid] for bid, _ in sorted_books if bid in data["books"]]

def bootstrap_sample():
    """Create a demo book if library is empty."""
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