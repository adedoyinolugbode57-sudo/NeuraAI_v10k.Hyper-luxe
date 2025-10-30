"""
main.py — NeuraAI_v10k.Hyperluxe (Final, ~800-line Grand Entry)

Features:
- PostgreSQL via SQLAlchemy (DATABASE_URL env)
- Uses ai_engine (OpenAI) when available; falls back to local model for offline
- Microservice-first (AI_SERVICE_URL etc.) with local-module fallbacks
- Optional realtime chat via Flask-SocketIO (if installed)
- Admin dashboard and token protection (NEURA_ADMIN_TOKEN)
- Endpoints: /chat, /api/books/*, /api/games/*, /api/analytics/*, /api/voice/*, /api/health/*
- Background maintenance thread, upload, backups, bootstrap
- Logging, events ingestion, and basic DB models (users, chats, events)
- Ready for Render + Gunicorn
Author: ChatGPT + Joshua Dav
"""

import os
import sys
import time
import json
import logging
import atexit
import threading
import random
from pathlib import Path
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional, Dict, Any

# Flask and extras
from flask import (
    Flask, request, jsonify, send_from_directory, abort, render_template_string
)
from flask_cors import CORS

# HTTP for microservice proxying
import requests

# SQLAlchemy for PostgreSQL
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Try optional socketio
USE_SOCKETIO = False
socketio = None
try:
    from flask_socketio import SocketIO, emit, join_room, leave_room
    USE_SOCKETIO = True
except Exception:
    USE_SOCKETIO = False

# -------------------------
# Project paths & dirs
# -------------------------
PROJECT_ROOT = Path(__file__).parent.resolve()
STATIC_DIR = PROJECT_ROOT / "static"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"
UPLOADS_DIR = PROJECT_ROOT / "uploads"
for d in (STATIC_DIR, TEMPLATES_DIR, DATA_DIR, LOG_DIR, UPLOADS_DIR):
    d.mkdir(parents=True, exist_ok=True)

# -------------------------
# Environment / Config
# -------------------------
ENV = os.getenv("FLASK_ENV", "production")
PORT = int(os.getenv("PORT", os.getenv("RENDER_PORT", 5000)))
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/neura")
NEURA_ADMIN_TOKEN = os.getenv("NEURA_ADMIN_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
NEURA_MODEL = os.getenv("NEURA_MODEL", "gpt-5-mini")

# Microservice URLs (optional)
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL")
VOICE_SERVICE_URL = os.getenv("VOICE_SERVICE_URL")
GAMES_SERVICE_URL = os.getenv("GAMES_SERVICE_URL")
BOOKS_SERVICE_URL = os.getenv("BOOKS_SERVICE_URL")
ANALYTICS_SERVICE_URL = os.getenv("ANALYTICS_SERVICE_URL")
UPDATE_SERVICE_URL = os.getenv("UPDATE_SERVICE_URL")

# -------------------------
# Logging
# -------------------------
LOG_FILE = LOG_DIR / "neura.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(str(LOG_FILE))
    ],
)
logger = logging.getLogger("neura")

# -------------------------
# Flask app
# -------------------------
app = Flask(__name__, static_folder=str(STATIC_DIR), template_folder=str(TEMPLATES_DIR))
CORS(app)

if USE_SOCKETIO:
    socketio = SocketIO(app, cors_allowed_origins="*")
    logger.info("SocketIO available — realtime enabled.")
else:
    logger.info("SocketIO not installed — realtime disabled.")

# -------------------------
# Database setup (SQLAlchemy)
# -------------------------
Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

# Example models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True, nullable=False)
    email = Column(String(256), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatLog(Base):
    __tablename__ = "chat_logs"
    id = Column(Integer, primary_key=True)
    user = Column(String(128), nullable=True)
    prompt = Column(Text)
    response = Column(Text)
    latency = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    type = Column(String(128))
    payload = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables ensured.")
    except Exception as e:
        logger.exception("init_db failed: %s", e)

# initialize DB at startup
init_db()

# -------------------------
# Safe imports (local modules as fallbacks)
# -------------------------
def safe_import(modname: str):
    try:
        mod = __import__(modname)
        logger.info("Imported local module: %s", modname)
        return mod
    except Exception as e:
        logger.debug("Local module %s not available: %s", modname, e)
        return None

local_ai = safe_import("ai_engine")
local_voice = safe_import("ai_voice_assistant") or safe_import("voice_assistant")
local_games = safe_import("mini_games")
local_books = safe_import("book_platform")
local_analytics = safe_import("analytics_routes")
local_healthcare = safe_import("healthcare")
local_ai_memory = safe_import("ai_memory")

# -------------------------
# Helpers & utilities
# -------------------------
def require_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", "") or request.args.get("admin_token", "")
        if token.startswith("Bearer "):
            token = token.split(" ", 1)[1]
        if not NEURA_ADMIN_TOKEN:
            logger.warning("NEURA_ADMIN_TOKEN not set — admin endpoints are open (dev).")
            return f(*args, **kwargs)
        if token != NEURA_ADMIN_TOKEN:
            return jsonify({"ok": False, "error": "unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapper

def proxy_post(url: str, payload: dict, timeout: int = 15) -> dict:
    try:
        r = requests.post(url, json=payload, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.exception("proxy_post failed to %s : %s", url, e)
        return {"ok": False, "error": str(e)}

def proxy_get(url: str, params: dict = None, timeout: int = 10) -> dict:
    try:
        r = requests.get(url, params=params or {}, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.exception("proxy_get failed to %s : %s", url, e)
        return {"ok": False, "error": str(e)}

def append_event_db(event_type: str, payload: dict):
    try:
        db = SessionLocal()
        ev = Event(type=event_type, payload=payload)
        db.add(ev)
        db.commit()
        db.close()
    except Exception:
        logger.exception("append_event_db failed")

def append_event_file(payload: dict):
    try:
        path = DATA_DIR / "events.log"
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except Exception:
        logger.exception("append_event_file failed")

def append_event(event_type: str, payload: dict):
    append_event_file({"type": event_type, "payload": payload, "ts": time.time()})
    try:
        append_event_db(event_type, payload)
    except Exception:
        pass

# -------------------------
# AI generation wrapper
# Prefer: AI_SERVICE_URL -> local_ai module -> OpenAI via ai_engine module (if present) -> fallback simple model
# -------------------------
def ai_call_microservice(prompt: str, user: str = "guest", extra: dict = None) -> dict:
    if not AI_SERVICE_URL:
        return {"ok": False, "error": "no_microservice"}
    payload = {"prompt": prompt, "user": user}
    if extra:
        payload.update(extra)
    url = AI_SERVICE_URL.rstrip("/") + "/chat"
    return proxy_post(url, payload)

def ai_call_local_module(prompt: str, user: str = "guest"):
    if not local_ai:
        return {"ok": False, "error": "no_local_ai"}
    try:
        # Check for commonly used functions
        if hasattr(local_ai, "ai_generate"):
            out = local_ai.ai_generate(prompt, user=user)
            return {"ok": True, "reply": out}
        if hasattr(local_ai, "generate_reply"):
            out = local_ai.generate_reply(prompt, user=user)
            return {"ok": True, "reply": out}
        # fallback: if module exposes 'chat' that returns dict
        if hasattr(local_ai, "chat"):
            res = local_ai.chat({"prompt": prompt, "user": user})
            if isinstance(res, dict) and "reply" in res:
                return {"ok": True, "reply": res["reply"]}
            return {"ok": True, "reply": str(res)}
    except Exception:
        logger.exception("local_ai call failed")
    return {"ok": False, "error": "local_ai_failed"}

def ai_call_openai(prompt: str, user: str = "guest", model: str = None):
    """
    Use OpenAI through local ai_engine if it implements a wrapper that uses OPENAI_API_KEY.
    If local_ai has function ai_generate_openai or similar, prefer it. Otherwise attempt a minimal direct call to openai package (if installed).
    """
    try:
        # First try local_ai wrappers that might use OpenAI correctly
        if local_ai:
            if hasattr(local_ai, "ai_generate_openai"):
                return {"ok": True, "reply": local_ai.ai_generate_openai(prompt, user=user)}
            if hasattr(local_ai, "openai_generate"):
                return {"ok": True, "reply": local_ai.openai_generate(prompt, user=user)}
        # Direct openai fallback if package is installed and OPENAI_API_KEY exists
        if OPENAI_API_KEY:
            import openai
            openai.api_key = OPENAI_API_KEY
            model_to_use = model or NEURA_MODEL or "gpt-4o"
            # Try Chat Completions style using recent openai library pattern
            try:
                # Use chat completion API shape for modern versions
                resp = openai.chat.completions.create(
                    model=model_to_use,
                    messages=[
                        {"role":"system", "content":"You are NeuraAI, a helpful, fast assistant."},
                        {"role":"user", "content": prompt}
                    ],
                    max_tokens=400,
                    temperature=0.6
                )
                if resp and getattr(resp, "choices", None):
                    content = resp.choices[0].message.content.strip()
                    return {"ok": True, "reply": content}
                # fallback structure
                if isinstance(resp, dict) and "choices" in resp:
                    content = resp["choices"][0]["message"]["content"]
                    return {"ok": True, "reply": content}
            except Exception as e:
                logger.exception("openai.chat.completions failed, trying completions endpoint: %s", e)
                # older fallback
                try:
                    resp = openai.Completion.create(model=model_to_use, prompt=prompt, max_tokens=200)
                    text = resp.choices[0].text.strip()
                    return {"ok": True, "reply": text}
                except Exception:
                    logger.exception("openai.Completion.create failed")
    except Exception:
        logger.exception("ai_call_openai failed")
    return {"ok": False, "error": "openai_failed_or_not_configured"}

def generate_ai_reply(prompt: str, user: str = "guest", prefer: str = "microservice") -> Dict[str, Any]:
    """
    Orchestrate AI call according to preference:
    - 'microservice' first (AI_SERVICE_URL)
    - then local module
    - then OpenAI direct (if API key)
    - finally fallback simple generator
    """
    # 1) Microservice
    if AI_SERVICE_URL and prefer in ("microservice", "auto"):
        res = ai_call_microservice(prompt, user)
        if res.get("ok"):
            return res

    # 2) Local ai module
    res = ai_call_local_module(prompt, user)
    if res.get("ok"):
        return res

    # 3) OpenAI direct
    res = ai_call_openai(prompt, user)
    if res.get("ok"):
        return res

    # 4) Microservice again as last resort
    if AI_SERVICE_URL and prefer == "auto":
        res = ai_call_microservice(prompt, user)
        if res.get("ok"):
            return res

    # 5) Simple fallback
    fallback = simple_fallback_reply(prompt)
    return {"ok": True, "reply": fallback}

def simple_fallback_reply(prompt: str) -> str:
    p = prompt.lower()
    if "hello" in p or p.strip() in ("hi", "hey"):
        return "Hello — I'm NeuraAI Hyperluxe. Try asking 'recommend a book' or 'play a game'."
    if "time" in p:
        return f"Server time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"
    if "health" in p:
        return "I can help with basic health advice. Use /api/health/check with symptoms."
    if "crypto" in p:
        if local_ai and hasattr(local_ai, "crypto_summary"):
            try:
                return local_ai.crypto_summary()
            except Exception:
                pass
        return "Connect a crypto insights module to get live market advice."
    return "Interesting — tell me more."

# -------------------------
# Chat endpoints (HTTP + optional SocketIO)
# -------------------------
@app.route("/chat", methods=["POST"])
def chat_endpoint():
    body = request.get_json(silent=True) or {}
    message = body.get("message") or body.get("prompt") or ""
    user = body.get("user", "guest")
    voice = bool(body.get("voice", False))
    prefer = body.get("prefer", "auto")

    if not message:
        return jsonify({"ok": False, "error": "empty_message"}), 400

    start = time.time()
    res = generate_ai_reply(message, user=user, prefer=prefer)
    latency = round(time.time() - start, 3)
    reply = res.get("reply", "Sorry — no reply available.")

    # Save to DB log
    try:
        db = SessionLocal()
        log = ChatLog(user=user, prompt=message, response=reply, latency=latency)
        db.add(log)
        db.commit()
        db.close()
    except Exception:
        logger.exception("Failed to save chat log")

    # append event
    append_event("ai_query", {"user": user, "prompt": message, "latency": latency})

    out = {"ok": True, "reply": reply, "latency_s": latency}

    # TTS generation if requested
    if voice:
        audio_url = None
        tts_payload = {"text": reply, "language": body.get("language", "en"), "mood": body.get("mood", "cheerful")}
        if VOICE_SERVICE_URL:
            try:
                r = proxy_post(VOICE_SERVICE_URL.rstrip("/") + "/speak", tts_payload)
                audio_url = r.get("audio")
            except Exception:
                logger.exception("voice service error")
        elif local_voice and hasattr(local_voice, "speak_text"):
            try:
                audio_url = local_voice.speak_text(reply, lang=tts_payload["language"], mood=tts_payload["mood"])
            except Exception:
                logger.exception("local tts error")
        out["audio"] = audio_url

    return jsonify(out)

# SocketIO handlers if available
if USE_SOCKETIO:
    @socketio.on("join")
    def _join(data):
        room = data.get("room", "global")
        join_room(room)
        emit("system", {"msg": f"Joined {room}"}, room=room)

    @socketio.on("message")
    def _on_message(data):
        room = data.get("room", "global")
        prompt = data.get("prompt", "")
        user = data.get("user", "guest")
        voice = bool(data.get("voice", False))
        if not prompt:
            emit("error", {"error": "empty_prompt"}, room=room)
            return
        emit("typing", {"user": "neura"}, room=room)
        res = generate_ai_reply(prompt, user=user)
        reply = res.get("reply", "No reply.")
        append_event("ai_query", {"user": user, "prompt": prompt})
        emit("reply", {"user": "neura", "reply": reply}, room=room)
        if voice:
            if VOICE_SERVICE_URL:
                r = proxy_post(VOICE_SERVICE_URL.rstrip("/") + "/speak", {"text": reply})
                audio = r.get("audio")
                emit("audio", {"url": audio}, room=room)
            elif local_voice and hasattr(local_voice, "speak_text"):
                try:
                    audio = local_voice.speak_text(reply)
                    emit("audio", {"url": audio}, room=room)
                except Exception:
                    pass

# -------------------------
# Books microservice wrappers
# -------------------------
@app.route("/api/books/list", methods=["GET"])
def books_list():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    q = request.args.get("q")
    category = request.args.get("category")
    if BOOKS_SERVICE_URL:
        return jsonify(proxy_get(BOOKS_SERVICE_URL.rstrip("/") + "/books/list", params={"page": page, "page_size": page_size, "q": q, "category": category}))
    if local_books and hasattr(local_books, "list_books"):
        try:
            data = local_books.list_books(page=page, page_size=page_size, category=category, q=q)
            return jsonify({"ok": True, "data": data})
        except Exception:
            logger.exception("local book list failed")
            return jsonify({"ok": False, "error": "local_books_error"}), 500
    return jsonify({"ok": False, "error": "books_unavailable"}), 404

@app.route("/api/books/get/<book_id>", methods=["GET"])
def books_get(book_id):
    if BOOKS_SERVICE_URL:
        return jsonify(proxy_get(BOOKS_SERVICE_URL.rstrip("/") + f"/books/get/{book_id}"))
    if local_books and hasattr(local_books, "get_book"):
        try:
            book = local_books.get_book(book_id)
            if book:
                return jsonify({"ok": True, "book": book})
            return jsonify({"ok": False, "error": "not_found"}), 404
        except Exception:
            logger.exception("local book get failed")
            return jsonify({"ok": False, "error": "local_books_error"}), 500
    return jsonify({"ok": False, "error": "books_unavailable"}), 404

@app.route("/api/books/add", methods=["POST"])
@require_admin
def books_add():
    payload = request.get_json(silent=True) or {}
    if BOOKS_SERVICE_URL:
        return jsonify(proxy_post(BOOKS_SERVICE_URL.rstrip("/") + "/books/add", payload))
    if local_books and hasattr(local_books, "add_book"):
        try:
            book = local_books.add_book(payload)
            append_event("book_add", {"title": book.get("title"), "author": book.get("author")})
            return jsonify({"ok": True, "book": book})
        except Exception:
            logger.exception("local book add failed")
            return jsonify({"ok": False, "error": "local_add_failed"}), 500
    return jsonify({"ok": False, "error": "books_unavailable"}), 404

# -------------------------
# Games microservice wrappers
# -------------------------
@app.route("/api/games/list", methods=["GET"])
def games_list():
    if GAMES_SERVICE_URL:
        return jsonify(proxy_get(GAMES_SERVICE_URL.rstrip("/") + "/games/list"))
    if local_games and hasattr(local_games, "load_games"):
        try:
            games = local_games.load_games()
            return jsonify({"ok": True, "count": len(games), "games": games})
        except Exception:
            logger.exception("local games load failed")
            return jsonify({"ok": False, "error": "local_games_error"}), 500
    return jsonify({"ok": False, "error": "games_unavailable"}), 404

@app.route("/api/games/play/<game_id>", methods=["POST"])
def games_play(game_id):
    if GAMES_SERVICE_URL:
        return jsonify(proxy_post(GAMES_SERVICE_URL.rstrip("/") + f"/games/play/{game_id}", request.get_json(silent=True) or {}))
    if local_games and hasattr(local_games, "load_games"):
        try:
            games = local_games.load_games()
            for g in games:
                if g.get("id") == game_id:
                    return jsonify({"ok": True, "game": g})
            return jsonify({"ok": False, "error": "not_found"}), 404
        except Exception:
            logger.exception("local game play failed")
            return jsonify({"ok": False, "error": "local_games_error"}), 500
    return jsonify({"ok": False, "error": "games_unavailable"}), 404

@app.route("/api/games/bootstrap", methods=["POST"])
@require_admin
def games_bootstrap():
    if GAMES_SERVICE_URL:
        return jsonify(proxy_post(GAMES_SERVICE_URL.rstrip("/") + "/games/bootstrap", {}))
    if local_games and hasattr(local_games, "bootstrap_games"):
        try:
            local_games.bootstrap_games()
            return jsonify({"ok": True, "message": "games_bootstrapped"})
        except Exception:
            logger.exception("local bootstrap failed")
            return jsonify({"ok": False, "error": "bootstrap_failed"}), 500
    return jsonify({"ok": False, "error": "games_unavailable"}), 404

# -------------------------
# Analytics microservice wrappers
# -------------------------
@app.route("/api/analytics/summary", methods=["GET"])
@require_admin
def analytics_summary():
    if ANALYTICS_SERVICE_URL:
        return jsonify(proxy_get(ANALYTICS_SERVICE_URL.rstrip("/") + "/summary"))
    if local_analytics and hasattr(local_analytics, "summary"):
        try:
            s = local_analytics.summary()
            return jsonify({"ok": True, "summary": s})
        except Exception:
            logger.exception("local analytics summary failed")
            return jsonify({"ok": False, "error": "local_analytics_error"}), 500
    # fallback using events.log
    events_file = DATA_DIR / "events.log"
    total = 0
    types = {}
    if events_file.exists():
        with open(events_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    e = json.loads(line.strip())
                    total += 1
                    types[e.get("type")] = types.get(e.get("type"), 0) + 1
                except Exception:
                    continue
    return jsonify({"ok": True, "summary": {"total_events": total, "top_event_types": types}})

# -------------------------
# Voice microservice wrappers (TTS)
# -------------------------
@app.route("/api/voice/speak", methods=["POST"])
def voice_speak():
    payload = request.get_json(silent=True) or {}
    text = payload.get("text", "")
    lang = payload.get("language", "en")
    mood = payload.get("mood", "cheerful")
    if not text:
        return jsonify({"ok": False, "error": "no_text"}), 400
    if VOICE_SERVICE_URL:
        return jsonify(proxy_post(VOICE_SERVICE_URL.rstrip("/") + "/speak", payload))
    if local_voice and hasattr(local_voice, "speak_text"):
        try:
            audio = local_voice.speak_text(text, lang=lang, mood=mood)
            return jsonify({"ok": True, "audio": audio})
        except Exception:
            logger.exception("local voice speak failed")
            return jsonify({"ok": False, "error": "tts_failed"}), 500
    return jsonify({"ok": False, "error": "voice_unavailable"}), 404

# -------------------------
# Health microservice wrapper
# -------------------------
@app.route("/api/health/check", methods=["POST"])
def health_check():
    payload = request.get_json(silent=True) or {}
    if local_healthcare and hasattr(local_healthcare, "generate_wellness_report"):
        try:
            report = local_healthcare.generate_wellness_report(payload)
            return jsonify({"ok": True, "report": report})
        except Exception:
            logger.exception("local healthcare failed")
            return jsonify({"ok": False, "error": "healthcare_failed"}), 500
    return jsonify({"ok": False, "error": "healthcare_unavailable"}), 404

# -------------------------
# Admin endpoints & dashboard
# -------------------------
ADMIN_HTML = """
<!doctype html><html><head><meta charset="utf-8"><title>NeuraAI Admin</title>
<style>body{background:#070720;color:#e0f7ff;font-family:Inter,Arial;padding:20px} .card{background:#0f1624;padding:18px;border-radius:10px;margin-bottom:12px}</style>
</head><body>
<h1>NeuraAI Hyperluxe — Admin Panel</h1>
<div class="card">
<button onclick="doAction('stats')">Get Stats</button>
<button onclick="doAction('backup')">Backup Events</button>
<button onclick="doAction('bootstrap')">Bootstrap Demo</button>
</div>
<pre id="out"></pre>
<script>
const token = prompt('Enter admin token:');
async function doAction(a){
  const headers = {'Authorization':'Bearer '+token,'Content-Type':'application/json'};
  let res = await fetch('/admin/'+a,{method:'POST',headers}).then(r=>r.json());
  document.getElementById('out').textContent = JSON.stringify(res,null,2);
}
</script>
</body></html>
"""

@app.route("/admin", methods=["GET"])
def admin_ui():
    return ADMIN_HTML

@app.route("/admin/stats", methods=["POST"])
@require_admin
def admin_stats_post():
    uptime = time.time() - app.config.get("start_ts", time.time())
    modules = {
        "ai": bool(AI_SERVICE_URL or local_ai or OPENAI_API_KEY),
        "voice": bool(VOICE_SERVICE_URL or local_voice),
        "games": bool(GAMES_SERVICE_URL or local_games),
        "books": bool(BOOKS_SERVICE_URL or local_books),
        "analytics": bool(ANALYTICS_SERVICE_URL or local_analytics)
    }
    return jsonify({"ok": True, "uptime_s": uptime, "modules": modules, "time": datetime.utcnow().isoformat()})

@app.route("/admin/backup", methods=["POST"])
@require_admin
def admin_backup():
    events_file = DATA_DIR / "events.log"
    if not events_file.exists():
        return jsonify({"ok": False, "error": "no_events"})
    backup_dir = PROJECT_ROOT / "backups"
    backup_dir.mkdir(exist_ok=True)
    dst = backup_dir / f"events_backup_{int(time.time())}.log"
    with open(events_file, "rb") as sf, open(dst, "wb") as df:
        df.write(sf.read())
    return jsonify({"ok": True, "path": str(dst)})

@app.route("/admin/bootstrap", methods=["POST"])
@require_admin
def admin_bootstrap():
    try:
        # bootstrap local data files and optionally call microservices bootstrap endpoints
        bootstrap_defaults()
        if GAMES_SERVICE_URL:
            proxy_post(GAMES_SERVICE_URL.rstrip("/") + "/games/bootstrap", {})
        if BOOKS_SERVICE_URL:
            proxy_post(BOOKS_SERVICE_URL.rstrip("/") + "/books/bootstrap", {})
        return jsonify({"ok": True, "message": "Bootstrapped locally and attempted microservice bootstraps."})
    except Exception:
        logger.exception("admin bootstrap failed")
        return jsonify({"ok": False, "error": "bootstrap_failed"}), 500

# -------------------------
# Uploads (admin)
# -------------------------
@app.route("/admin/upload", methods=["POST"])
@require_admin
def admin_upload():
    if "file" not in request.files:
        return jsonify({"ok": False, "error": "no_file"}), 400
    f = request.files["file"]
    dest = UPLOADS_DIR / f.filename
    f.save(str(dest))
    return jsonify({"ok": True, "path": str(dest)})

# -------------------------
# Health & readiness
# -------------------------
@app.route("/healthz", methods=["GET"])
def healthz():
    mem_ok = True
    try:
        import psutil
        proc = psutil.Process()
        mem = proc.memory_info().rss
        mem_ok = mem < 2 * 1024 * 1024 * 1024
    except Exception:
        mem_ok = True
    status = {
        "ok": True,
        "env": ENV,
        "ai": bool(AI_SERVICE_URL or local_ai or OPENAI_API_KEY),
        "voice": bool(VOICE_SERVICE_URL or local_voice),
        "memory_ok": mem_ok,
        "time": datetime.utcnow().isoformat()
    }
    return jsonify(status)

@app.route("/readyz", methods=["GET"])
def readyz():
    ready = True
    details = {}
    if AI_SERVICE_URL:
        try:
            r = requests.get(AI_SERVICE_URL.rstrip("/") + "/status", timeout=3)
            details["ai_status"] = r.json() if r.ok else {"ok": False, "code": r.status_code}
            if not r.ok:
                ready = False
        except Exception as e:
            details["ai_status_error"] = str(e)
            ready = False
    else:
        details["ai_local"] = bool(local_ai or OPENAI_API_KEY)
    return jsonify({"ready": ready, "details": details})

# -------------------------
# Events ingestion endpoint
# -------------------------
@app.route("/events", methods=["POST"])
def ingest_event():
    payload = request.get_json(silent=True) or {}
    ev_type = payload.get("type", "custom")
    append_event(ev_type, payload.get("payload", {}))
    return jsonify({"ok": True})

# -------------------------
# Background maintenance
# -------------------------
_shutdown = threading.Event()

def background_worker():
    logger.info("Background worker started.")
    while not _shutdown.is_set():
        try:
            # prune audio files
            audio_dir = STATIC_DIR / "audio"
            if audio_dir.exists():
                files = sorted(audio_dir.glob("*.mp3"), key=lambda p: p.stat().st_mtime)
                if len(files) > 200:
                    for f in files[:len(files)-200]:
                        try:
                            f.unlink()
                        except Exception:
                            pass
            # rotate events.log
            ev = DATA_DIR / "events.log"
            if ev.exists() and ev.stat().st_size > 5_000_000:
                dst = PROJECT_ROOT / f"events_rotated_{int(time.time())}.log"
                try:
                    ev.rename(dst)
                except Exception:
                    pass
        except Exception:
            logger.exception("background_task error")
        time.sleep(60 if ENV != "production" else 300)

_bg_thread = threading.Thread(target=background_worker, daemon=True)
_bg_thread.start()

@atexit.register
def shutdown():
    logger.info("Shutting down NeuraAI gateway.")
    _shutdown.set()
    try:
        _bg_thread.join(timeout=2)
    except Exception:
        pass

# -------------------------
# Bootstrap defaults (create minimal JSON files to avoid errors)
# -------------------------
def bootstrap_defaults():
    books = DATA_DIR / "books.json"
    if not books.exists():
        books.write_text(json.dumps({"books": {}}, indent=2), encoding="utf-8")
    games = DATA_DIR / "game_data.json"
    if not games.exists():
        games.write_text(json.dumps({"games": []}, indent=2), encoding="utf-8")
    memory = DATA_DIR / "memory_store.json"
    if not memory.exists():
        memory.write_text(json.dumps({"conversations": {}}, indent=2), encoding="utf-8")
    logger.info("Bootstrap defaults created.")

# -------------------------
# CLI / Main
# -------------------------
app.config["start_ts"] = time.time()

def run_dev():
    bootstrap_defaults()
    if USE_SOCKETIO:
        logger.info("Running dev with socketio on port %s", PORT)
        socketio.run(app, host="0.0.0.0", port=PORT, debug=(ENV != "production"))
    else:
        logger.info("Running Flask dev on port %s", PORT)
        app.run(host="0.0.0.0", port=PORT, debug=(ENV != "production"))

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "run"
    if arg in ("run", "start"):
        run_dev()
    elif arg == "bootstrap":
        bootstrap_defaults()
        print("Bootstrapped minimal data files.")
    elif arg == "test":
        print("NeuraAI Gateway Test")
        print("ENV:", ENV)
        print("DATABASE_URL:", DATABASE_URL)
        print("AI_SERVICE_URL:", AI_SERVICE_URL or "local")
        print("VOICE_SERVICE_URL:", VOICE_SERVICE_URL or "local")
        print("Modules available (local):")
        print(" - ai_engine:", bool(local_ai))
        print(" - ai_voice:", bool(local_voice))
        print(" - mini_games:", bool(local_games))
        print(" - book_platform:", bool(local_books))
        print(" - analytics:", bool(local_analytics))
    else:
        print("Usage: python main.py [run|bootstrap|test]")
        from flask_caching import Cache
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache = Cache(app)
from auto_register import register_all_blueprints
register_all_blueprints(app)