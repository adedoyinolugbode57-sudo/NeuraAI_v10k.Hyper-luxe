MOODS = {}

def log_mood(user_id: str, mood: str):
    MOODS.setdefault(user_id, []).append(mood)

def get_recent_mood(user_id: str):
    return MOODS.get(user_id, [])[-1] if user_id in MOODS else "neutral"