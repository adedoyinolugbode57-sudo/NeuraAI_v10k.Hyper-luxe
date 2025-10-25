# user_profiles.py
"""
User profiles module for NeuraAI_v10k.HyperLuxe
Features: register/login, JWT tokens, avatar upload, preferences.
Requires: config.py and database.db (or adapt to your DB layer).
Created by ChatGPT + Joshua Dav
"""

import os
import time
import uuid
import logging
from typing import Optional, Dict
from functools import wraps
from pathlib import Path

import jwt
from passlib.context import CryptContext

from config import OPENAI_API_KEY, ADMIN_TOKEN, PROJECT_ROOT  # PROJECT_ROOT optional
try:
    from database import db
except Exception:
    db = None  # fallback; you can implement file fallback if needed

logger = logging.getLogger("user_profiles")
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT config — set these env vars in Render or .env
JWT_SECRET = os.getenv("JWT_SECRET", "change_this_secret")
JWT_ALG = "HS256"
ACCESS_EXPIRE = int(os.getenv("ACCESS_EXPIRE", 900))    # 15 minutes
REFRESH_EXPIRE = int(os.getenv("REFRESH_EXPIRE", 60*60*24*30))  # 30 days

AVATAR_DIR = Path(os.getenv("AVATAR_DIR", str(Path(__file__).parent / "uploads" / "avatars")))
AVATAR_DIR.mkdir(parents=True, exist_ok=True)

def hash_password(password: str) -> str:
    return pwd_ctx.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_ctx.verify(password, hashed)

def _make_uid() -> str:
    return "user_" + uuid.uuid4().hex[:12]

def create_tokens(uid: str) -> Dict[str, str]:
    now = int(time.time())
    access = jwt.encode({"sub": uid, "exp": now + ACCESS_EXPIRE, "iat": now}, JWT_SECRET, algorithm=JWT_ALG)
    refresh = jwt.encode({"sub": uid, "exp": now + REFRESH_EXPIRE, "iat": now}, JWT_SECRET, algorithm=JWT_ALG)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer", "expires_in": ACCESS_EXPIRE}

def decode_token(token: str) -> Optional[Dict]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except Exception:
        return None

# Storage helpers (uses database.py's users table if available)
def _save_user_record(uid: str, email: str, hashed_pw: str, username: Optional[str] = None, prefs: dict = None):
    if db:
        # store in SQL DB
        try:
            db.create_user(uid=uid, username=username, email=email, prefs=prefs or {})
            return True
        except Exception:
            logger.exception("db.create_user failed")
            return False
    # fallback file method
    users_file = Path(__file__).parent / "users.json"
    users_file.parent.mkdir(parents=True, exist_ok=True)
    data = {}
    if users_file.exists():
        data = json.loads(users_file.read_text(encoding="utf-8"))
    data.setdefault("users", {})[uid] = {"uid": uid, "email": email, "username": username, "password": hashed_pw, "prefs": prefs or {}}
    users_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return True

def _find_user_by_email(email: str) -> Optional[Dict]:
    if db:
        try:
            # fallback to get_user (assumes field email exists; adapt if needed)
            # database.get_user currently matches by uid; you may add a SQL query here
            with db.get_conn() as conn:
                r = conn.execute("SELECT uid, username, email, prefs FROM users WHERE email = :e", {"e": email}).fetchone()
                if r:
                    return dict(r)
        except Exception:
            pass
    users_file = Path(__file__).parent / "users.json"
    if users_file.exists():
        data = json.loads(users_file.read_text(encoding="utf-8"))
        for u in data.get("users", {}).values():
            if u.get("email") == email:
                return u
    return None

# Public API
def register_user(email: str, password: str, username: Optional[str] = None) -> Dict:
    if _find_user_by_email(email):
        return {"error": "email_exists"}
    uid = _make_uid()
    hashed = hash_password(password)
    ok = _save_user_record(uid, email, hashed, username=username, prefs={})
    if not ok:
        return {"error": "save_failed"}
    tokens = create_tokens(uid)
    logger.info("Registered user %s", email)
    return {"ok": True, "uid": uid, "tokens": tokens}

def login_user(email: str, password: str) -> Dict:
    user = _find_user_by_email(email)
    if not user:
        return {"error": "not_found"}
    hashed = user.get("password") or (user.get("prefs") or {}).get("password_hash")
    if not hashed or not verify_password(password, hashed):
        return {"error": "invalid_credentials"}
    uid = user.get("uid")
    tokens = create_tokens(uid)
    return {"ok": True, "uid": uid, "tokens": tokens}

def upload_avatar(uid: str, file_storage) -> Optional[str]:
    filename = f"{uid}_{secure_filename(file_storage.filename)}"
    dest = AVATAR_DIR / filename
    file_storage.save(dest)
    # persist path in DB prefs if possible
    if db:
        rec = db.get_user(uid)
        if rec:
            prefs = rec.get("prefs") or {}
            prefs["avatar"] = str(dest)
            with db.get_conn() as conn:
                conn.execute("UPDATE users SET prefs = :p WHERE uid = :u", {"p": prefs, "u": uid})
    return str(dest)

# Decorator for route protection (Flask)
def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        from flask import request, jsonify
        auth = request.headers.get("Authorization", "") or request.args.get("token") or ""
        token = auth.split("Bearer ")[-1] if "Bearer " in auth else auth
        payload = decode_token(token)
        if not payload:
            return (jsonify({"error": "unauthorized"}), 401)
        request.user = payload.get("sub")
        return f(*args, **kwargs)
    return wrapper