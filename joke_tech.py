import random

JOKES = [
    "Why did the computer go to the doctor? It caught a virus.",
    "Why did the developer go broke? Because he used up all his cache.",
    "Why did the smartphone go to school? It wanted to improve its apps.",
    "Why did the robot go on a diet? Too many bytes.",
    "Why was the computer cold? It left its Windows open.",
    "Why did the programmer quit his job? He didn’t get arrays.",
    "Why did the keyboard break up with the monitor? Too many arguments.",
    "Why was the computer tired? It had too many tabs open.",
    "Why did the server go to therapy? Too many requests.",
    "Why did the AI go to art class? To learn how to draw conclusions.",
    "Why did the router break up? Lost connection.",
    "Why was the computer sticky? It had too many cookies.",
    "Why did the hacker break up with the code? Too many bugs.",
    "Why did the printer go to school? To improve its type-setting.",
    "Why did the laptop get glasses? To improve its web sight."
]

def tell_joke() -> str:
    return random.choice(JOKES)