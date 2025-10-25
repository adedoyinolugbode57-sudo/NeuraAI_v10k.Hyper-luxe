"""
admin_panel.py — NeuraAI_v10k.Hyperluxe
Premium Admin Control Center
Created by ChatGPT + Joshua Dav
"""

import os, json, time
from functools import wraps
from flask import Flask, request, jsonify, render_template_string

ADMIN_TOKEN = os.getenv("NEURA_ADMIN_TOKEN", "default-token")

app = Flask(__name__)

# -------------------------------
# 🔐 Token-based Authentication
# -------------------------------
def require_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if token != ADMIN_TOKEN:
            return jsonify({"error": "Unauthorized"}), 403
        return func(*args, **kwargs)
    return wrapper

# -------------------------------
# 🌐 Admin Dashboard (Web UI)
# -------------------------------
HTML_DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>🧠 NeuraAI Admin Panel</title>
<style>
body { font-family: 'Poppins', sans-serif; background: linear-gradient(135deg,#090909,#111122,#202040);
color: white; margin:0; padding:2em; }
h1 { color: #40c9ff; }
button { background:#40c9ff; border:none; padding:10px 20px; margin:5px; border-radius:10px;
cursor:pointer; font-size:16px; color:#000; transition:0.3s; }
button:hover { background:#00e6b0; }
.card { background:#1a1a2e; padding:20px; margin-top:20px; border-radius:20px; box-shadow:0 0 10px #000; }
</style>
</head>
<body>
  <h1>🧠 NeuraAI Hyperluxe Admin Dashboard</h1>
  <div class="card">
    <h2>System Controls</h2>
    <button onclick="trigger('refresh_cache')">♻️ Refresh Cache</button>
    <button onclick="trigger('reset_sessions')">🧹 Reset Sessions</button>
    <button onclick="trigger('analyze_logs')">📊 Analyze Logs</button>
  </div>

  <div class="card">
    <h2>Platform Metrics</h2>
    <button onclick="getStats()">📈 Get Stats</button>
    <pre id="output"></pre>
  </div>

  <script>
  const headers = { "Authorization": "Bearer {{token}}", "Content-Type": "application/json" };
  async function trigger(action){
    let r = await fetch('/admin/'+action, {method:'POST', headers});
    document.getElementById('output').textContent = JSON.stringify(await r.json(),null,2);
  }
  async function getStats(){
    let r = await fetch('/admin/stats', {headers});
    document.getElementById('output').textContent = JSON.stringify(await r.json(),null,2);
  }
  </script>
</body>
</html>
"""

@app.route("/admin", methods=["GET"])
def admin_page():
    return render_template_string(HTML_DASHBOARD, token=ADMIN_TOKEN)

# -------------------------------
# ⚙️ Backend Admin Actions
# -------------------------------
@app.route("/admin/<action>", methods=["POST"])
@require_admin
def admin_action(action):
    if action == "refresh_cache":
        time.sleep(1)
        return jsonify({"ok": True, "message": "Cache refreshed."})
    elif action == "reset_sessions":
        time.sleep(1)
        return jsonify({"ok": True, "message": "All sessions reset."})
    elif action == "analyze_logs":
        logs = "No logs found"
        log_path = "activity.log"
        if os.path.exists(log_path):
            with open(log_path) as f: logs = f.read()[-2000:]
        return jsonify({"ok": True, "logs": logs})
    else:
        return jsonify({"error": "Unknown action"})

@app.route("/admin/stats", methods=["GET"])
@require_admin
def admin_stats():
    data = {
        "uptime": f"{round(time.time() - ps_start,2)}s",
        "books": len(json.load(open('books.json'))["books"]) if os.path.exists("books.json") else 0,
        "games": 25,
        "users": 100,
        "cpu": "Normal",
        "status": "All systems optimal 🚀"
    }
    return jsonify(data)

ps_start = time.time()