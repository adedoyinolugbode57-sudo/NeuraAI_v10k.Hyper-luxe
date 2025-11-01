"""
emotion_palette.py
Map text or speech into color-emotion visuals (mock).
"""

import random

EMOTIONS = ["happy", "sad", "angry", "relaxed", "excited", "nostalgic"]
COLORS = {
    "happy": "yellow",
    "sad": "blue",
    "angry": "red",
    "relaxed": "green",
    "excited": "orange",
    "nostalgic": "purple"
}

def detect_emotion(text: str) -> str:
    """Simulate emotion detection."""
    words = text.lower().split()
    if any(w in words for w in ["love", "joy", "fun", "smile"]):
        return "happy"
    if any(w in words for w in ["cry", "lost", "alone", "sad"]):
        return "sad"
    if any(w in words for w in ["mad", "hate", "furious", "angry"]):
        return "angry"
    return random.choice(EMOTIONS)

def emotion_to_color(emotion: str) -> str:
    return COLORS.get(emotion, "gray")

# Example usage
if __name__ == "__main__":
    text = "I am feeling very excited and joyful today!"
    emotion = detect_emotion(text)
    color = emotion_to_color(emotion)
    print(f"Text: {text}")
    print(f"Detected Emotion: {emotion}")
    print(f"Color Palette: {color}")