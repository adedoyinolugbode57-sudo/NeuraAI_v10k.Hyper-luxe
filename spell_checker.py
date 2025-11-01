"""
spell_checker.py
Basic spell checker (mock).
"""

COMMON_MISTAKES = {"teh": "the", "recieve": "receive", "adress": "address"}

def correct_spelling(text: str) -> str:
    for wrong, right in COMMON_MISTAKES.items():
        text = text.replace(wrong, right)
    return text