# feedback_portal.py — NeuraAI_v10k.Hyperluxe
# Handles user feedback, feature requests, and satisfaction ratings
# Works with PostgreSQL or fallback JSON logging

from flask import Blueprint, request, jsonify
from datetime import datetime
import os, json
from dotenv import load_dotenv
import psycopg2

load_dotenv()
feedback_bp = Blueprint("feedback", __name__)

# PostgreSQL database connection (optional)
DB_URL = os.getenv("DATABASE_URL")
USE_DB = bool(DB_URL)

# Fallback path if database isn’t available
FEEDBACK_LOG = "feedback_logs.json"

def save_to_json(data):
    """Save feedback entries locally if no DB is connected"""
    if not os.path.exists(FEEDBACK_LOG):
        with open(FEEDBACK_LOG, "w") as f:
            json.dump([], f, indent=2)
    with open(FEEDBACK_LOG, "r+") as f:
        existing = json.load(f)
        existing.append(data)
        f.seek(0)
        json.dump(existing, f, indent=2)

def save_to_postgres(data):
    """Save feedback directly into PostgreSQL"""
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id SERIAL PRIMARY KEY,
                username TEXT,
                rating INTEGER,
                category TEXT,
                message TEXT,
                timestamp TIMESTAMP
            )
        """)
        cur.execute("""
            INSERT INTO feedback (username, rating, category, message, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        """, (data["username"], data["rating"], data["category"], data["message"], data["timestamp"]))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("DB Save Error:", e)
        return False

@feedback_bp.route("/api/feedback", methods=["POST"])
def submit_feedback():
    """Receive feedback from frontend or chatbot"""
    data = request.get_json() or {}
    entry = {
        "username": data.get("username", "Guest"),
        "rating": int(data.get("rating", 5)),
        "category": data.get("category", "general"),
        "message": data.get("message", ""),
        "timestamp": datetime.utcnow().isoformat()
    }

    if USE_DB and save_to_postgres(entry):
        return jsonify({"status": "success", "source": "database"}), 200
    else:
        save_to_json(entry)
        return jsonify({"status": "success", "source": "local"}), 200

@feedback_bp.route("/api/feedback/all", methods=["GET"])
def get_feedback():
    """Admin-only: retrieve all feedback"""
    token = request.headers.get("Authorization")
    admin_token = os.getenv("ADMIN_TOKEN", "neura-admin-2025")
    if token != f"Bearer {admin_token}":
        return jsonify({"error": "Unauthorized"}), 403

    if USE_DB:
        try:
            conn = psycopg2.connect(DB_URL)
            cur = conn.cursor()
            cur.execute("SELECT username, rating, category, message, timestamp FROM feedback ORDER BY id DESC")
            records = cur.fetchall()
            cur.close()
            conn.close()
            return jsonify([{
                "username": r[0], "rating": r[1], "category": r[2],
                "message": r[3], "timestamp": str(r[4])
            } for r in records]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        if not os.path.exists(FEEDBACK_LOG):
            return jsonify([])
        with open(FEEDBACK_LOG, "r") as f:
            return jsonify(json.load(f)), 200

@feedback_bp.route("/api/feedback/stats", methods=["GET"])
def feedback_stats():
    """View average rating and total submissions"""
    try:
        if USE_DB:
            conn = psycopg2.connect(DB_URL)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*), AVG(rating) FROM feedback")
            total, avg_rating = cur.fetchone()
            cur.close()
            conn.close()
        else:
            with open(FEEDBACK_LOG, "r") as f:
                feedback = json.load(f)
            total = len(feedback)
            avg_rating = sum([f["rating"] for f in feedback]) / total if total else 0

        return jsonify({
            "total_feedback": total,
            "average_rating": round(avg_rating, 2)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500