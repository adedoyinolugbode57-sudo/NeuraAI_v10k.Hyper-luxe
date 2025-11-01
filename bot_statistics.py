"""
bot_statistics.py
Track basic stats of chatbot usage.
"""

STATS = {
    "messages_processed": 0,
    "active_users": set()
}

def log_message(user_id: str):
    STATS["messages_processed"] += 1
    STATS["active_users"].add(user_id)

def get_stats():
    return {
        "messages_processed": STATS["messages_processed"],
        "active_users_count": len(STATS["active_users"])
    }