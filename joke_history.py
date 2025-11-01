import random

JOKES = [
    "Why did the king go to the dentist? To get his teeth crowned.",
    "Why did the history book look sad? Too many dates.",
    "Why did the archaeologist break up? Too many buried feelings.",
    "Why did the soldier bring a pencil to war? To draw his weapon.",
    "Why did the knight always carry a notebook? For sword notes.",
    "Why did the museum go to school? To get more exhibits.",
    "Why did the pyramid go to therapy? Feeling stacked.",
    "Why did the Roman Empire cut off its WiFi? Too many connections.",
    "Why did the historian get in trouble? Because he was caught rewriting history.",
    "Why did the pharaoh refuse to play cards? Too many tombs.",
    "Why did the medieval knight go to school? To improve his knight-life balance.",
    "Why did the ancient tablet blush? It got written on.",
    "Why did the historian cross the road? To get to the past side.",
    "Why did the castle go on vacation? It needed to get its walls down.",
    "Why did the timeline go to therapy? Feeling stretched out."
]

def tell_joke() -> str:
    return random.choice(JOKES)