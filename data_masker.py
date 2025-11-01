def mask_data(text: str) -> str:
    import re
    text = re.sub(r"\b\d{12,16}\b", "****MASKED****", text)  # fake card numbers
    text = re.sub(r"\b\d{10}\b", "****MASKED****", text)  # phone numbers
    return text