CONFIG = {"theme": "dark", "notifications": True}
def get_config(key: str):
    return CONFIG.get(key)