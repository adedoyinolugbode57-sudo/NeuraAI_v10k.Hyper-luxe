# utils.py
import json
import logging
import time
from datetime import datetime, timedelta

CONFIG_FILE = "config.json"

def load_config(file_path, default_config=None):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception:
        logging.warning(f"Config not found. Using default config.")
        return default_config or {}

def save_config(file_path, config_data):
    try:
        with open(file_path, "w") as f:
            json.dump(config_data, f, indent=4)
        return True
    except Exception as e:
        logging.error(f"Failed to save config: {e}")
        return False

# ---------------- Premium Logic ----------------
def is_premium(user_id, config_data):
    """Check if a user has premium access"""
    premium_users = config_data.get("premium_users", {})
    # premium_users dict: {user_id: expiry_timestamp}
    if user_id in premium_users:
        expiry = datetime.fromisoformat(premium_users[user_id])
        if expiry > datetime.utcnow():
            return True
        else:
            # Premium expired, remove
            del premium_users[user_id]
            save_config(CONFIG_FILE, config_data)
    return False

def add_premium(user_id, days=30):
    """Grant premium for a specific number of days"""
    config_data = load_config(CONFIG_FILE)
    expiry = datetime.utcnow() + timedelta(days=days)
    if "premium_users" not in config_data:
        config_data["premium_users"] = {}
    config_data["premium_users"][user_id] = expiry.isoformat()
    save_config(CONFIG_FILE, config_data)
    logging.info(f"Granted premium to {user_id} until {expiry}")
    return True

def format_response(text, theme, premium=False):
    """Format chatbot response with theme & premium badge"""
    badge = "💎 " if premium else ""
    formatted = f"[{theme.upper()}]{badge}{text}"
    return formatted