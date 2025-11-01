def detect_emotion(text: str) -> str:
    emotions = ["happy", "sad", "angry", "confused", "excited", "neutral"]
    import random
    return random.choice(emotions)