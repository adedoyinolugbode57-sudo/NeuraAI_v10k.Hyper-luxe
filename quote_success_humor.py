"""
quote_success_humor.py
Return humorous or witty quotes about life, success, and ambition.
"""

import random

QUOTES = [
    "Behind every great man is a woman rolling her eyes.",
    "I find television very educating. Every time somebody turns on the set, I go into the other room and read a book.",
    "I am so clever that sometimes I don't understand a single word of what I am saying.",
    "If you think you are too small to be effective, you have never been in the dark with a mosquito.",
    "Age is of no importance unless you’re a cheese.",
    "I didn't fail the test. I just found 100 ways to do it wrong.",
    "The road to success is dotted with many tempting parking spaces.",
    "Opportunity is missed by most people because it is dressed in overalls and looks like work.",
    "I intend to live forever. So far, so good.",
    "Behind every successful man is a surprised woman.",
    "The elevator to success is out of order. You’ll have to use the stairs… one step at a time.",
    "Success is relative. The more the people you impress, the more the people hate you.",
    "I have a lot of growing up to do. I realized that the other day inside my fort.",
    "Even if you are on the right track, you’ll get run over if you just sit there.",
    "Life is short. Smile while you still have teeth."
]

def get_quote() -> str:
    return random.choice(QUOTES)