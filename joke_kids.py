import random

JOKES = [
    "Why did the teddy bear say no to dessert? He was stuffed.",
    "Why did the kid bring a ladder to school? To go to high school.",
    "Why did the cookie go to the doctor? It felt crummy.",
    "Why did the kid put his money in the blender? He wanted to make liquid assets.",
    "Why did the balloon go near the ceiling? It wanted to rise to the occasion.",
    "Why did the banana go to the doctor? It wasn’t peeling well.",
    "Why did the cupcake go to the party? It felt sweet.",
    "Why did the pencil go to the principal’s office? It was drawing attention.",
    "Why did the jellybean go to school? To get a little smarter.",
    "Why did the crayons break up? They couldn’t color together.",
    "Why did the milk go to school? To get cultured.",
    "Why did the gum cross the road? It wanted to stick around.",
    "Why did the apple stop in traffic? It ran out of juice.",
    "Why did the kid bring a ladder? To reach new heights.",
    "Why did the robot go to school? To improve its byte size."
]

def tell_joke() -> str:
    return random.choice(JOKES)