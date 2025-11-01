TOXIC_WORDS = ["hate", "stupid", "idiot"]

def sanitize(text: str) -> str:
    for w in TOXIC_WORDS:
        text = text.replace(w, "[censored]")
    return text