"""
emoji_utils.py
Independent emoji utilities for Neuraluxe-AI.
"""
EMOJIS = {
    "smile": "😄",
    "thinking": "🤔",
    "fire": "🔥",
    "star": "⭐",
}

def get_emoji(name: str):
    return EMOJIS.get(name, "")