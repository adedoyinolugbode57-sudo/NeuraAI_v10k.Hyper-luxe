import random

JOKES = [
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "Why did the cookie go to the doctor? It was feeling crummy.",
    "Why did the grape stop in the middle of the road? It ran out of juice.",
    "Why did the bread break up? It kneaded space.",
    "Why did the banana go to the party? Because it was a-peeling.",
    "Why did the coffee file a police report? It got mugged.",
    "Why did the lettuce blush? It saw the salad dressing.",
    "Why did the potato cross the road? To get mashed.",
    "Why did the pie go to school? It wanted a piece of knowledge.",
    "Why did the chef break up? Too many whisk-takes.",
    "Why did the milk go to school? To get cultured.",
    "Why did the donut go to therapy? Feeling empty inside.",
    "Why did the cheese refuse to fight? It didn’t want to get grated.",
    "Why did the pasta get promoted? It was al dente.",
    "Why did the apple go to therapy? It felt rotten inside."
]

def tell_joke() -> str:
    return random.choice(JOKES)