PREFS = {}
def set_preference(user_id: str, key: str, value: str):
    PREFS[f"{user_id}_{key}"] = value
    return f"Preference {key} set for {user_id}"