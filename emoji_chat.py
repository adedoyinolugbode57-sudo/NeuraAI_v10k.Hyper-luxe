# emoji_chat.py
"""
Emoji & Memory Chat Module — independent and extended
Supports dynamic emoji lookup using the emoji library.
"""

from flask import Flask, request, jsonify
import os
import emoji  # pip install emoji

app = Flask(__name__)

conversation_memory = {}

def find_emoji(keyword: str) -> str:
    """Return a single emoji for a given keyword alias if possible."""
    try:
        # convert alias like ":rocket:" into actual emoji
        alias = f":{keyword.lower().replace(' ', '_')}:"
        char = emoji.emojize(alias, language='alias')
        # if alias not found, emojize returns alias itself
        if char == alias:
            return ""
        return char
    except Exception:
        return ""

@app.route("/chat/<user_id>", methods=["POST"])
def chat(user_id):
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "No message provided."}), 400

    if user_id not in conversation_memory:
        conversation_memory[user_id] = []

    conversation_memory[user_id].append({"user": message})

    # Example: pick an emoji based on a simple keyword check
    emo = ""
    if "happy" in message.lower():
        emo = find_emoji("smile")
    elif "sad" in message.lower():
        emo = find_emoji("cry")
    elif "rocket" in message.lower():
        emo = find_emoji("rocket")

    response_text = f"I remember you said: '{message}' {emo or find_emoji('star')}"
    conversation_memory[user_id].append({"bot": response_text})

    return jsonify({
        "response": response_text,
        "memory_count": len(conversation_memory[user_id]),
    })

@app.route("/chat/<user_id>/memory", methods=["GET"])
def view_memory(user_id):
    memory = conversation_memory.get(user_id, [])
    return jsonify(memory)

@app.route("/emoji/<keyword>", methods=["GET"])
def get_emoji(keyword):
    return jsonify({"emoji": find_emoji(keyword)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10001)))