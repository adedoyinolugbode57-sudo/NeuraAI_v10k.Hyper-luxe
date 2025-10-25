"""
voice_routes.py (v3.0)
NeuraAI v10k Hyperluxe — Interactive Voice Assistant Routes
Created by ChatGPT + Joshua Dav
Supports multilingual voice input, real-time text-to-speech, and mood adaptation.
"""

import os, time, json, random
from flask import Blueprint, request, jsonify
from ai_engine import generate_reply
from ai_voice_assistant import speak_text
from ai_memory import remember
from googletrans import Translator

voice_bp = Blueprint("voice_routes", __name__)

LOG_FILE = "voice_logs.json"
translator = Translator()

# 🔐 Ensure voice log file exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, indent=2)

# 🧠 Mood states — the assistant changes tone dynamically
MOODS = {
    "cheerful": ["😊", "🌞", "🎉", "🌈"],
    "calm": ["🌿", "💤", "🫖"],
    "serious": ["💼", "📘", "🧠"],
    "romantic": ["💖", "🌹", "✨"],
    "curious": ["🤔", "🔍", "🧩"]
}

def log_voice_interaction(user_msg, ai_msg, mood):
    with open(LOG_FILE, "r+", encoding="utf-8") as f:
        data = json.load(f)
        data.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "user": user_msg,
            "ai": ai_msg,
            "mood": mood
        })
        f.seek(0)
        json.dump(data[-200:], f, indent=2)

def detect_mood(text: str) -> str:
    text = text.lower()
    if any(k in text for k in ["love", "beautiful", "sweet"]):
        return "romantic"
    if any(k in text for k in ["how", "why", "what", "who"]):
        return "curious"
    if any(k in text for k in ["work", "project", "study"]):
        return "serious"
    if any(k in text for k in ["relax", "calm", "sleep"]):
        return "calm"
    return "cheerful"

@voice_bp.route("/voice_chat", methods=["POST"])
def voice_chat():
    data = request.get_json()
    message = data.get("message", "").strip()
    lang = data.get("language", "en")

    if not message:
        return jsonify({"error": "empty_message"}), 400

    # 🌍 Translate input to English for consistent AI processing
    translated_text = translator.translate(message, src=lang, dest="en").text

    # 🤖 Generate AI reply using core engine
    ai_reply = generate_reply(translated_text)

    # 💬 Translate back to user language
    localized_reply = translator.translate(ai_reply, src="en", dest=lang).text

    # 😄 Adaptive mood system
    mood = detect_mood(ai_reply)
    emoji = random.choice(MOODS[mood])
    mood_reply = f"{localized_reply} {emoji}"

    # 🧠 Memory logging
    remember("user", message)
    remember("ai", mood_reply)
    log_voice_interaction(message, mood_reply, mood)

    # 🔊 Text-to-speech (optional)
    audio_file = speak_text(mood_reply, lang)

    return jsonify({
        "reply": mood_reply,
        "audio": audio_file,
        "mood": mood,
        "language": lang
    })

@voice_bp.route("/voice_moods", methods=["GET"])
def voice_moods():
    return jsonify({"available_moods": list(MOODS.keys()), "count": len(MOODS)})

@voice_bp.route("/voice_status", methods=["GET"])
def voice_status():
    return jsonify({
        "status": "🟢 Voice Engine Online",
        "supported_languages": 150,
        "moods": list(MOODS.keys()),
        "engine": "NeuraAI v10k Hyperluxe Voice System"
    })