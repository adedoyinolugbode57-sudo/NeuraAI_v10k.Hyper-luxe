import random

JOKES = [
    "Why did the chicken cross the playground? To get to the other slide.",
    "Why don’t cats play poker in the jungle? Too many cheetahs.",
    "Why did the dog sit in the shade? He didn’t want to be a hot dog.",
    "Why did the elephant bring a suitcase? He was packing his trunk.",
    "Why did the cow go to space? To see the moooon.",
    "Why did the bird go to jail? He was caught tweeting.",
    "Why did the fish blush? It saw the ocean’s bottom.",
    "Why did the goat get promoted? He was outstanding in his field.",
    "Why did the pig become an actor? He was really good at hamming it up.",
    "Why did the horse go behind the tree? To change his jockeys.",
    "Why did the owl get a promotion? It was a wise decision.",
    "Why did the rabbit refuse dessert? He was already stuffed.",
    "Why did the frog take the bus? His car got toad away.",
    "Why did the dog sit on the clock? He wanted to be on time.",
    "Why did the cat bring a ladder? To reach new heights."
]

def tell_joke() -> str:
    return random.choice(JOKES)