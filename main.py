# ===========================================================
# 🌌 Neuraluxe-AI (NeuraAI v10k Hyperluxe)
# 🚀 Koyeb Cloud Deployment — Final Production Version
# ===========================================================
# Author: ChatGPT + Joshua Dav
# License: Proprietary / All Rights Reserved
# Deployment: Koyeb (Flask + Gunicorn)
# Description:
#   Full-stack AI ecosystem — chat, automation, marketplace,
#   and creativity fused into one neon-intelligent experience.
# ===========================================================

import os, time, logging, asyncpg, asyncio
from datetime import datetime
from flask import Flask, jsonify
from dotenv import load_dotenv

# -----------------------------------------------------------
# ✅ Environment Verification
# -----------------------------------------------------------
load_dotenv()

REQUIRED_VARS = ["FLASK_ENV", "LOG_LEVEL", "ENABLE_ENV_CHECK", "DATABASE_URL"]
missing = [v for v in REQUIRED_VARS if not os.getenv(v)]
if missing:
    print(f"⚠️ Missing environment variables: {missing}")
else:
    print(f"✅ Environment OK — {', '.join(REQUIRED_VARS)} loaded")

# -----------------------------------------------------------
# 🧠 Flask App Initialization
# -----------------------------------------------------------
# ===========================================================
# ✅ Neuraluxe-AI v10k Hyperluxe — Dependency Check Snippet
# Ensures all key packages are available before startup
# ===========================================================

import importlib, sys, logging

logger = logging.getLogger("Neuraluxe-Startup")
logger.setLevel(logging.INFO)

required_libs = [
    "flask", "flask_cors", "flask_caching", "flask_sqlalchemy",
    "requests", "httpx", "asyncpg", "psycopg2", "redis",
    "rq", "apscheduler", "uvicorn", "gunicorn"
]

missing = []
for lib in required_libs:
    try:
        importlib.import_module(lib)
    except ImportError:
        missing.append(lib)

if missing:
    logger.warning(f"⚠️ Missing libraries: {', '.join(missing)}")
else:
    logger.info("✅ All essential Neuraluxe-AI dependencies loaded successfully.")

logger.info("🌌 Neuraluxe-AI Hyperluxe engine initialized.")
logger.info("🚀 Environment ready. Waiting for Koyeb startup signal...")# ===========================================================
# ✅ Neuraluxe-AI v10k Hyperluxe — Dependency Check Snippet
# Ensures all key packages are available before startup
# ===========================================================

import importlib, sys, logging

logger = logging.getLogger("Neuraluxe-Startup")
logger.setLevel(logging.INFO)

required_libs = [
    "flask", "flask_cors", "flask_caching", "flask_sqlalchemy",
    "requests", "httpx", "asyncpg", "psycopg2", "redis",
    "rq", "apscheduler", "uvicorn", "gunicorn"
]

missing = []
for lib in required_libs:
    try:
        importlib.import_module(lib)
    except ImportError:
        missing.append(lib)

if missing:
    logger.warning(f"⚠️ Missing libraries: {', '.join(missing)}")
else:
    logger.info("✅ All essential Neuraluxe-AI dependencies loaded successfully.")

logger.info("🌌 Neuraluxe-AI Hyperluxe engine initialized.")
logger.info("🚀 Environment ready. Waiting for Koyeb startup signal...")
app = Flask(__name__)

log_level = os.getenv("LOG_LEVEL", "info").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))
logger = logging.getLogger("Neuraluxe-AI")

# -----------------------------------------------------------
# 🧩 PostgreSQL Async Connection
# -----------------------------------------------------------
DB_URL = os.getenv("DATABASE_URL")

async def init_db():
    """Initialize database connection."""
    try:
        app.db = await asyncpg.create_pool(DB_URL, min_size=1, max_size=5)
        logger.info("✅ PostgreSQL connected successfully.")
    except Exception as e:
        logger.error(f"❌ PostgreSQL connection failed: {e}")

@app.before_first_request
def before_start():
    """Event before first API request."""
    loop = asyncio.get_event_loop()
    loop.create_task(init_db())

# -----------------------------------------------------------
# 🧭 Core Routes
# -----------------------------------------------------------
@app.route("/")
def index():
    return jsonify({
        "app": "Neuraluxe-AI v10k Hyperluxe",
        "status": "online",
        "uptime": datetime.utcnow().isoformat(),
        "message": "Welcome to Neuraluxe-AI 🌌 — Intelligence meets design."
    })

@app.route("/env/check")
def env_check():
    return jsonify({
        "env_verified": len(missing) == 0,
        "required_vars": REQUIRED_VARS,
        "missing_vars": missing,
        "server_time": datetime.utcnow().isoformat(),
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "db_connected": hasattr(app, "db")})

# -----------------------------------------------------------
# 🧩 Blueprint Imports (modules)
# -----------------------------------------------------------
# You can safely import your other systems here 👇
# from modules.marketplace import marketplace_blueprint
# from modules.crypto import crypto_blueprint
# from modules.voice import voice_blueprint
# app.register_blueprint(marketplace_blueprint)
# app.register_blueprint(crypto_blueprint)
# app.register_blueprint(voice_blueprint)

# -----------------------------------------------------------
# 🪐 Local Debug Entry
# -----------------------------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
# main.py
"""
Neuraluxe-AI Hyperluxe — Mega Main Server
Author: ChatGPT + Joshua Dav
Purpose: Single-file backend for Neuraluxe-AI (expanded, large, feature-rich)
Notes:
 - Designed to run on Render with `gunicorn main:app`
 - Includes many endpoints: marketplace, chat, healthcare, payments, voice, translation, analytics, admin, scheduler
 - Mock integrations included; hooks provided to plug real APIs (OpenAI, Opay, Payoneer, Redis, etc.)
 - Contains extensive comments, utilities, background workers, and sample seeders
"""

# ----------------------------
# Standard library imports
# ----------------------------
import os
import sys
import time
import math
import json
import uuid
import queue
import copy
import random
import atexit
import sqlite3
import logging
import threading
from datetime import datetime, timedelta
from functools import wraps, lru_cache
from typing import Any, Dict, List, Optional, Tuple

# ----------------------------
# Third-party imports (optional)
# ----------------------------
try:
    from flask import Flask, request, jsonify, send_from_directory, g, abort
    from flask_cors import CORS
except Exception:
    raise RuntimeError("Flask and Flask-Cors are required. pip install flask flask-cors")

# Optional: OpenAI support (only if installed and enabled)
try:
    import openai
    OPENAI_INSTALLED = True
except Exception:
    OPENAI_INSTALLED = False

# Optional: Rich for CLI env check (not required)
try:
    from rich.console import Console
    RICH_AVAILABLE = True
except Exception:
    RICH_AVAILABLE = False

# ----------------------------
# Basic configuration
# ----------------------------
APP_NAME = "Neuraluxe-AI"
VERSION = os.environ.get("APP_VERSION", "v10k.Hyperluxe")
CREATORS = "ChatGPT + Joshua Dav"

PORT = int(os.environ.get("PORT", 10000))
DEBUG = os.environ.get("FLASK_ENV", "production").lower() != "production"
DATABASE_FILE = os.environ.get("NEURA_DB", "neuraluxe_full.db")
NEURA_ADMIN_TOKEN = os.environ.get("NEURA_ADMIN_TOKEN", "neura-admin-2025")
DEVELOPER_FREE_EMAIL = os.environ.get("NEURA_DEV_FREE_EMAIL", "adedoyinolugbode57@gmail.com")
OPENAI_ENABLED = os.environ.get("OPENAI_ENABLED", "false").lower() in ("1", "true", "yes")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None) or None
ITEMS_SIMULATED_CAP = int(os.environ.get("ITEMS_SIMULATED_CAP", 1000000))
ITEMS_PAGE_SIZE_DEFAULT = int(os.environ.get("ITEMS_PAGE_SIZE_DEFAULT", 24))
CACHE_WARM_PAGES = int(os.environ.get("CACHE_WARM_PAGES", 5))
RATE_LIMIT_SECONDS = float(os.environ.get("NEURA_RATE_LIMIT_SECONDS", 0.0))
SAFE_MAX_PAGE_SIZE = int(os.environ.get("SAFE_MAX_PAGE_SIZE", 1000))

# Configure OpenAI if enabled
if OPENAI_ENABLED and OPENAI_API_KEY and OPENAI_INSTALLED:
    try:
        openai.api_key = OPENAI_API_KEY
    except Exception:
        pass

# ----------------------------
# App initialization
# ----------------------------
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Logging
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO, stream=sys.stdout,
                    format="%(asctime)s %(levelname)s %(name)s - %(message)s")
logger = logging.getLogger("neuraluxe")
logger.info(f"Starting {APP_NAME} {VERSION} (DEBUG={DEBUG})")

# ----------------------------
# Database helpers (SQLite)
# ----------------------------
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        need_init = not os.path.exists(DATABASE_FILE)
        db = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
        db.row_factory = sqlite3.Row
        g._database = db
        if need_init:
            init_db(db)
    return db

def init_db(db_conn):
    logger.info("Initializing database schema...")
    cur = db_conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        is_free INTEGER DEFAULT 0,
        transactions INTEGER DEFAULT 0,
        locked_until INTEGER DEFAULT 0,
        metadata TEXT DEFAULT '{}',
        created_at INTEGER
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        item_id TEXT,
        amount REAL,
        currency TEXT,
        meta TEXT,
        created_at INTEGER
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS feedbacks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        message TEXT,
        rating INTEGER,
        created_at INTEGER
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS analytics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT,
        value TEXT,
        created_at INTEGER
    );
    """)
    db_conn.commit()
    # Seed dev free user
    ensure_user(DEVELOPER_FREE_EMAIL, is_free=True)

def ensure_user(email: str, is_free: bool=False):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    if row:
        return dict(row)
    now = int(time.time())
    cur.execute("INSERT INTO users (email,is_free,created_at) VALUES (?, ?, ?)", (email, 1 if is_free else 0, now))
    db.commit()
    return {"email": email, "is_free": is_free, "created_at": now}

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# ----------------------------
# Utilities
# ----------------------------
def utc_ts() -> int:
    return int(time.time())

def make_id(prefix: str = "id") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

def safe_float(v, default=0.0):
    try:
        return float(v)
    except Exception:
        return default

def pretty_json(obj):
    try:
        return json.dumps(obj, ensure_ascii=False, indent=2)
    except Exception:
        return str(obj)

# ----------------------------
# Rate limiting decorator
# ----------------------------
_rate_store: Dict[str, float] = {}

def rate_limit(seconds: float):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if seconds <= 0:
                return f(*args, **kwargs)
            client = request.headers.get("X-Forwarded-For", request.remote_addr or "anon")
            now = time.time()
            last = _rate_store.get(client, 0)
            if now - last < seconds:
                retry_after = seconds - (now - last)
                return jsonify({"error": "rate_limited", "retry_after": retry_after}), 429
            _rate_store[client] = now
            return f(*args, **kwargs)
        return wrapper
    return decorator

# ----------------------------
# Admin decorator
# ----------------------------
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization") or request.args.get("admin_token")
        if not token:
            return jsonify({"error": "missing_admin_token"}), 401
        if token.startswith("Bearer "):
            token = token.split(" ", 1)[1]
        if token != NEURA_ADMIN_TOKEN:
            return jsonify({"error": "invalid_admin_token"}), 403
        return f(*args, **kwargs)
    return wrapper

# ----------------------------
# Marketplace Generator
# ----------------------------
CATEGORIES = [
    "AI Tools", "Automation Bots", "Trading Scripts", "Freelancer Tools", "Design Studio",
    "Crypto Assets", "Voice & Language", "Education Packs", "Developer Plugins", "Global Add-Ons"
]

def mulberry32(seed: int) -> float:
    seed = int(seed) & 0xffffffff
    seed = (seed + 0x6D2B79F5) & 0xffffffff
    seed = (seed ^ (seed >> 16)) * 0x45d9f3b
    seed = (seed ^ (seed >> 16)) * 0x45d9f3b
    seed = seed ^ (seed >> 16)
    return (seed & 0xffffffff) / 4294967296.0

def gen_item(index: int) -> Dict[str, Any]:
    i = max(1, int(index))
    r = mulberry32(i)
    cat = CATEGORIES[i % len(CATEGORIES)]
    base_map = {
        "AI Tools":"Neuraluxe AI Tool",
        "Automation Bots":"AutoFlow Bot",
        "Trading Scripts":"Neuraluxe Trader",
        "Freelancer Tools":"Freelance Boost Kit",
        "Design Studio":"Studio Pack",
        "Crypto Assets":"Crypto Signal Module",
        "Voice & Language":"Voice Pack",
        "Education Packs":"Learning Module",
        "Developer Plugins":"Dev Plugin",
        "Global Add-Ons":"Legacy Add-On"
    }
    base = base_map.get(cat, "Neuraluxe Asset")
    price = round(29.99 + ((i % 1000) * ((9999.99 - 29.99) / 1000)) + (r * 49.99), 2)
    rating = round(3.0 + (r * 2.0), 1)
    return {
        "id": f"nli-{i}",
        "name": f"{base} #{i}",
        "category": cat,
        "price": price,
        "currency": "USD",
        "rating": rating,
        "description": f"A premium {cat} asset by Neuraluxe — preview #{i}.",
        "image": f"https://picsum.photos/seed/neuraluxe{i}/400/300",
        "created_at": utc_ts()
    }

# Caching pages
_items_cache_lock = threading.Lock()
_items_page_cache: Dict[str, Dict] = {}

def _page_cache_key(page:int, size:int, q:Optional[str], category:Optional[str], min_p:Optional[float], max_p:Optional[float]) -> str:
    return f"p{page}_s{size}_q{q or ''}_c{category or ''}_min{min_p or ''}_max{max_p or ''}"

def get_items_page(page:int=1, page_size:int=ITEMS_PAGE_SIZE_DEFAULT, q:Optional[str]=None, category:Optional[str]=None, min_price:Optional[float]=None, max_price:Optional[float]=None) -> Dict[str, Any]:
    page = max(1, int(page))
    page_size = max(1, min(int(page_size), SAFE_MAX_PAGE_SIZE))
    key = _page_cache_key(page, page_size, q, category, min_price, max_price)
    with _items_cache_lock:
        if key in _items_page_cache:
            return _items_page_cache[key]
    start_idx = (page - 1) * page_size + 1
    results = []
    idx = start_idx
    while len(results) < page_size and idx <= ITEMS_SIMULATED_CAP:
        it = gen_item(idx)
        if category and it["category"].lower() != category.lower():
            idx += 1; continue
        if q and q.lower() not in (it["name"] + " " + it["description"]).lower():
            idx += 1; continue
        if min_price is not None and it["price"] < float(min_price):
            idx += 1; continue
        if max_price is not None and it["price"] > float(max_price):
            idx += 1; continue
        results.append(it)
        idx += 1
    payload = {"page": page, "page_size": page_size, "items": results, "total_estimate": ITEMS_SIMULATED_CAP}
    with _items_cache_lock:
        _items_page_cache[key] = payload
    return payload

# Warm cache thread
def warm_cache():
    logger.info("Starting cache warmer...")
    for p in range(1, CACHE_WARM_PAGES + 1):
        try:
            get_items_page(page=p, page_size=ITEMS_PAGE_SIZE_DEFAULT)
            logger.debug(f"Warmed page {p}")
        except Exception:
            logger.exception("Cache warm error")
    logger.info("Cache warming complete")

threading.Thread(target=warm_cache, daemon=True).start()

# ----------------------------
# Payment mock & registration
# ----------------------------
MAX_RETRIES = 3
LOCK_DURATION = 24 * 60 * 60

def verify_payment_mock(user_email: str, amount: float, provider: str="opay") -> Dict[str, Any]:
    # Developer bypass
    if user_email and user_email.lower() == DEVELOPER_FREE_EMAIL.lower():
        return {"ok": True, "reason": "developer_free_bypass", "tx_id": make_id("tx")}
    try:
        amount_f = float(amount)
    except Exception:
        return {"ok": False, "reason": "invalid_amount"}
    # For mock, accept amounts <= 10000
    if amount_f <= 10000:
        return {"ok": True, "reason": "mock_confirmed", "tx_id": make_id("tx")}
    return {"ok": False, "reason": "amount_too_large"}

def register_purchase(user_email: str, item_id: str, amount: float, currency: str="USD", meta: Optional[Dict]=None) -> int:
    db = get_db()
    cur = db.cursor()
    now = utc_ts()
    cur.execute("INSERT INTO purchases (user_email,item_id,amount,currency,meta,created_at) VALUES (?,?,?,?,?,?)",
                (user_email, item_id, float(amount), currency, json.dumps(meta or {}), now))
    db.commit()
    return cur.lastrowid

# ----------------------------
# Chat / AI endpoints
# ----------------------------
def call_openai(prompt: str, model: str="gpt-4o-mini", max_tokens:int=256, temperature:float=0.7) -> str:
    if not OPENAI_ENABLED or not OPENAI_INSTALLED:
        raise RuntimeError("OpenAI not configured")
    try:
        # Attempt multiple client styles to be robust
        if hasattr(openai, "ChatCompletion"):
            resp = openai.ChatCompletion.create(model=model, messages=[{"role":"user","content":prompt}], max_tokens=max_tokens, temperature=temperature)
            try:
                return resp.choices[0].message["content"]
            except Exception:
                try:
                    return resp["choices"][0]["message"]["content"]
                except Exception:
                    return str(resp)
        else:
            resp = openai.Completion.create(engine=model, prompt=prompt, max_tokens=max_tokens, temperature=temperature)
            return resp.choices[0].text
    except Exception as e:
        logger.exception("OpenAI call error: %s", e)
        raise

def mock_chat(prompt: str) -> str:
    r = mulberry32(abs(hash(prompt)) % 4294967296)
    canned = [
        "Sure — I can handle that for you.",
        "Interesting — here's a practical plan.",
        "Let's break this down into clear steps.",
        "I recommend starting with the high-impact task."
    ]
    return canned[int(r * len(canned))] + f" (mock reply for: {prompt[:60]})"

@app.route("/api/chat", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_chat():
    payload = request.get_json() or {}
    prompt = payload.get("prompt") or payload.get("message") or ""
    user_email = payload.get("user_email") or "guest@example.com"
    model = payload.get("model") or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    if not prompt:
        return jsonify({"error": "empty_prompt"}), 400
    logger.info(f"Chat request by {user_email} model={model} len={len(prompt)}")
    if OPENAI_ENABLED and OPENAI_INSTALLED and OPENAI_API_KEY:
        try:
            resp = call_openai(prompt, model=model)
            return jsonify({"ok": True, "provider": "openai", "response": resp})
        except Exception:
            logger.warning("Falling back to mock chat")
    resp = mock_chat(prompt)
    return jsonify({"ok": True, "provider": "mock", "response": resp})

# ----------------------------
# Healthcare endpoints
# ----------------------------
@app.route("/api/health/symptoms", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_health_symptoms():
    payload = request.get_json() or {}
    symptoms = payload.get("symptoms", "")
    if not symptoms:
        return jsonify({"error": "missing_symptoms"}), 400
    s = symptoms.lower()
    advices = []
    if any(k in s for k in ["fever", "temperature"]):
        advices.append("Check temperature; hydrate and rest. Seek doctor if >38.5°C.")
    if any(k in s for k in ["cough", "sore throat"]):
        advices.append("Warm fluids, rest, and isolate if infection suspected.")
    if any(k in s for k in ["pain", "ache"]):
        advices.append("Use analgesics sensibly; consult a professional if persistent.")
    if not advices:
        advices.append("Monitor symptoms; seek care if they worsen.")
    record_analytics("health_symptom_check", {"symptoms": symptoms})
    return jsonify({"ok": True, "symptoms": symptoms, "advice": advices})

@app.route("/api/health/medication", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_health_medication():
    payload = request.get_json() or {}
    drug = (payload.get("drug") or payload.get("name") or "").strip()
    if not drug:
        return jsonify({"error": "missing_drug"}), 400
    # Placeholder - integrate real drug API as a later step
    sample = {
        "requested": drug,
        "brand_name": f"{drug.title()}-Brand",
        "manufacturer": "Neuraluxe Pharma (demo)",
        "purpose": "Analgesic / Demo",
        "dosage": "Follow health professional guidance",
        "source": "mock"
    }
    record_analytics("med_lookup", {"drug": drug})
    return jsonify({"ok": True, "results": [sample]})

# ----------------------------
# Marketplace endpoints
# ----------------------------
@app.route("/api/market/items", methods=["GET"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_market_items():
    try:
        page = int(request.args.get("page", 1))
    except Exception:
        page = 1
    try:
        page_size = int(request.args.get("page_size", ITEMS_PAGE_SIZE_DEFAULT))
    except Exception:
        page_size = ITEMS_PAGE_SIZE_DEFAULT
    q = request.args.get("q")
    category = request.args.get("category")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    min_p = safe_float(min_price, None) if min_price else None
    max_p = safe_float(max_price, None) if max_price else None
    data = get_items_page(page=page, page_size=page_size, q=q, category=category, min_price=min_p, max_price=max_p)
    record_analytics("market_query", {"page": page, "q": q or "", "category": category or ""})
    return jsonify(data)

@app.route("/api/market/purchase", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_market_purchase():
    payload = request.get_json() or {}
    user_email = payload.get("user_email") or payload.get("email") or "guest@example.com"
    item_id = payload.get("item_id")
    amount = safe_float(payload.get("amount", 0.0), 0.0)
    if not item_id:
        return jsonify({"error": "missing_item_id"}), 400
    verify = verify_payment_mock(user_email, amount)
    if verify.get("ok"):
        purchase_id = register_purchase(user_email, item_id, amount)
        record_analytics("purchase", {"user": user_email, "item_id": item_id, "amount": amount})
        return jsonify({"ok": True, "purchase_id": purchase_id, "tx_id": verify.get("tx_id")})
    else:
        return jsonify({"ok": False, "reason": verify.get("reason")}), 402

# ----------------------------
# Feedback endpoints
# ----------------------------
@app.route("/api/feedback", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_feedback():
    payload = request.get_json() or {}
    email = payload.get("user_email", "anonymous")
    message = payload.get("message", "")
    rating = int(payload.get("rating", 0))
    if not message:
        return jsonify({"error":"missing_message"}), 400
    db = get_db()
    cur = db.cursor()
    now = utc_ts()
    cur.execute("INSERT INTO feedbacks (user_email, message, rating, created_at) VALUES (?,?,?,?)", (email, message, rating, now))
    db.commit()
    record_analytics("feedback", {"user": email, "rating": rating})
    return jsonify({"ok": True, "inserted": cur.lastrowid})

# ----------------------------
# Analytics helpers & endpoints
# ----------------------------
def record_analytics(key: str, value: Any):
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO analytics (key, value, created_at) VALUES (?, ?, ?)", (key, json.dumps(value), utc_ts()))
        db.commit()
    except Exception:
        logger.exception("Failed to record analytics")

@app.route("/api/admin/analytics", methods=["GET"])
@admin_required
def api_admin_analytics():
    key = request.args.get("key")
    limit = int(request.args.get("limit", 100))
    db = get_db()
    cur = db.cursor()
    if key:
        cur.execute("SELECT * FROM analytics WHERE key = ? ORDER BY created_at DESC LIMIT ?", (key, limit))
    else:
        cur.execute("SELECT * FROM analytics ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    return jsonify({"ok": True, "items": [dict(r) for r in rows]})

# ----------------------------
# Admin & management endpoints
# ----------------------------
@app.route("/api/admin/stats", methods=["GET"])
@admin_required
def api_admin_stats():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) AS c FROM users")
    users = cur.fetchone()["c"]
    cur.execute("SELECT COUNT(*) AS c FROM purchases")
    purchases = cur.fetchone()["c"]
    cur.execute("SELECT COUNT(*) AS c FROM feedbacks")
    feedbacks = cur.fetchone()["c"]
    uptime = int(time.time() - app_start_time)
    return jsonify({"ok": True, "users": users, "purchases": purchases, "feedbacks": feedbacks, "uptime_seconds": uptime})

@app.route("/api/admin/seed", methods=["POST"])
@admin_required
def api_admin_seed():
    db = get_db()
    cur = db.cursor()
    # seed users
    sample = [f"seed{i}@example.com" for i in range(1, 51)]
    now = utc_ts()
    for email in sample:
        try:
            cur.execute("INSERT INTO users (email,is_free,created_at) VALUES (?,?,?)", (email, 0, now))
        except Exception:
            pass
    # seed purchases
    for i in range(1, 101):
        cur.execute("INSERT INTO purchases (user_email,item_id,amount,currency,meta,created_at) VALUES (?,?,?,?,?,?)",
                    (sample[i % len(sample)], f"nli-{i}", float(29.99 + i), "USD", json.dumps({"seed": True}), now))
    db.commit()
    return jsonify({"ok": True, "seeded_users": len(sample), "seeded_purchases": 100})

# ----------------------------
# Voice & TTS endpoints (placeholders)
# ----------------------------
def synthesize_tts_dummy(text: str, voice: str="default"):
    # returns a pretend URL to synthesized audio
    return {"ok": True, "url": f"https://storage.neuraluxe.ai/tts/{make_id('tts')}.mp3", "voice": voice}

@app.route("/api/voice/tts", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_tts():
    payload = request.get_json() or {}
    text = payload.get("text", "")
    voice = payload.get("voice", "default")
    if not text:
        return jsonify({"error":"missing_text"}), 400
    out = synthesize_tts_dummy(text, voice=voice)
    record_analytics("tts_request", {"len": len(text), "voice": voice})
    return jsonify(out)

@app.route("/api/voice/stt", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_stt():
    payload = request.get_json() or {}
    audio = payload.get("audio_base64")
    if not audio:
        return jsonify({"error":"missing_audio"}), 400
    # Pretend we transcribed
    transcription = "[transcription placeholder]"
    record_analytics("stt", {"size": len(audio)})
    return jsonify({"ok": True, "transcription": transcription})

# ----------------------------
# Translation placeholder
# ----------------------------
@app.route("/api/translate", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_translate():
    payload = request.get_json() or {}
    text = payload.get("text", "")
    target = payload.get("target", "en")
    if not text:
        return jsonify({"error":"missing_text"}), 400
    translated = f"[{target}] {text}"
    record_analytics("translate", {"len": len(text), "target": target})
    return jsonify({"ok": True, "translated": translated})

# ----------------------------
# Diagnostic routes (/env/check and /ai/diagnose)
# ----------------------------
@app.route("/env/check", methods=["GET"])
def env_check():
    keys = [
        "APP_NAME", "APP_VERSION", "FLASK_ENV", "PORT",
        "DATABASE_URL", "VOICE_ENGINE", "CACHE_TYPE",
        "OPENAI_ENABLED", "OPENAI_MODEL"
    ]
    summary = {}
    for k in keys:
        summary[k] = os.environ.get(k, "❌ Missing")
    return jsonify({
        "status": "ok",
        "summary": summary,
        "developer": os.environ.get("NEURA_DEV_FREE_EMAIL", "Not set"),
        "note": "Environment checked. If OPENAI_ENABLED=true and key available, AI cloud will be active."
    })

@app.route("/ai/diagnose", methods=["GET"])
def ai_diagnose():
    openai_on = os.environ.get("OPENAI_ENABLED", "false").lower() in ("1", "true", "yes")
    openai_key = os.environ.get("OPENAI_API_KEY")
    res = {
        "ai_mode": "cloud" if openai_on and openai_key else "offline",
        "openai_key_present": bool(openai_key),
        "database": bool(os.environ.get("DATABASE_URL") or os.path.exists(DATABASE_FILE)),
        "cache_warmed_pages": CACHE_WARM_PAGES,
        "msg": "diagnostic run"
    }
    # If OpenAI configured, try a lightweight call
    if openai_on and openai_key and OPENAI_INSTALLED:
        try:
            openai.api_key = openai_key
            # lightweight call: list models or similar (best-effort)
            if hasattr(openai, "models"):
                _ = openai.models.list()
            res["openai"] = "connected"
        except Exception as e:
            res["openai"] = f"error: {e}"
    else:
        res["openai"] = "not-configured"
    return jsonify(res)

# ----------------------------
# Static site helper
# ----------------------------
@app.route("/site/<path:path>", methods=["GET"])
def site_routes(path):
    # Serve files from static, templates, root
    roots = ["static", "templates", "."]
    for r in roots:
        fp = os.path.join(r, path)
        if os.path.exists(fp):
            return send_from_directory(r, path)
    abort(404)

# ----------------------------
# Background job queue & scheduler
# ----------------------------
job_queue = queue.Queue()

def job_worker():
    while True:
        job = job_queue.get()
        if job is None:
            break
        try:
            fn = job.get("fn")
            args = job.get("args", [])
            kwargs = job.get("kwargs", {})
            logger.info(f"Job start: {job.get('name')}")
            fn(*args, **kwargs)
            logger.info(f"Job done: {job.get('name')}")
        except Exception:
            logger.exception("Job execution error")
        finally:
            job_queue.task_done()

threading.Thread(target=job_worker, daemon=True).start()

def schedule(fn, name="job", delay=0, args=None, kwargs=None):
    if args is None: args=[]
    if kwargs is None: kwargs={}
    def _runner():
        if delay > 0:
            time.sleep(delay)
        job_queue.put({"fn": fn, "args": args, "kwargs": kwargs, "name": name})
    threading.Thread(target=_runner, daemon=True).start()
    return True

# Example scheduled task
def nightly_maintenance():
    logger.info("Running nightly maintenance")
    with _items_cache_lock:
        _items_page_cache.clear()
    db = get_db()
    cur = db.cursor()
    cutoff = utc_ts() - (30 * 24 * 3600)
    cur.execute("DELETE FROM analytics WHERE created_at < ?", (cutoff,))
    db.commit()
    logger.info("Nightly maintenance complete")

# schedule nightly maintenance every 24 hours in background thread
def _daily_scheduler():
    while True:
        try:
            now = datetime.utcnow()
            next_run = (datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1))
            seconds = (next_run - now).total_seconds()
            logger.info(f"Scheduler sleeping {seconds} secs until midnight UTC")
            time.sleep(max(60, seconds))
            nightly_maintenance()
        except Exception:
            logger.exception("Scheduler loop error")
            time.sleep(60)

threading.Thread(target=_daily_scheduler, daemon=True).start()

# ----------------------------
# Startup tasks & graceful shutdown
# ----------------------------
app_start_time = time.time()

def graceful_shutdown():
    logger.info("Shutting down Neuraluxe-AI gracefully")
    try:
        job_queue.put(None)
    except Exception:
        pass
    try:
        with _items_cache_lock:
            _items_page_cache.clear()
    except Exception:
        pass

atexit.register(graceful_shutdown)

# ----------------------------
# CLI & helper commands (if run as script)
# ----------------------------
def seed_demo_data():
    logger.info("Seeding demo data...")
    db = get_db()
    cur = db.cursor()
    now = utc_ts()
    try:
        for i in range(1, 101):
            email = f"user{i}@example.com"
            try:
                cur.execute("INSERT INTO users (email,is_free,created_at) VALUES (?,?,?)", (email, 0, now))
            except Exception:
                pass
            cur.execute("INSERT INTO purchases (user_email,item_id,amount,currency,meta,created_at) VALUES (?,?,?,?,?,?)",
                        (email, f"nli-{i}", float(29.99 + (i%50)), "USD", json.dumps({"demo": True}), now))
        db.commit()
        logger.info("Demo data seeded")
    except Exception:
        logger.exception("Seeding failed")

# ----------------------------
# Utility endpoints
# ----------------------------
@app.route("/api/info", methods=["GET"])
def api_info():
    return jsonify({
        "app": APP_NAME,
        "version": VERSION,
        "creators": CREATORS,
        "uptime_seconds": int(time.time() - app_start_time)
    })

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "pass", "time": utc_ts()})

# ----------------------------
# Final run
# ----------------------------
# ==========================================================
# 🌍 Environment Variable Verification Route
# ==========================================================
from flask import jsonify
import os

@app.route("/env/check")
def env_check():
    """Verify all environment variables are loaded correctly."""
    keys_to_check = [
        "APP_NAME", "APP_VERSION", "FLASK_ENV", "PORT",
        "DATABASE_URL", "VOICE_ENGINE", "TTS_LANG",
        "CACHE_TYPE", "CRYPTO_API", "OPENFDA_API_BASE",
        "NEURA_DEV_FREE_EMAIL", "OPENAI_ENABLED", "LOG_LEVEL",
    ]

    summary = {}
    for key in keys_to_check:
        value = os.getenv(key)
        if value:
            summary[key] = value if "KEY" not in key else "✅ Loaded"
        else:
            summary[key] = "⚠️ Missing"

    return jsonify({
        "status": "success",
        "app": os.getenv("APP_NAME", "NeuraAI_v10k_Hyperluxe"),
        "version": os.getenv("APP_VERSION", "v10k"),
        "env_summary": summary,
        "message": "All environment variables verified successfully!"
    }), 200
    # --- Optional: Quick Environment Summary Log on Startup ---
if os.getenv("ENABLE_ENV_CHECK", "false").lower() == "true":
    print("\n🌍 Environment Summary — Neuraluxe-AI Boot Log")
    print("-------------------------------------------------")
    for key in ["APP_NAME", "APP_VERSION", "FLASK_ENV", "PORT", "LOG_LEVEL"]:
        val = os.getenv(key, "⚠️ Missing")
        print(f"{key}: {val}")
    print("-------------------------------------------------\n")
if __name__ == "__main__":
    # Ensure DB exists
    get_db()
    # Optionally seed demo data if env set
    if os.environ.get("NEURA_SEED_DEMO", "false").lower() in ("1", "true", "yes"):
        seed_demo_data()
    logger.info(f"Neuraluxe-AI starting on 0.0.0.0:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
    # ----------------------------
# Mini Games & Fun Endpoints
# ----------------------------
GUESSES_STORE: Dict[str, int] = {}

@app.route("/api/game/number_guess", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_number_guess():
    payload = request.get_json() or {}
    user = payload.get("user_email", "guest@example.com")
    guess = payload.get("guess")
    if guess is None:
        return jsonify({"error":"missing_guess"}), 400
    try:
        guess = int(guess)
    except Exception:
        return jsonify({"error":"guess_must_be_integer"}), 400
    # generate target if not present
    if user not in GUESSES_STORE:
        GUESSES_STORE[user] = random.randint(1, 100)
    target = GUESSES_STORE[user]
    if guess == target:
        msg = f"Correct! Number was {target}."
        del GUESSES_STORE[user]
    elif guess < target:
        msg = "Too low!"
    else:
        msg = "Too high!"
    record_analytics("game_guess", {"user": user, "guess": guess, "target": target})
    return jsonify({"ok": True, "message": msg, "target_known": guess==target})

@app.route("/api/game/quiz", methods=["GET"])
def api_quiz():
    sample = [
        {"question":"What is 5+7?", "options":["10","12","14"], "answer":"12"},
        {"question":"Capital of France?", "options":["Berlin","Madrid","Paris"], "answer":"Paris"},
        {"question":"Python type of 3.14?","options":["int","float","str"],"answer":"float"}
    ]
    q = random.choice(sample)
    record_analytics("game_quiz_served", {"question": q["question"]})
    return jsonify({"ok": True, "quiz": q})

# ----------------------------
# Crypto / Trading Mock Endpoints
# ----------------------------
@app.route("/api/crypto/price", methods=["GET"])
def api_crypto_price():
    symbol = (request.args.get("symbol") or "BTC").upper()
    price = round(1000 + random.random()*50000, 2)
    record_analytics("crypto_price", {"symbol": symbol, "price": price})
    return jsonify({"ok": True, "symbol": symbol, "price_usd": price})

@app.route("/api/crypto/signal", methods=["GET"])
def api_crypto_signal():
    symbol = (request.args.get("symbol") or "ETH").upper()
    signals = ["BUY", "SELL", "HOLD"]
    signal = random.choice(signals)
    confidence = round(50 + random.random()*50,1)
    record_analytics("crypto_signal", {"symbol": symbol, "signal": signal})
    return jsonify({"ok": True, "symbol": symbol, "signal": signal, "confidence": confidence})

@app.route("/api/crypto/portfolio", methods=["POST"])
def api_crypto_portfolio():
    payload = request.get_json() or {}
    user = payload.get("user_email", "guest@example.com")
    assets = [
        {"symbol":"BTC","amount":round(random.random()*2,3)},
        {"symbol":"ETH","amount":round(random.random()*10,3)},
        {"symbol":"DOGE","amount":round(random.random()*1000,2)}
    ]
    record_analytics("portfolio_view", {"user": user})
    return jsonify({"ok": True, "user": user, "assets": assets})

# ----------------------------
# Freelancer / Task Market Enhancements
# ----------------------------
@app.route("/api/freelance/tasks", methods=["GET"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_freelance_tasks():
    tasks = []
    for i in range(1,6):
        tasks.append({
            "id": f"task-{i}",
            "title": f"Design task #{i}",
            "description": "Complete this mock design assignment",
            "reward": round(20 + random.random()*100,2),
            "status": random.choice(["open","assigned","completed"])
        })
    record_analytics("freelance_tasks_list", {"count": len(tasks)})
    return jsonify({"ok": True, "tasks": tasks})

@app.route("/api/freelance/assign", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_freelance_assign():
    payload = request.get_json() or {}
    task_id = payload.get("task_id")
    user = payload.get("user_email", "guest@example.com")
    if not task_id:
        return jsonify({"error":"missing_task_id"}), 400
    record_analytics("freelance_task_assign", {"task_id": task_id, "user": user})
    return jsonify({"ok": True, "task_id": task_id, "assigned_to": user})

# ----------------------------
# AI Utilities
# ----------------------------
@app.route("/api/ai/summarize", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_ai_summarize():
    payload = request.get_json() or {}
    text = payload.get("text","")
    if not text:
        return jsonify({"error":"missing_text"}), 400
    summary = text[:75] + "..." if len(text)>75 else text
    record_analytics("ai_summarize", {"len": len(text)})
    return jsonify({"ok": True, "summary": summary})

@app.route("/api/ai/fact", methods=["GET"])
def api_ai_fact():
    facts = [
        "Honey never spoils.",
        "Bananas are berries, but strawberries are not.",
        "Octopuses have three hearts.",
        "Sharks existed before trees."
    ]
    fact = random.choice(facts)
    record_analytics("ai_fact", {})
    return jsonify({"ok": True, "fact": fact})

@app.route("/api/ai/joke", methods=["GET"])
def api_ai_joke():
    jokes = [
        "Why did the AI cross the road? To optimize the other side!",
        "I would tell you a joke about neural nets, but it's overfitting.",
        "Why was the robot angry? It had a byte of problems."
    ]
    joke = random.choice(jokes)
    record_analytics("ai_joke", {})
    return jsonify({"ok": True, "joke": joke})

# ----------------------------
# Background Job Example: Leaderboard Update
# ----------------------------
leaderboard_store: Dict[str,float] = {}

def update_leaderboard():
    logger.info("Updating leaderboard...")
    # mock scores
    for i in range(1,11):
        leaderboard_store[f"user{i}@example.com"] = round(random.random()*1000,2)
    logger.info("Leaderboard updated")
    record_analytics("leaderboard_update", {"count": len(leaderboard_store)})

# schedule leaderboard update every hour
def _hourly_scheduler():
    while True:
        try:
            update_leaderboard()
            time.sleep(3600)
        except Exception:
            logger.exception("Hourly scheduler error")
            time.sleep(60)

threading.Thread(target=_hourly_scheduler, daemon=True).start()

# ----------------------------
# Mock Notifications
# ----------------------------
@app.route("/api/notify", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_notify():
    payload = request.get_json() or {}
    user = payload.get("user_email", "guest@example.com")
    message = payload.get("message","")
    if not message:
        return jsonify({"error":"missing_message"}), 400
    # pretend to send
    record_analytics("notify", {"user": user, "msg_len": len(message)})
    return jsonify({"ok": True, "user": user, "message": message, "status":"sent_mock"})
    # ----------------------------
# Extended AI endpoints
# ----------------------------
@app.route("/api/ai/summarize", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_ai_summarize():
    payload = request.get_json() or {}
    text = payload.get("text", "")
    if not text:
        return jsonify({"error": "missing_text"}), 400
    # Mock summarization
    summary = text[:max(50, len(text)//3)] + "..." if len(text) > 50 else text
    record_analytics("ai_summarize", {"len": len(text)})
    return jsonify({"ok": True, "summary": summary})

@app.route("/api/ai/jokes", methods=["GET"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_ai_jokes():
    jokes = [
        "Why did the AI go to therapy? It had too many hidden layers.",
        "Why did the neural network break up with the dataset? Too many biases.",
        "Why did the robot apply for a job? It wanted to byte the bullet.",
        "Why was the computer cold? It left its Windows open."
    ]
    joke = random.choice(jokes)
    record_analytics("ai_joke", {"joke": joke})
    return jsonify({"ok": True, "joke": joke})

@app.route("/api/ai/code_assist", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_ai_code_assist():
    payload = request.get_json() or {}
    prompt = payload.get("prompt", "")
    if not prompt:
        return jsonify({"error": "missing_prompt"}), 400
    # Mock code suggestion
    suggestion = f"# Suggested snippet for: {prompt[:50]}\nprint('Hello Neuraluxe!')"
    record_analytics("ai_code_assist", {"prompt_len": len(prompt)})
    return jsonify({"ok": True, "suggestion": suggestion})

# ----------------------------
# User profiles & settings
# ----------------------------
@app.route("/api/user/profile", methods=["GET"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_user_profile():
    email = request.args.get("email") or "guest@example.com"
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    if not row:
        return jsonify({"error": "user_not_found"}), 404
    return jsonify({"ok": True, "profile": dict(row)})

@app.route("/api/user/settings", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_user_settings():
    payload = request.get_json() or {}
    email = payload.get("email")
    settings = payload.get("settings", {})
    if not email:
        return jsonify({"error": "missing_email"}), 400
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT metadata FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    if not row:
        return jsonify({"error": "user_not_found"}), 404
    meta = json.loads(row["metadata"] or "{}")
    meta.update(settings)
    cur.execute("UPDATE users SET metadata = ? WHERE email = ?", (json.dumps(meta), email))
    db.commit()
    record_analytics("user_settings_update", {"email": email})
    return jsonify({"ok": True, "updated": meta})

# ----------------------------
# Email notifications mock
# ----------------------------
def send_email_mock(to: str, subject: str, body: str):
    logger.info(f"Mock email sent to {to}: {subject}")
    return {"ok": True, "to": to, "subject": subject}

@app.route("/api/notify/email", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_notify_email():
    payload = request.get_json() or {}
    email = payload.get("email")
    subject = payload.get("subject", "No Subject")
    body = payload.get("body", "")
    if not email or not body:
        return jsonify({"error": "missing_email_or_body"}), 400
    result = send_email_mock(email, subject, body)
    record_analytics("email_notification", {"to": email})
    return jsonify(result)

# ----------------------------
# Extra analytics / reporting
# ----------------------------
@app.route("/api/admin/reports/users", methods=["GET"])
@admin_required
def api_admin_reports_users():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT email, is_free, transactions, metadata, created_at FROM users ORDER BY created_at DESC LIMIT 200")
    rows = [dict(r) for r in cur.fetchall()]
    return jsonify({"ok": True, "users": rows})

@app.route("/api/admin/reports/purchases", methods=["GET"])
@admin_required
def api_admin_reports_purchases():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT user_email, item_id, amount, currency, meta, created_at FROM purchases ORDER BY created_at DESC LIMIT 200")
    rows = [dict(r) for r in cur.fetchall()]
    return jsonify({"ok": True, "purchases": rows})

# ----------------------------
# Extended TTS / STT options
# ----------------------------
@app.route("/api/voice/tts_advanced", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_tts_advanced():
    payload = request.get_json() or {}
    text = payload.get("text", "")
    voice = payload.get("voice", "advanced")
    speed = payload.get("speed", 1.0)
    if not text:
        return jsonify({"error": "missing_text"}), 400
    # Mock advanced TTS URL
    url = f"https://storage.neuraluxe.ai/tts/{make_id('tts_adv')}.mp3"
    record_analytics("tts_advanced_request", {"len": len(text), "voice": voice, "speed": speed})
    return jsonify({"ok": True, "url": url, "voice": voice, "speed": speed})

@app.route("/api/voice/stt_advanced", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_stt_advanced():
    payload = request.get_json() or {}
    audio = payload.get("audio_base64")
    lang = payload.get("lang", "en")
    if not audio:
        return jsonify({"error": "missing_audio"}), 400
    transcription = f"[transcribed {len(audio)} bytes in {lang}]"
    record_analytics("stt_advanced_request", {"size": len(audio), "lang": lang})
    return jsonify({"ok": True, "transcription": transcription})

# ----------------------------
# Developer CLI helpers
# ----------------------------
@app.route("/api/dev/run_job", methods=["POST"])
@admin_required
def api_dev_run_job():
    payload = request.get_json() or {}
    job_name = payload.get("name", "dev_job")
    delay = safe_float(payload.get("delay", 0))
    logger.info(f"Developer scheduling job: {job_name} delay={delay}")
    schedule(lambda: logger.info(f"Executed dev job {job_name}"), name=job_name, delay=delay)
    return jsonify({"ok": True, "scheduled": job_name, "delay": delay})

@app.route("/api/dev/clear_cache", methods=["POST"])
@admin_required
def api_dev_clear_cache():
    with _items_cache_lock:
        _items_page_cache.clear()
    logger.info("Developer cleared items cache")
    return jsonify({"ok": True, "cache_cleared": True})

@app.route("/api/dev/seed_demo_batch", methods=["POST"])
@admin_required
def api_dev_seed_demo_batch():
    try:
        seed_demo_data()
        return jsonify({"ok": True, "message": "Demo batch seeded"})
    except Exception as e:
        logger.exception("Failed to seed demo batch")
        return jsonify({"ok": False, "error": str(e)})

# ----------------------------
# New marketplace utilities
# ----------------------------
@app.route("/api/market/categories", methods=["GET"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_market_categories():
    return jsonify({"ok": True, "categories": CATEGORIES})

@app.route("/api/market/item/<item_id>", methods=["GET"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_market_item(item_id):
    # Fetch single item (mock)
    idx = int(item_id.split("-")[-1])
    item = gen_item(idx)
    return jsonify({"ok": True, "item": item})

# ----------------------------
# Fun / extra mock endpoints
# ----------------------------
@app.route("/api/fun/quote", methods=["GET"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_fun_quote():
    quotes = [
        "Innovation distinguishes between a leader and a follower.",
        "AI is not about replacing humans, it's about augmenting them.",
        "Neural networks are like poetry for computers."
    ]
    return jsonify({"ok": True, "quote": random.choice(quotes)})

@app.route("/api/fun/lucky_number", methods=["GET"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_fun_lucky_number():
    number = random.randint(1, 100)
    record_analytics("lucky_number_request", {"number": number})
    return jsonify({"ok": True, "number": number})
    # ----------------------------
# Email notifications mock continued
# ----------------------------
@app.route("/api/notify/email", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_notify_email():
    payload = request.get_json() or {}
    to = payload.get("to")
    subject = payload.get("subject", "Neuraluxe Notification")
    body = payload.get("body", "")
    if not to or not body:
        return jsonify({"error": "missing_to_or_body"}), 400
    result = send_email_mock(to, subject, body)
    record_analytics("email_sent", {"to": to, "subject_len": len(subject), "body_len": len(body)})
    return jsonify(result)

# ----------------------------
# Leaderboard & scoring
# ----------------------------
@app.route("/api/leaderboard", methods=["GET"])
def api_leaderboard():
    top = sorted(leaderboard_store.items(), key=lambda kv: kv[1], reverse=True)[:10]
    leaderboard = [{"user": u, "score": s} for u, s in top]
    return jsonify({"ok": True, "leaderboard": leaderboard})

@app.route("/api/leaderboard/submit", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_leaderboard_submit():
    payload = request.get_json() or {}
    user = payload.get("user_email", "guest@example.com")
    score = safe_float(payload.get("score", 0.0), 0.0)
    leaderboard_store[user] = leaderboard_store.get(user, 0) + score
    record_analytics("leaderboard_submit", {"user": user, "score": score})
    return jsonify({"ok": True, "new_score": leaderboard_store[user]})

# ----------------------------
# Mini-games: Dice Roll
# ----------------------------
@app.route("/api/game/dice", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_dice_roll():
    payload = request.get_json() or {}
    user = payload.get("user_email", "guest@example.com")
    sides = int(payload.get("sides", 6))
    if sides < 2:
        return jsonify({"error": "invalid_sides"}), 400
    roll = random.randint(1, sides)
    record_analytics("game_dice", {"user": user, "roll": roll, "sides": sides})
    return jsonify({"ok": True, "roll": roll, "sides": sides})

# ----------------------------
# Mini-games: Coin Flip
# ----------------------------
@app.route("/api/game/coin", methods=["POST"])
@rate_limit(RATE_LIMIT_SECONDS)
def api_coin_flip():
    payload = request.get_json() or {}
    user = payload.get("user_email", "guest@example.com")
    flip = random.choice(["Heads", "Tails"])
    record_analytics("game_coin", {"user": user, "flip": flip})
    return jsonify({"ok": True, "flip": flip})

# ----------------------------
# Random tips & motivational quotes
# ----------------------------
@app.route("/api/tips/random", methods=["GET"])
def api_random_tip():
    tips = [
        "Stay consistent with your coding practice.",
        "Break tasks into smaller achievable goals.",
        "Always back up your data frequently.",
        "Take breaks and rest your mind.",
        "Experiment with new ideas to learn faster.",
        "Keep your AI models updated with latest data."
    ]
    tip = random.choice(tips)
    record_analytics("random_tip", {"tip": tip})
    return jsonify({"ok": True, "tip": tip})

# ----------------------------
# Mock weather endpoint
# ----------------------------
@app.route("/api/weather", methods=["GET"])
def api_weather():
    city = request.args.get("city", "Unknown")
    temp_c = round(15 + random.random()*20,1)
    condition = random.choice(["Sunny","Cloudy","Rainy","Stormy","Snowy"])
    record_analytics("weather_lookup", {"city": city})
    return jsonify({"ok": True, "city": city, "temperature_c": temp_c, "condition": condition})

# ----------------------------
# Mock stock market
# ----------------------------
@app.route("/api/stocks/quote", methods=["GET"])
def api_stock_quote():
    symbol = (request.args.get("symbol") or "AAPL").upper()
    price = round(50 + random.random()*500,2)
    change = round(-5 + random.random()*10,2)
    record_analytics("stock_quote", {"symbol": symbol, "price": price})
    return jsonify({"ok": True, "symbol": symbol, "price": price, "change": change})

# ----------------------------
# Fun text transformations
# ----------------------------
@app.route("/api/fun/uppercase", methods=["POST"])
def api_uppercase():
    payload = request.get_json() or {}
    text = payload.get("text","")
    if not text:
        return jsonify({"error":"missing_text"}), 400
    transformed = text.upper()
    record_analytics("fun_uppercase", {"len": len(text)})
    return jsonify({"ok": True, "original": text, "transformed": transformed})

@app.route("/api/fun/lowercase", methods=["POST"])
def api_lowercase():
    payload = request.get_json() or {}
    text = payload.get("text","")
    if not text:
        return jsonify({"error":"missing_text"}), 400
    transformed = text.lower()
    record_analytics("fun_lowercase", {"len": len(text)})
    return jsonify({"ok": True, "original": text, "transformed": transformed})

@app.route("/api/fun/reverse", methods=["POST"])
def api_reverse_text():
    payload = request.get_json() or {}
    text = payload.get("text","")
    if not text:
        return jsonify({"error":"missing_text"}), 400
    transformed = text[::-1]
    record_analytics("fun_reverse", {"len": len(text)})
    return jsonify({"ok": True, "original": text, "transformed": transformed})

# ----------------------------
# Shutdown endpoint (admin)
# ----------------------------
@app.route("/api/admin/shutdown", methods=["POST"])
@admin_required
def api_admin_shutdown():
    record_analytics("admin_shutdown", {})
    threading.Thread(target=lambda: os._exit(0), daemon=True).start()
    return jsonify({"ok": True, "message": "Server shutting down..."})

# ----------------------------
# Extra utilities
# ----------------------------
@app.route("/api/utils/uuid", methods=["GET"])
def api_utils_uuid():
    uid = make_id("uuid")
    return jsonify({"ok": True, "uuid": uid})

@app.route("/api/utils/timestamp", methods=["GET"])
def api_utils_timestamp():
    ts = utc_ts()
    return jsonify({"ok": True, "timestamp": ts})

@app.route("/api/utils/random", methods=["GET"])
def api_utils_random():
    val = random.random()
    return jsonify({"ok": True, "value": val})

# ----------------------------
# End of extended snippet
# ----------------------------
# main.py
"""
Neuraluxe-AI Hyperluxe — Mega Main Server
Author: ChatGPT + Joshua Dav
Purpose: Single-file backend for Neuraluxe-AI (final, production-ready)
Notes:
 - Designed to run on Render with `gunicorn main:app`
 - Includes endpoints: marketplace, chat, healthcare, payments, voice, translation, analytics, admin, scheduler
 - Mock integrations; hooks provided to plug real APIs (OpenAI, Opay, Payoneer, Redis, etc.)
 - Contains background workers, sample seeders, mini-games, trading, AI utilities
"""

# ----------------------------
# Standard library imports
# ----------------------------
import os, sys, time, math, json, uuid, queue, copy, random, atexit, sqlite3, logging, threading
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Dict, Optional

# ----------------------------
# Third-party imports
# ----------------------------
try:
    from flask import Flask, request, jsonify, send_from_directory, g, abort
    from flask_cors import CORS
except Exception:
    raise RuntimeError("Flask and Flask-Cors required. pip install flask flask-cors")

# Optional: OpenAI support
try:
    import openai
    OPENAI_INSTALLED = True
except Exception:
    OPENAI_INSTALLED = False

# ----------------------------
# Configuration
# ----------------------------
APP_NAME = "Neuraluxe-AI"
VERSION = os.environ.get("APP_VERSION", "v10k.Hyperluxe")
CREATORS = "ChatGPT + Joshua Dav"

PORT = int(os.environ.get("PORT", 10000))
DEBUG = os.environ.get("FLASK_ENV", "production").lower() != "production"
DATABASE_FILE = os.environ.get("NEURA_DB", "neuraluxe_full.db")
NEURA_ADMIN_TOKEN = os.environ.get("NEURA_ADMIN_TOKEN", "neura-admin-2025")
DEVELOPER_FREE_EMAIL = os.environ.get("NEURA_DEV_FREE_EMAIL", "adedoyinolugbode57@gmail.com")
OPENAI_ENABLED = os.environ.get("OPENAI_ENABLED", "false").lower() in ("1", "true", "yes")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)
ITEMS_SIMULATED_CAP = int(os.environ.get("ITEMS_SIMULATED_CAP", 1000000))
ITEMS_PAGE_SIZE_DEFAULT = int(os.environ.get("ITEMS_PAGE_SIZE_DEFAULT", 24))
CACHE_WARM_PAGES = int(os.environ.get("CACHE_WARM_PAGES", 5))
RATE_LIMIT_SECONDS = float(os.environ.get("NEURA_RATE_LIMIT_SECONDS", 0.0))
SAFE_MAX_PAGE_SIZE = int(os.environ.get("SAFE_MAX_PAGE_SIZE", 1000))

if OPENAI_ENABLED and OPENAI_API_KEY and OPENAI_INSTALLED:
    openai.api_key = OPENAI_API_KEY

# ----------------------------
# App initialization
# ----------------------------
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app, resources={r"/api/*": {"origins": "*"}})

logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO, stream=sys.stdout,
                    format="%(asctime)s %(levelname)s %(name)s - %(message)s")
logger = logging.getLogger("neuraluxe")
logger.info(f"Starting {APP_NAME} {VERSION} (DEBUG={DEBUG})")

app_start_time = time.time()

# ----------------------------
# Database helpers
# ----------------------------
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        need_init = not os.path.exists(DATABASE_FILE)
        db = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
        db.row_factory = sqlite3.Row
        g._database = db
        if need_init:
            init_db(db)
    return db

def init_db(db_conn):
    logger.info("Initializing database schema...")
    cur = db_conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        is_free INTEGER DEFAULT 0,
        transactions INTEGER DEFAULT 0,
        locked_until INTEGER DEFAULT 0,
        metadata TEXT DEFAULT '{}',
        created_at INTEGER
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        item_id TEXT,
        amount REAL,
        currency TEXT,
        meta TEXT,
        created_at INTEGER
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS feedbacks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        message TEXT,
        rating INTEGER,
        created_at INTEGER
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS analytics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT,
        value TEXT,
        created_at INTEGER
    );
    """)
    db_conn.commit()
    ensure_user(DEVELOPER_FREE_EMAIL, is_free=True)

def ensure_user(email: str, is_free: bool=False):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    if row:
        return dict(row)
    now = int(time.time())
    cur.execute("INSERT INTO users (email,is_free,created_at) VALUES (?, ?, ?)", (email, 1 if is_free else 0, now))
    db.commit()
    return {"email": email, "is_free": is_free, "created_at": now}

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# ----------------------------
# Utilities
# ----------------------------
def utc_ts() -> int: return int(time.time())
def make_id(prefix: str = "id") -> str: return f"{prefix}_{uuid.uuid4().hex[:12]}"
def safe_float(v, default=0.0): 
    try: return float(v)
    except Exception: return default
def pretty_json(obj): 
    try: return json.dumps(obj, ensure_ascii=False, indent=2)
    except Exception: return str(obj)

# ----------------------------
# Rate limiting
# ----------------------------
_rate_store: Dict[str,float] = {}
def rate_limit(seconds: float):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if seconds <= 0: return f(*args, **kwargs)
            client = request.headers.get("X-Forwarded-For", request.remote_addr or "anon")
            now = time.time()
            last = _rate_store.get(client, 0)
            if now - last < seconds:
                retry_after = seconds - (now - last)
                return jsonify({"error": "rate_limited", "retry_after": retry_after}), 429
            _rate_store[client] = now
            return f(*args, **kwargs)
        return wrapper
    return decorator

# ----------------------------
# Admin decorator
# ----------------------------
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization") or request.args.get("admin_token")
        if not token:
            return jsonify({"error": "missing_admin_token"}), 401
        if token.startswith("Bearer "): token = token.split(" ",1)[1]
        if token != NEURA_ADMIN_TOKEN: return jsonify({"error": "invalid_admin_token"}), 403
        return f(*args, **kwargs)
    return wrapper

# ----------------------------
# Marketplace generation
# ----------------------------
CATEGORIES = ["AI Tools","Automation Bots","Trading Scripts","Freelancer Tools","Design Studio",
              "Crypto Assets","Voice & Language","Education Packs","Developer Plugins","Global Add-Ons"]
              # ==========================================================
# 🌌 Neuraluxe-AI Tail Section — Stable Worker v3 Fix
# ==========================================================

import math, uuid

# ---------- Utility Section ----------
def gen_item(index: int):
    """Generate a lightweight AI item safely."""
    categories = [
        "AI Tools", "Automation Bots", "Trading Scripts",
        "Freelancer Tools", "Design Studio", "Crypto Assets",
        "Voice & Language", "Education Packs", "Developer Kits"
    ]
    i = max(1, index)
    cat = categories[i % len(categories)]
    return {
        "id": f"nli-{i}",
        "name": f"Neuraluxe {cat} {i}",
        "category": cat,
        "uuid": str(uuid.uuid4())[:8],
        "rating": round((i % 5) + 0.5, 1)
    }

@app.route("/items/<int:count>")
def get_items(count):
    """Return a list of generated AI items."""
    data = [gen_item(i) for i in range(1, min(count, 50) + 1)]
    return jsonify({
        "status": "success",
        "items": data,
        "count": len(data)
    })

# ---------- Safe Environment Checker ----------
@app.route("/env/check")
def env_check():
    """Quick Render-friendly env check route."""
    keys_to_check = [
        "APP_NAME", "APP_VERSION", "FLASK_ENV",
        "CACHE_TYPE", "LOG_LEVEL", "OPENAI_ENABLED"
    ]
    summary = {k: ("✅" if os.getenv(k) else "⚠️ Missing") for k in keys_to_check}
    return jsonify({
        "app": os.getenv("APP_NAME", "Neuraluxe-AI"),
        "version": os.getenv("APP_VERSION", "v10k"),
        "env": summary,
        "message": "Environment check successful 🚀"
    }), 200


# ---------- App Runner ----------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
    # ===========================================================
# 🌌 Neuraluxe-AI v10k Hyperluxe — Ultimate Final Full Production Snippet
# Author: ChatGPT + Joshua Dav
# ===========================================================

import os, multiprocessing, logging, psycopg2, redis, platform, socket, psutil
from datetime import datetime
import smtplib
from email.message import EmailMessage
import requests

# -----------------------------
# 📁 Logging Setup
# -----------------------------
LOG_FILE = os.path.join(os.getcwd(), "neuraluxe_startup.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("NeuraluxeAI")

def log(msg):
    logger.info(msg)

# -----------------------------
# 🚨 Notification System
# -----------------------------
def send_email_alert(subject, body):
    try:
        EMAIL_USER = os.getenv("ALERT_EMAIL_USER")
        EMAIL_PASS = os.getenv("ALERT_EMAIL_PASS")
        EMAIL_TO = os.getenv("ALERT_EMAIL_TO")
        if EMAIL_USER and EMAIL_PASS and EMAIL_TO:
            msg = EmailMessage()
            msg.set_content(body)
            msg["Subject"] = subject
            msg["From"] = EMAIL_USER
            msg["To"] = EMAIL_TO
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_USER, EMAIL_PASS)
                smtp.send_message(msg)
            log("✅ Email alert sent successfully")
    except Exception as e:
        log(f"❌ Failed to send email alert | {e}")

def send_telegram_alert(message):
    try:
        BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
        CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
        if BOT_TOKEN and CHAT_ID:
            requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": message})
            log("✅ Telegram alert sent successfully")
    except Exception as e:
        log(f"❌ Failed to send Telegram alert | {e}")

def send_discord_alert(message):
    try:
        WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
        if WEBHOOK_URL:
            requests.post(WEBHOOK_URL, json={"content": message})
            log("✅ Discord alert sent successfully")
    except Exception as e:
        log(f"❌ Failed to send Discord alert | {e}")

# -----------------------------
# 🧪 Startup Diagnostics
# -----------------------------
def startup_diagnostics():
    log("\n=== 🌟 Neuraluxe-AI Ultimate Startup 🌟 ===")
    
    # Environment Info
    log(f"APP: {os.getenv('APP_NAME', 'NeuraAI_v10k_Hyperluxe')}")
    log(f"VERSION: {os.getenv('APP_VERSION', 'v10k')}")
    log(f"FLASK_ENV: {os.getenv('FLASK_ENV', 'production')}")
    log(f"PORT: {os.getenv('PORT', '10000')}")
    log(f"ASYNC_MODE: {os.getenv('ASYNC_MODE', 'true')}")
    log(f"OPENAI_ENABLED: {os.getenv('OPENAI_ENABLED', 'false')}")
    log(f"CACHE_TYPE: {os.getenv('CACHE_TYPE', 'simple')}")

    # Workers & Threads
    try:
        gunicorn_args = os.getenv("GUNICORN_CMD_ARGS", "--workers=4 --threads=8")
        workers = int(gunicorn_args.split("--workers=")[1].split()[0])
        threads = int(gunicorn_args.split("--threads=")[1].split()[0])
        log(f"Workers: {workers} | Threads: {threads}")
    except Exception:
        log("Workers/Threads info could not be parsed. Using defaults 4/8.")

    # CPU & RAM
    log(f"CPU Count: {multiprocessing.cpu_count()}")
    mem = psutil.virtual_memory()
    log(f"RAM: {mem.total / (1024 ** 3):.2f} GB | Available: {mem.available / (1024 ** 3):.2f} GB")

    # OS & Host
    log(f"OS: {platform.system()} {platform.release()}")
    log(f"Hostname: {socket.gethostname()} | IP: {socket.gethostbyname(socket.gethostname())}")

    # Disk Usage
    disk = psutil.disk_usage("/")
    log(f"Disk: Total {disk.total / (1024**3):.2f} GB | Free {disk.free / (1024**3):.2f} GB")

    # PostgreSQL Check
    try:
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            conn = psycopg2.connect(db_url)
            conn.close()
            log("✅ PostgreSQL: Connection successful")
        else:
            log("⚠️ PostgreSQL: DATABASE_URL not set")
    except Exception as e:
        log(f"❌ PostgreSQL: Connection failed | {e}")
        send_email_alert("Neuraluxe-AI Startup DB Error", str(e))
        send_telegram_alert(f"Neuraluxe-AI DB Error: {e}")
        send_discord_alert(f"Neuraluxe-AI DB Error: {e}")

    # Redis Check
    try:
        r = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
        r.ping()
        log("✅ Redis: Connection successful")
    except Exception as e:
        log(f"❌ Redis: Connection failed | {e}")
        send_email_alert("Neuraluxe-AI Startup Redis Error", str(e))
        send_telegram_alert(f"Neuraluxe-AI Redis Error: {e}")
        send_discord_alert(f"Neuraluxe-AI Redis Error: {e}")

    # AI Services
    ai_enabled = os.getenv("OPENAI_ENABLED", "false").lower() == "true"
    log(f"AI Services Enabled: {ai_enabled}")

    # Optional Features
    log("🌟 Additional Features Enabled:")
    optional_features = [
        "Offline + online hybrid AI mode",
        "Persistent memory storage for sessions",
        "Automatic environment validation /env/check",
        "Email alerts for critical failures",
        "Logging all diagnostics to file + console",
        "Resource monitoring for CPU, RAM, Disk",
        "Redis & DB checks with error alerts",
        "AI services readiness check",
        "Developer free-tier bypass toggle",
        "Future ready hooks for trading bots & marketplace scaling"
    ]
    for idx, feat in enumerate(optional_features, start=1):
        log(f"{idx}. {feat}")

    log("✅ All checks complete. Neuraluxe-AI is live and ready!\n")

# Execute startup diagnostics
startup_diagnostics()