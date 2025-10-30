"""
admin_panel.py
Neura-AI v10k.Hyperluxe
---------------------------------------
Admin panel for monitoring, analytics, and control
of the entire AI assistant ecosystem.
"""

import os
import json
import time
import random
import platform
import psutil
from datetime import datetime
from functools import wraps
from flask import Flask, request, jsonify, render_template, redirect, url_for, session

# --------------------------------------------------
# Configuration
# --------------------------------------------------
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "neura-admin-2025")
CHAT_LOGS_PATH = "chat_logs.json"
USER_PREFS_PATH = "user_profiles.json"
MEMORY_PATH = "memory_store.json"
IDEAS_PATH = "ideas_roadmap.json"

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "neura_secret_key_2025")

# --------------------------------------------------
# Utility Functions
# --------------------------------------------------
def _read_json(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def _timestamp():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

def _system_info():
    """Collect live system statistics."""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "platform": platform.system(),
        "uptime": time.strftime("%H:%M:%S", time.gmtime(time.time())),
        "timestamp": _timestamp(),
    }

# --------------------------------------------------
# Auth Middleware
# --------------------------------------------------
def require_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = session.get("admin_token") or request.headers.get("Authorization")
        if token == f"Bearer {ADMIN_TOKEN}" or token == ADMIN_TOKEN:
            return func(*args, **kwargs)
        return jsonify({"error": "Unauthorized access"}), 403
    return wrapper

# --------------------------------------------------
# Admin Routes
# --------------------------------------------------
@app.route("/admin/login", methods=["POST"])
def login_admin():
    data = request.get_json() or {}
    token = data.get("token")
    if token == ADMIN_TOKEN:
        session["admin_token"] = token
        return jsonify({"message": "✅ Admin logged in successfully"})
    return jsonify({"error": "Invalid token"}), 403


@app.route("/admin/dashboard", methods=["GET"])
@require_admin
def dashboard():
    """Render a beautiful admin dashboard."""
    chat_logs = _read_json(CHAT_LOGS_PATH).get("history", [])
    users = _read_json(USER_PREFS_PATH)
    ideas = _read_json(IDEAS_PATH)
    sys_info = _system_info()

    stats = {
        "total_users": len(users),
        "total_chats": len(chat_logs),
        "cpu_usage": sys_info["cpu_percent"],
        "memory_usage": sys_info["memory_percent"],
        "system": sys_info["platform"],
        "uptime": sys_info["uptime"],
        "ideas_count": len(ideas) if isinstance(ideas, dict) else 0,
    }

    # Lightweight inline HTML dashboard
    html = f"""
    <html>
    <head>
      <title>Neura-AI Admin Panel</title>
      <style>
        body {{
          background: linear-gradient(135deg, #020024 0%, #090979 35%, #00d4ff 100%);
          font-family: 'Poppins', sans-serif;
          color: white;
          text-align: center;
          padding: 40px;
        }}
        .stat-card {{
          background: rgba(255, 255, 255, 0.1);
          border-radius: 20px;
          margin: 15px auto;
          padding: 20px;
          width: 300px;
          backdrop-filter: blur(10px);
        }}
        .title {{
          font-size: 2em;
          margin-bottom: 20px;
        }}
        .btn {{
          background: #00d4ff;
          color: black;
          border: none;
          padding: 10px 25px;
          border-radius: 10px;
          cursor: pointer;
          font-weight: bold;
        }}
        .btn:hover {{
          background: #07a0c3;
        }}
      </style>
    </head>
    <body>
      <div class="title">💼 Neura-AI v10k Hyperluxe Admin Panel</div>
      <div class="stat-card"><b>Total Users:</b> {stats['total_users']}</div>
      <div class="stat-card"><b>Total Conversations:</b> {stats['total_chats']}</div>
      <div class="stat-card"><b>CPU Usage:</b> {stats['cpu_usage']}%</div>
      <div class="stat-card"><b>Memory Usage:</b> {stats['memory_usage']}%</div>
      <div class="stat-card"><b>Ideas Registered:</b> {stats['ideas_count']}</div>
      <div class="stat-card"><b>System:</b> {stats['system']} | Uptime: {stats['uptime']}</div>
      <form method="post" action="/admin/clear_memory">
        <button class="btn">🧹 Clear Memory</button>
      </form>
      <form method="post" action="/admin/export_backup">
        <button class="btn">📦 Export Backup</button>
      </form>
    </body>
    </html>
    """
    return html


@app.route("/admin/clear_memory", methods=["POST"])
@require_admin
def clear_memory():
    _write_json(MEMORY_PATH, {"context": []})
    _write_json(CHAT_LOGS_PATH, {"history": []})
    return jsonify({"message": "🧠 Memory and logs cleared successfully."})


@app.route("/admin/export_backup", methods=["POST"])
@require_admin
def export_backup():
    data = {
        "chat_logs": _read_json(CHAT_LOGS_PATH),
        "memory": _read_json(MEMORY_PATH),
        "user_prefs": _read_json(USER_PREFS_PATH),
        "timestamp": _timestamp()
    }
    backup_name = f"backup_{int(time.time())}.json"
    _write_json(backup_name, data)
    return jsonify({"message": "📦 Backup created.", "file": backup_name})


@app.route("/admin/stats", methods=["GET"])
@require_admin
def get_stats():
    sys_info = _system_info()
    chat_count = len(_read_json(CHAT_LOGS_PATH).get("history", []))
    user_count = len(_read_json(USER_PREFS_PATH))
    return jsonify({
        "system": sys_info,
        "total_chats": chat_count,
        "total_users": user_count,
    })


@app.route("/admin/add_idea", methods=["POST"])
@require_admin
def add_idea():
    """Add development ideas to roadmap."""
    data = request.get_json() or {}
    idea = data.get("idea")
    desc = data.get("description", "No description provided.")
    ideas = _read_json(IDEAS_PATH)
    ideas[str(int(time.time()))] = {"idea": idea, "description": desc, "timestamp": _timestamp()}
    _write_json(IDEAS_PATH, ideas)
    return jsonify({"message": "💡 Idea added successfully."})


@app.route("/admin/users", methods=["GET"])
@require_admin
def get_users():
    """List all users and their preferences."""
    users = _read_json(USER_PREFS_PATH)
    return jsonify(users)

@app.route("/admin/delete_user/<user_id>", methods=["DELETE"])
@require_admin
def delete_user(user_id):
    """Remove user data manually."""
    users = _read_json(USER_PREFS_PATH)
    if user_id in users:
        del users[user_id]
        _write_json(USER_PREFS_PATH, users)
        return jsonify({"message": f"🧍 User {user_id} deleted."})
    return jsonify({"error": "User not found."}), 404


@app.route("/admin/health", methods=["GET"])
@require_admin
def system_health():
    """Check live system health."""
    info = _system_info()
    return jsonify({"status": "OK", "system_info": info})

# --------------------------------------------------
# Standalone Execution
# --------------------------------------------------
if __name__ == "__main__":
    print("🚀 Neura-AI Admin Panel Ready at http://localhost:8000/admin/dashboard")
    app.run(host="0.0.0.0", port=8000)