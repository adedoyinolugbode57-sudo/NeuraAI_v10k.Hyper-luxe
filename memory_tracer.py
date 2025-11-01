MEMORY_DB = {}

def save_memory(user_id: str, message: str):
    MEMORY_DB.setdefault(user_id, []).append(message)

def recall_memory(user_id: str) -> list:
    return MEMORY_DB.get(user_id, [])