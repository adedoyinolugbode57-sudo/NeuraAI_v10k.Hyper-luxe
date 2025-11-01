"""
historical_reenactor.py
Generate mock historical scene descriptions.
"""

import random

ERAS = ["Ancient Egypt", "Medieval Europe", "Renaissance Italy", "Industrial Revolution", "Future Tech Era"]
EVENTS = ["battle", "celebration", "invention", "discovery", "council meeting"]

def generate_scene(era: str = None) -> str:
    """Return a mock historical scene."""
    era = era or random.choice(ERAS)
    event = random.choice(EVENTS)
    characters = ["king", "scientist", "soldier", "artist", "merchant"]
    char = random.choice(characters)
    location = f"{era} city" if "Future" not in era else "futuristic lab"
    return f"In {location}, a {char} witnesses a {event}."

def batch_scenes(n: int = 5) -> list:
    return [generate_scene() for _ in range(n)]

# Example usage
if __name__ == "__main__":
    for scene in batch_scenes(10):
        print(scene)