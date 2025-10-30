"""
security_manager.py
Neura-AI v10k.Hyperluxe — Security utilities (HMAC tokens, API keys, password hashing)
Author: ChatGPT + Joshua Dav
Purpose: Lightweight, dependency-free helpers for tokens, API keys and password hashing.
Usage:
    from security_manager import (
        hash_password, verify_password,
        generate_api_key, verify_api_key,
        generate_token, verify_token,
        require_token
    )
Notes:
- Uses environment variables: SECRET_KEY (recommended), ADMIN_TOKEN (optional).
- No secrets are hard-coded here.
"""

import os
import time
import hmac
import hashlib
import secrets
import base64
from functools import wraps
from typing import Optional
from flask import request, jsonify

# Configuration from environment (fallback to generated ephemeral secret in dev)
SECRET_KEY = os.getenv("SECRET_KEY") or os.getenv("NEURA_SECRET") or secrets.token_hex(32)
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "")  # recommended to set in env (Render / .env)

# -------------------------
# Password hashing (PBKDF2)
# -------------------------
def hash_password(password: str, salt: Optional[bytes] = None, iterations: int = 200_000) -> str:
    """
    Hash password using PBKDF2-HMAC-SHA256.
    Returns: base64-encoded string containing iterations:salt:hash
    """
    if salt is None:
        salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    b64 = base64.b64encode(dk).decode("utf-8")
    s_salt = base64.b64encode(salt).decode("utf-8")
    return f"{iterations}:{s_salt}:{b64}"

def verify_password(password: str, stored: str) -> bool:
    """
    Verify a password against the stored format iterations:salt:hash
    """
    try:
        iterations_str, s_salt, s_hash = stored.split(":")
        iterations = int(iterations_str)
        salt = base64.b64decode(s_salt.encode("utf-8"))
        expected = base64.b64decode(s_hash.encode("utf-8"))
        test = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
        return hmac.compare_digest(test, expected)
    except Exception:
        return False

# -------------------------
# API keys (simple)
# -------------------------
def generate_api_key(prefix: str = "neura", length: int = 32) -> str:
    """Generate a random API key: <prefix>_<hex>"""
    token = secrets.token_hex(length // 2)
    return f"{prefix}_{token}"

def verify_api_key(api_key: str, allowed_keys: Optional[set] = None) -> bool:
    """
    Verify API key against a provided set of allowed keys.
    If allowed_keys is None, check against ADMIN_TOKEN if set.
    """
    if allowed_keys:
        return api_key in allowed_keys
    if ADMIN_TOKEN and api_key == ADMIN_TOKEN:
        return True
    # as a fallback, allow keys that start with known prefix (not recommended for prod)
    return api_key.startswith("neura_")

# -------------------------
# HMAC timed tokens (stateless)
# -------------------------
def _hmac_sign(msg: bytes, key: bytes) -> str:
    mac = hmac.new(key, msg, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(mac).decode("utf-8").rstrip("=")

def generate_token(payload: str, expires_in: int = 3600) -> str:
    """
    Generate a stateless HMAC token containing: payload|expiry|signature
    payload: short identifier (user id, api_key, etc.)
    expires_in: seconds until expiration
    Result: base64(payload)|expiry|signature
    """
    expiry = int(time.time()) + int(expires_in)
    payload_b64 = base64.urlsafe_b64encode(payload.encode("utf-8")).decode("utf-8").rstrip("=")
    msg = f"{payload_b64}:{expiry}".encode("utf-8")
    sig = _hmac_sign(msg, SECRET_KEY.encode("utf-8"))
    return f"{payload_b64}:{expiry}:{sig}"

def verify_token(token: str) -> Optional[dict]:
    """
    Verify the token and return {'payload': ..., 'expiry': ...} or None.
    """
    try:
        parts = token.split(":")
        if len(parts) != 3:
            return None
        payload_b64, expiry_str, sig = parts
        expiry = int(expiry_str)
        if time.time() > expiry:
            return None
        msg = f"{payload_b64}:{expiry}".encode("utf-8")
        expected_sig = _hmac_sign(msg, SECRET_KEY.encode("utf-8"))
        if not hmac.compare_digest(expected_sig, sig):
            return None
        payload = base64.urlsafe_b64decode(payload_b64 + "==").decode("utf-8")
        return {"payload": payload, "expiry": expiry}
    except Exception:
        return None

# -------------------------
# Flask route decorator
# -------------------------
def require_token(header_name: str = "Authorization", prefix: str = "Bearer ", admin_allowed: bool = True):
    """
    Flask decorator to protect routes.
    Usage:
        @require_token()
        def my_route(): ...
    It checks (in order):
    1) Authorization header Bearer <token> — verifies HMAC token
    2) X-API-KEY header — verifies API key via verify_api_key
    3) If admin_allowed and Authorization Bearer <ADMIN_TOKEN> present, allows
    Returns 401 JSON on failure.
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # 1) Authorization header
            auth = request.headers.get(header_name, "") or request.args.get("auth", "")
            if auth:
                if auth.startswith(prefix):
                    token = auth[len(prefix):].strip()
                    # admin token shortcut
                    if admin_allowed and token == ADMIN_TOKEN and ADMIN_TOKEN:
                        return f(*args, **kwargs)
                    verified = verify_token(token)
                    if verified:
                        # attach to request context (lightweight)
                        request.security = verified
                        return f(*args, **kwargs)
                else:
                    # maybe raw api key
                    key = auth.strip()
                    if verify_api_key(key):
                        request.security = {"api_key": key}
                        return f(*args, **kwargs)

            # 2) X-API-KEY header fallback
            xkey = request.headers.get("X-API-KEY", "") or request.args.get("api_key", "")
            if xkey and verify_api_key(xkey):
                request.security = {"api_key": xkey}
                return f(*args, **kwargs)

            # 3) Admin token via env (unsafe if empty)
            if admin_allowed and ADMIN_TOKEN:
                bearer = request.headers.get("Authorization", "")
                if bearer.startswith(prefix) and bearer[len(prefix):].strip() == ADMIN_TOKEN:
                    return f(*args, **kwargs)

            # rejected
            return jsonify({"ok": False, "error": "unauthorized"}), 401
        return wrapped
    return decorator

# -------------------------
# Utility helpers
# -------------------------
def secure_compare(a: str, b: str) -> bool:
    """Constant-time compare for secrets."""
    try:
        return hmac.compare_digest(a.encode("utf-8"), b.encode("utf-8"))
    except Exception:
        return False

def rotate_secret(new_secret: Optional[str] = None) -> str:
    """
    Rotate the in-memory secret key (useful for testing).
    WARNING: In production, rotate via environment and restart your process.
    """
    global SECRET_KEY
    SECRET_KEY = new_secret or secrets.token_hex(32)
    return SECRET_KEY

# -------------------------
# Quick CLI / demo functions
# -------------------------
if __name__ == "__main__":
    print("security_manager demo")
    pw = "test-password"
    h = hash_password(pw)
    print("hashed:", h)
    print("verify:", verify_password(pw, h))
    ak = generate_api_key()
    print("api_key:", ak)
    token = generate_token("user:alice", expires_in=3600)
    print("token:", token)
    print("verify token:", verify_token(token))