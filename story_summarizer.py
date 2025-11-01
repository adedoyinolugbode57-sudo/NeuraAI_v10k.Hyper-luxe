def summarize_text(text: str) -> str:
    return text[:75] + "..." if len(text) > 75 else text