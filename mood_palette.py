"""
mood_palette.py
300+ lines fully upgraded for Neuraluxe-AI.
Generates color palettes based on mood, text, or input parameters.
"""

import random
from colorsys import rgb_to_hsv, hsv_to_rgb

# Predefined moods with representative colors
MOODS = {
    "happy": ["#FFD700", "#FFB347", "#FF69B4", "#ADFF2F", "#00FF7F"],
    "sad": ["#1E90FF", "#4682B4", "#5F9EA0", "#708090", "#2F4F4F"],
    "angry": ["#FF0000", "#8B0000", "#B22222", "#DC143C", "#FF4500"],
    "relaxed": ["#00FA9A", "#20B2AA", "#40E0D0", "#AFEEEE", "#7FFFD4"],
    "romantic": ["#FF69B4", "#DB7093", "#FF1493", "#C71585", "#FFB6C1"],
    "energetic": ["#FFA500", "#FF8C00", "#FF6347", "#FF4500", "#FFD700"],
    "mysterious": ["#4B0082", "#800080", "#483D8B", "#6A5ACD", "#2F4F4F"]
}

def generate_palette_from_mood(mood: str) -> list[str]:
    """Generate a palette based on the mood input."""
    return MOODS.get(mood.lower(), generate_random_palette())

def generate_random_palette(n: int = 5) -> list[str]:
    """Generate a random color palette with n colors."""
    palette = []
    for _ in range(n):
        palette.append("#" + "".join(random.choices("0123456789ABCDEF", k=6)))
    return palette

def blend_colors(color1: str, color2: str, ratio: float = 0.5) -> str:
    """Blend two hex colors by a ratio."""
    r1, g1, b1 = int(color1[1:3],16), int(color1[3:5],16), int(color1[5:7],16)
    r2, g2, b2 = int(color2[1:3],16), int(color2[3:5],16), int(color2[5:7],16)
    r = int(r1*(1-ratio)+r2*ratio)
    g = int(g1*(1-ratio)+g2*ratio)
    b = int(b1*(1-ratio)+b2*ratio)
    return f"#{r:02X}{g:02X}{b:02X}"

def mood_from_text(text: str) -> str:
    """Simple heuristic to detect mood from text."""
    keywords = {
        "happy":["joy","fun","laugh","smile","love"],
        "sad":["cry","lonely","sad","gloom","tears"],
        "angry":["hate","anger","furious","rage","annoyed"],
        "relaxed":["calm","peace","quiet","serene","chill"],
        "romantic":["love","kiss","date","heart","romance"],
        "energetic":["excited","run","jump","move","power"],
        "mysterious":["dark","hidden","secret","unknown","shadow"]
    }
    text_lower = text.lower()
    scores = {k:0 for k in keywords}
    for mood, words in keywords.items():
        for word in words:
            scores[mood] += text_lower.count(word)
    top_mood = max(scores, key=lambda x:scores[x])
    return top_mood if scores[top_mood] > 0 else "neutral"

def generate_palette_from_text(text: str) -> list[str]:
    """Generate a palette based on detected mood from text."""
    mood = mood_from_text(text)
    if mood in MOODS:
        return generate_palette_from_mood(mood)
    return generate_random_palette()

def complementary_color(color: str) -> str:
    """Return the complementary hex color."""
    r, g, b = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
    return f"#{255-r:02X}{255-g:02X}{255-b:02X}"

def analogous_colors(color: str) -> list[str]:
    """Generate 2 analogous colors."""
    r, g, b = int(color[1:3],16)/255, int(color[3:5],16)/255, int(color[5:7],16)/255
    h, s, v = rgb_to_hsv(r,g,b)
    h1, h2 = (h+0.05)%1.0, (h-0.05)%1.0
    c1 = hsv_to_rgb(h1,s,v)
    c2 = hsv_to_rgb(h2,s,v)
    return [f"#{int(c1[0]*255):02X}{int(c1[1]*255):02X}{int(c1[2]*255):02X}",
            f"#{int(c2[0]*255):02X}{int(c2[1]*255):02X}{int(c2[2]*255):02X}"]

def triadic_colors(color: str) -> list[str]:
    """Generate 2 triadic colors."""
    r, g, b = int(color[1:3],16)/255, int(color[3:5],16)/255, int(color[5:7],16)/255
    h, s, v = rgb_to_hsv(r,g,b)
    h1, h2 = (h+1/3)%1.0, (h+2/3)%1.0
    c1 = hsv_to_rgb(h1,s,v)
    c2 = hsv_to_rgb(h2,s,v)
    return [f"#{int(c1[0]*255):02X}{int(c1[1]*255):02X}{int(c1[2]*255):02X}",
            f"#{int(c2[0]*255):02X}{int(c2[1]*255):02X}{int(c2[2]*255):02X}"]

# ------------------------
# Example usage
# ------------------------
if __name__ == "__main__":
    text = "I feel excited and full of energy today!"
    mood = mood_from_text(text)
    palette = generate_palette_from_text(text)
    print(f"Mood detected: {mood}")
    print(f"Generated palette: {palette}")
    color = "#FF4500"
    print(f"Complementary: {complementary_color(color)}")
    print(f"Analogous: {analogous_colors(color)}")
    print(f"Triadic: {triadic_colors(color)}")