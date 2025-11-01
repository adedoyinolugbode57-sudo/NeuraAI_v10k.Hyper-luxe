"""
context_cache.py
Cache recent chat context for faster recall.
"""

context_store = {}

def save_context(user_id: str, context: str):
    context_store[user_id] = context

def get_context(user_id: str) -> str:
    return context_store.get(user_id, "")

# Example
if __name__ == "__main__":
    save_context("user123", "Previous conversation text")
    print(get_context("user123"))