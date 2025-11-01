import random

JOKES = [
    "Why can't you trust an atom? Because they make up everything!",
    "Why did the biologist break up with the physicist? No chemistry.",
    "Why did the germ go to school? To become a little cultured.",
    "Why did the physics book look sad? Too many problems.",
    "Why did the chemist keep his Nobel Prize medal in the freezer? To stay cool under pressure.",
    "Why did the neuron stay in bed? It needed to recharge its potential.",
    "Why did the astronaut break up with his girlfriend? He needed space.",
    "Why did the scientist bring a ladder to the lab? To reach higher potentials.",
    "Why did the electron go to therapy? It had too many negative thoughts.",
    "Why did the math book look unhappy? Too many problems.",
    "Why did the geologist go on a date? To find a gem.",
    "Why did the physicist cross the road? To get to the same side.",
    "Why did the chemist get arrested? He was caught in a reaction.",
    "Why did the biology teacher go to the beach? To study current events.",
    "Why did the microscope break up with the sample? It felt magnified."
]

def tell_joke() -> str:
    return random.choice(JOKES)