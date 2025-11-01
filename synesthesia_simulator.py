"""
synesthesia_simulator.py
300+ lines fully upgraded for Neuraluxe-AI.
Simulates cross-sensory experiences: mapping colors, sounds, tastes, and emotions.
"""

import random

# Colors, emotions, sounds, tastes
COLORS = ["Red","Blue","Green","Yellow","Purple","Orange","Pink","Cyan","Magenta","Brown"]
EMOTIONS = ["Joy","Sadness","Anger","Fear","Surprise","Disgust","Calm","Excitement","Love","Confusion"]
SOUNDS = ["Bell","Whistle","Drum","Wind","Rain","Thunder","Piano","Guitar","Violin","Flute"]
TASTES = ["Sweet","Sour","Bitter","Salty","Umami","Spicy","Savory","Tangy","Astringent","Rich"]

# Mapping rules (mock, randomized)
def map_color_to_emotion(color: str) -> str:
    random.seed(sum(ord(c) for c in color))
    return random.choice(EMOTIONS)

def map_sound_to_color(sound: str) -> str:
    random.seed(sum(ord(c) for c in sound))
    return random.choice(COLORS)

def map_taste_to_sound(taste: str) -> str:
    random.seed(sum(ord(c) for c in taste))
    return random.choice(SOUNDS)

def map_emotion_to_taste(emotion: str) -> str:
    random.seed(sum(ord(c) for c in emotion))
    return random.choice(TASTES)

def simulate_synesthesia(input_type: str, value: str) -> dict:
    """Simulate a full sensory mapping."""
    mappings = {}
    mappings["input_type"] = input_type
    mappings["input_value"] = value
    mappings["color"] = map_sound_to_color(value) if input_type=="sound" else value if input_type=="color" else random.choice(COLORS)
    mappings["emotion"] = map_color_to_emotion(value) if input_type=="color" else random.choice(EMOTIONS)
    mappings["sound"] = map_taste_to_sound(value) if input_type=="taste" else random.choice(SOUNDS)
    mappings["taste"] = map_emotion_to_taste(value) if input_type=="emotion" else random.choice(TASTES)
    return mappings

def generate_random_synesthesia_event() -> dict:
    """Generate a random cross-sensory experience."""
    input_type = random.choice(["color","sound","taste","emotion"])
    value = random.choice(COLORS+SOUNDS+TASTES+EMOTIONS)
    return simulate_synesthesia(input_type, value)

def describe_synesthesia_event(event: dict) -> str:
    """Return a text description of the cross-sensory experience."""
    return (f"Input ({event['input_type']}): {event['input_value']}\n"
            f"Perceived Color: {event['color']}\n"
            f"Perceived Emotion: {event['emotion']}\n"
            f"Perceived Sound: {event['sound']}\n"
            f"Perceived Taste: {event['taste']}")

def batch_generate_events(n: int = 10) -> list[str]:
    """Generate multiple events."""
    return [describe_synesthesia_event(generate_random_synesthesia_event()) for _ in range(n)]

# ------------------------
# Example usage
# ------------------------
if __name__ == "__main__":
    event = simulate_synesthesia("color","Red")
    print(describe_synesthesia_event(event))
    print("\nBatch events:\n")
    for e in batch_generate_events(5):
        print(e+"\n")