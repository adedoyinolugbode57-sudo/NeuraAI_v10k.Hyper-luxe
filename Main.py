# main.py
# NeuraAI_v10k.Hyperluxe - Full $10M premium AI chatbot web service
# Flask + GPT-3/5 + Mini-games + Voice + Themes + Premium + Analytics + Social Feed

import os
import json
import logging
import time
from threading import Thread
from functools import wraps
from datetime import datetime

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# --- Local module imports ---
try:
    from ai_engine import generate_response
    from ai_memory import get_memory, store_memory
    from ai_voice_assistant import play_voice, get_voice_options
    from mini_games import launch_game, get_game_list
    from utils import load_config, save_config, is_premium, add_premium, format_response
    from updater import check_updates, auto_update, schedule_auto_update
    from theme_engine import apply_theme
    from user_profiles import get_user_profile
    from analytics_routes import log_usage, log_error
    import social_feed
except ImportError as e:
    print(f"Module import warning: {e}")

# --- Flask app setup ---
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# --- Config ---
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "openai_api_key": "YOUR_OPENAI_API_KEY",
    "premium_users": {},
    "themes": ["neon", "dark", "light"],
    "default_theme": "neon"
}
config = load_config(CONFIG_FILE, DEFAULT_CONFIG)

# --- Helper decorators ---
def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        if not api_key or api_key != config["openai_api_key"]:
            return jsonify({"error": "Invalid or missing API key"}), 401
        return func(*args, **kwargs)
    return wrapper

# --- Startup background tasks ---
def startup_tasks():
    logging.info("Starting background tasks...")
    check_updates()
    schedule_auto_update(interval_hours=24)

Thread(target=startup_tasks, daemon=True).start()

# --- Routes ---

@app.route("/")
def home():
    return jsonify({"message": "Welcome to NeuraAI_v10k.Hyperluxe - $10M chatbot!"})

# --- Chatbot ---
@app.route("/chat", methods=["POST"])
@require_api_key
def chat():
    data = request.get_json()
    user_id = data.get("user_id", "guest")
    message = data.get("message", "")
    theme = data.get("theme", config.get("default_theme"))

    if not message:
        return jsonify({"error": "No message provided"}), 400

    premium = is_premium(user_id, config)
    memory = get_memory(user_id)
    prompt = f"{memory}\nUser: {message}\nAI:"

    try:
        response_text = generate_response(prompt)
        store_memory(user_id, message, response_text)
        formatted = format_response(response_text, theme, premium)
        log_usage(user_id, "chat", message)
        return jsonify({"response": formatted, "theme": theme, "premium": premium})
    except Exception as e:
        log_error(user_id, "chat", str(e))
        return jsonify({"error": "Chatbot error"}), 500

# --- Voice Assistant ---
@app.route("/voice", methods=["POST"])
@require_api_key
def voice():
    data = request.get_json()
    user_id = data.get("user_id", "guest")
    text = data.get("text", "")
    voice_type = data.get("voice_type", "male")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    if voice_type not in get_voice_options():
        return jsonify({"error": f"Invalid voice type. Options: {get_voice_options()}"}), 400

    audio_url = play_voice(text, voice_type)
    log_usage(user_id, "voice", text)
    return jsonify({"audio_url": audio_url, "voice_type": voice_type})

# --- Mini-games ---
@app.route("/game", methods=["POST"])
@require_api_key
def game():
    data = request.get_json()
    user_id = data.get("user_id", "guest")
    game_name = data.get("game_name", "")
    premium = is_premium(user_id, config)

    if not game_name:
        return jsonify({"available_games": get_game_list(), "premium": premium})

    if game_name not in get_game_list():
        return jsonify({"error": f"Game '{game_name}' not found"}), 404

    try:
        game_result = launch_game(game_name, user_id, premium)
        log_usage(user_id, "game", game_name)
        return jsonify({"game_name": game_name, "result": game_result, "premium": premium})
    except Exception as e:
        log_error(user_id, "game", str(e))
        return jsonify({"error": "Game error"}), 500

# --- Theme ---
@app.route("/theme", methods=["POST"])
@require_api_key
def theme():
    data = request.get_json()
    user_id = data.get("user_id", "guest")
    new_theme = data.get("theme", "")

    if new_theme not in config.get("themes", []):
        return jsonify({"error": f"Invalid theme. Options: {config.get('themes', [])}"}), 400

    apply_theme(user_id, new_theme)
    log_usage(user_id, "theme_change", new_theme)
    return jsonify({"message": f"Theme changed to {new_theme}", "theme": new_theme})

# --- Premium Check ---
@app.route("/premium-check", methods=["GET"])
@require_api_key
def premium_check():
    user_id = request.args.get("user_id", "guest")
    premium = is_premium(user_id, config)
    return jsonify({"user_id": user_id, "premium": premium})

# --- Add Premium (Admin) ---
@app.route("/premium-add", methods=["POST"])
@require_api_key
def premium_add():
    data = request.get_json()
    user_id = data.get("user_id")
    days = int(data.get("days", 30))

    if not user_id:
        return jsonify({"error": "No user_id provided"}), 400

    add_premium(user_id, days)
    return jsonify({"message": f"{user_id} granted premium for {days} days"})

# --- Auto-update ---
@app.route("/update", methods=["POST"])
@require_api_key
def update():
    try:
        Thread(target=auto_update, daemon=True).start()
        return jsonify({"message": "Update started in background"})
    except Exception as e:
        logging.error(f"Auto-update error: {e}")
        return jsonify({"error": "Failed to start update"}), 500

# --- Analytics ---
@app.route("/analytics", methods=["GET"])
@require_api_key
def analytics():
    try:
        data = analytics_routes.get_report()
        return jsonify({"analytics": data})
    except Exception as e:
        logging.error(f"Analytics error: {e}")
        return jsonify({"error": "Failed to fetch analytics"}), 500

# --- Social Feed ---
@app.route("/social-feed", methods=["GET"])
@require_api_key
def feed():
    try:
        posts = social_feed.get_feed()
        return jsonify({"feed": posts})
    except Exception as e:
        logging.error(f"Social feed error: {e}")
        return jsonify({"error": "Failed to fetch feed"}), 500

# --- Error Handlers ---
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

# --- Run Flask ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logging.info(f"Starting NeuraAI_v10k.Hyperluxe on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)