"""
api_key_manager.py
Load, validate, and rotate API keys safely.
"""

api_keys = {
    "openai": "FAKE_OPENAI_KEY",
    "local_ai": "LOCAL_KEY_123"
}

def get_key(service_name: str) -> str:
    return api_keys.get(service_name, "")

# Example
if __name__ == "__main__":
    print(get_key("openai"))