"""
emoji_replacer.py
Independent text-to-emoji conversion.
"""

EMOJI_MAP = {
    ":smile:": "😄",
    ":heart:": "❤️",
    ":fire:": "🔥",
    ":star:": "⭐",
}

def replace_emojis(text: str) -> str:
    for k, v in EMOJI_MAP.items():
        text = text.replace(k, v)
    return text