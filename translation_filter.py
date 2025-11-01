"""
translation_filter.py
Detects and filters inappropriate translations.
"""
def translate_safe(text: str, target_lang: str) -> str:
    filtered = text.replace("forbidden", "***")
    return f"Translated to {target_lang}: {filtered}"