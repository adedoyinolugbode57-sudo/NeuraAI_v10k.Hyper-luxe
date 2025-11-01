import random

JOKES = [
    "Why did the employee get fired from the calendar factory? He took a day off.",
    "Why don’t scientists trust atoms? They make up everything.",
    "Why did the manager go to school? To improve his leadership skills.",
    "Why did the stapler break up with the paper? It felt stuck.",
    "Why did the computer keep sneezing? It had a virus.",
    "Why did the office worker go to the doctor? Too many sick days.",
    "Why did the printer go to therapy? It had paper jams.",
    "Why did the coffee file a police report? It got mugged.",
    "Why did the boss bring a ladder to work? To reach new heights.",
    "Why did the copier go on strike? It felt overworked.",
    "Why did the accountant cross the road? To balance the books.",
    "Why did the email go to therapy? It felt spammed.",
    "Why did the office worker go to the beach? To surf the web.",
    "Why did the calendar go to therapy? Its days were numbered.",
    "Why did the desk bring a blanket? It wanted to cover its work."
]

def tell_joke() -> str:
    return random.choice(JOKES)