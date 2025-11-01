def tag_voice(text: str) -> str:
    tones = ["cheerful", "polite", "serious", "sarcastic", "neutral"]
    import random
    return f"[{random.choice(tones)}] {text}"