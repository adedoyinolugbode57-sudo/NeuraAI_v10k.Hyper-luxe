from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import random
import time

app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app)

# Simple AI engine (placeholder for full GPT-based logic)
responses = {
    "hello": [
        "Hi there 👋! I'm NeuraAI v10k Hyperluxe, your premium AI companion.",
        "Hey 👋, great to see you here on NeuraAI v10k!",
        "Welcome back 😎! Ready to explore the Hyperluxe world?"
    ],
    "bye": [
        "Goodbye 👋! Come back soon to your NeuraAI lounge.",
        "Farewell 🚀 — may your ideas shine bright!",
        "Take care 🌈 — the Hyperluxe AI awaits your return!"
    ],
    "thanks": [
        "You're most welcome 💫!",
        "Anytime 😄! I'm always here to help.",
        "Glad to assist 🌟!"
    ],
    "default": [
        "Interesting 🤔, could you tell me more?",
        "That's fascinating 😃!",
        "Let’s dive deeper — I love where this is going 😎!"
    ]
}

@app.route('/')
def index():
    return render_template('chat_interface.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").lower().strip()
    
    # Simulate "thinking"
    time.sleep(random.uniform(0.2, 0.5))

    # Basic keyword matching
    if "hello" in user_message:
        reply = random.choice(responses["hello"])
    elif "bye" in user_message:
        reply = random.choice(responses["bye"])
    elif "thank" in user_message:
        reply = random.choice(responses["thanks"])
    else:
        reply = random.choice(responses["default"])
    
    return jsonify({"reply": reply})

@app.route('/voice')
def voice():
    return jsonify({"status": "Voice engine active 🔊"})

@app.route('/status')
def status():
    return jsonify({"status": "✅ NeuraAI v10k Hyperluxe is live and ready!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)