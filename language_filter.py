"""
language_filter.py
Filters offensive or unwanted language.
"""
def filter_text(text: str) -> str:
    blocked = ["badword", "curse"]
    for word in blocked:
        text = text.replace(word, "*"*len(word))
    return text