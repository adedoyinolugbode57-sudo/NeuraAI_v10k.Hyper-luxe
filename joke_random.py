import random

JOKES = [
    "Why don’t skeletons fight each other? They don’t have the guts.",
    "Why did the scarecrow win an award? He was outstanding in his field.",
    "Why did the frog take the bus? His car got toad away.",
    "Why did the moon break up with the sun? Too many eclipses.",
    "Why did the music teacher go to jail? Because she got caught with the notes.",
    "Why did the ghost go to therapy? Feeling haunted.",
    "Why did the tree go to school? To branch out.",
    "Why did the painter go to jail? He had a brush with the law.",
    "Why did the snowman get upset? He heard the weather forecast.",
    "Why did the laptop go to school? To improve its web browsing.",
    "Why did the candy go to school? To get a little smarter.",
    "Why did the magician get locked out? He lost his keys.",
    "Why did the penguin cross the ice? To get to the other slide.",
    "Why did the robot go to therapy? Too many mixed signals.",
    "Why did the calendar go on a diet? Its days were numbered."
]

def tell_joke() -> str:
    return random.choice(JOKES)