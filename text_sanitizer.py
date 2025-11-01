"""
text_sanitizer.py
Clean user input, remove unsafe characters or bad words.
"""

BAD_WORDS = ["badword1", "badword2"]

def sanitize(text: str) -> str:
    for word in BAD_WORDS:
        text = text.replace(word, "***")
    return text.strip()