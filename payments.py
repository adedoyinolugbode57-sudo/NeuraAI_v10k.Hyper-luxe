# 💎 payments.py — Neuraluxe-AI Premium (Final Version)
# Handles subscription login and Opay-based payment verification
# © 2025 Neuraluxe Technologies. All Rights Reserved.

import os
import time
from flask import Flask, jsonify, request
from dotenv import load_dotenv

# ----------------------------
# 🌐 Environment Setup
# ----------------------------
load_dotenv()

OPAY_ACCOUNT = os.getenv("OPAY_ACCOUNT_NUMBER", "0000000000")
OPAY_API_KEY = os.getenv("OPAY_API_KEY", "demo_key")
DEFAULT_SUBSCRIPTION = float(os.getenv("DEFAULT_SUBSCRIPTION", 19.99))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
LOCK_DURATION = int(os.getenv("LOCK_DURATION", 86400))  # 24h default

# ----------------------------
# 🧍 Mock Database
# ----------------------------
users_db = {
    "adedoyinolugbode57@gmail.com": {
        "is_free": True,
        "transactions": 0,
        "locked_until": 0,
    }
}

# ----------------------------
# 💰 Payment Verification Logic
# ----------------------------
def verify_payment_opay(user_email, amount):
    """
    Replace this mock with the actual Opay API integration.
    Returns True if the payment is confirmed 100%.
    """
    # Free account bypass
    if users_db.get(user_email, {}).get("is_free", False):
        return True

    # TODO: Integrate Opay API real check here using OPAY_API_KEY
    # Example:
    # response = requests.get("https://api.opay.com/payments/status", headers={...})
    # return response.json().get("status") == "confirmed"

    # Mock success for demonstration
    return True

# ----------------------------
# 🚀 Login & Subscription Handler
# ----------------------------
def login_user(user_email, amount=DEFAULT_SUBSCRIPTION):
    current_time = time.time()

    if user_email not in users_db:
        users_db[user_email] = {
            "is_free": False,
            "transactions": 0,
            "locked_until": 0,
        }

    user = users_db[user_email]

    # If locked
    if current_time < user["locked_until"]:
        remaining = int(user["locked_until"] - current_time)
        return f"🚫 Account locked. Try again in {remaining // 3600}h {(remaining % 3600) // 60}m."

    # Payment check
    if verify_payment_opay(user_email, amount):
        user["transactions"] = 0
        user["locked_until"] = 0
        return success_message(user_email)
    else:
        user["transactions"] += 1
        if user["transactions"] >= MAX_RETRIES:
            user["locked_until"] = current_time + LOCK_DURATION
            user["transactions"] = 0
            return "⚠️ Payment failed 3 times. Account locked for 24 hours."
        else:
            remaining_attempts = MAX_RETRIES - user["transactions"]
            return f"❌ Payment failed. {remaining_attempts} retry(s) left."

# ----------------------------
# ✨ Premium Success Message
# ----------------------------
def success_message(user_email):
    return f"""
🎉 Welcome to Neuraluxe-AI Premium, {user_email}!
Your subscription is active — explore infinite intelligence. 💫
🧠 Enjoy full access to AI voice, learning, marketplace, and automation tools.
"""

# ----------------------------
# 🌐 Flask API (Independent)
# ----------------------------
app = Flask(__name__)

@app.route("/pay", methods=["POST"])
def pay():
    data = request.get_json(force=True)
    email = data.get("email")
    amount = float(data.get("amount", DEFAULT_SUBSCRIPTION))
    message = login_user(email, amount)
    return jsonify({"user": email, "message": message})

# ----------------------------
# 🧪 Local Test (Optional)
# ----------------------------
if __name__ == "__main__":
    print("🚀 Neuraluxe-AI Payment System Running on http://127.0.0.1:5001")
    app.run(port=5001, debug=True)