# rewards_system.py
"""
Rewards System for NeuraAI_v10k.HyperLuxe
Gamification module: XP, levels, badges, daily streaks, and bonuses.
"""

import json
import math
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    from database import db
except Exception:
    db = None

REWARDS_FILE = Path(__file__).parent / "data" / "rewards.json"
REWARDS_FILE.parent.mkdir(parents=True, exist_ok=True)

BADGES = [
    {"name": "Bronze", "xp": 0},
    {"name": "Silver", "xp": 1000},
    {"name": "Gold", "xp": 5000},
    {"name": "Platinum", "xp": 10000},
    {"name": "Diamond", "xp": 20000},
]

def load_rewards():
    if not REWARDS_FILE.exists():
        return {"users": {}}
    return json.loads(REWARDS_FILE.read_text(encoding="utf-8"))

def save_rewards(data):
    REWARDS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

def _get_user_data(uid: str) -> dict:
    data = load_rewards()
    return data["users"].setdefault(uid, {"xp": 0, "level": 1, "badge": "Bronze", "streak": 0, "last_active": None})

def _level_formula(xp: int) -> int:
    """Quadratic growth formula."""
    return int(math.sqrt(xp / 100)) + 1

def _get_badge(xp: int) -> str:
    current = "Bronze"
    for b in BADGES:
        if xp >= b["xp"]:
            current = b["name"]
    return current

def add_xp(uid: str, amount: int) -> dict:
    data = load_rewards()
    user = _get_user_data(uid)
    user["xp"] += amount
    user["level"] = _level_formula(user["xp"])
    user["badge"] = _get_badge(user["xp"])
    user["last_active"] = datetime.utcnow().isoformat()
    data["users"][uid] = user
    save_rewards(data)
    return user

def update_streak(uid: str) -> dict:
    data = load_rewards()
    user = _get_user_data(uid)
    today = datetime.utcnow().date()
    last = None
    if user["last_active"]:
        try:
            last = datetime.fromisoformat(user["last_active"]).date()
        except Exception:
            last = None
    if last == today:
        # already counted
        pass
    elif last == today - timedelta(days=1):
        user["streak"] += 1
    else:
        user["streak"] = 1
    user["last_active"] = datetime.utcnow().isoformat()
    # Add small bonus XP
    user["xp"] += 20 * user["streak"]
    user["level"] = _level_formula(user["xp"])
    user["badge"] = _get_badge(user["xp"])
    data["users"][uid] = user
    save_rewards(data)
    return user

def get_rank(uid: str) -> str:
    user = _get_user_data(uid)
    return f"Level {user['level']} • {user['badge']} Badge • XP: {user['xp']}"

def claim_daily_bonus(uid: str) -> dict:
    data = load_rewards()
    user = _get_user_data(uid)
    now = datetime.utcnow()
    if user.get("last_bonus"):
        last = datetime.fromisoformat(user["last_bonus"])
        if (now - last).days < 1:
            return {"error": "already_claimed"}
    bonus = 100 + user["streak"] * 10
    user["xp"] += bonus
    user["last_bonus"] = now.isoformat()
    user["badge"] = _get_badge(user["xp"])
    data["users"][uid] = user
    save_rewards(data)
    return {"ok": True, "bonus": bonus, "xp": user["xp"], "badge": user["badge"]}

def top_users(limit=10) -> list:
    data = load_rewards()
    users = list(data["users"].items())
    users.sort(key=lambda kv: kv[1]["xp"], reverse=True)
    return [{"uid": u, "xp": info["xp"], "level": info["level"], "badge": info["badge"]} for u, info in users[:limit]]

def reset_rewards():
    REWARDS_FILE.write_text(json.dumps({"users": {}}, indent=2), encoding="utf-8")

if __name__ == "__main__":
    # Example use
    uid = "user_test123"
    add_xp(uid, 300)
    update_streak(uid)
    print(get_rank(uid))
    print(top_users())