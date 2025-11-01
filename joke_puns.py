import random

JOKES = [
    "I used to be a banker but I lost interest.",
    "I’m reading a book about anti-gravity. It’s impossible to put down.",
    "I would tell you a construction joke, but I’m still working on it.",
    "I’m on a seafood diet. I see food and I eat it.",
    "I know a lot of jokes about retired people… but none of them work.",
    "I told my computer I needed a break, and it said 'No problem, I’ll go to sleep.'",
    "I used to play piano by ear, but now I use my hands.",
    "I’m friends with all electricians. We have good current connections.",
    "I used to be a baker, but I couldn’t make enough dough.",
    "I once tried to catch fog, but I mist.",
    "I stayed up all night to see where the sun went… and then it dawned on me.",
    "I got a job at a bakery because I kneaded dough.",
    "I’m reading a book on anti-gravity. It’s impossible to put down.",
    "I wondered why the baseball was getting bigger… then it hit me.",
    "I used to hate facial hair… but then it grew on me."
]

def tell_joke() -> str:
    return random.choice(JOKES)