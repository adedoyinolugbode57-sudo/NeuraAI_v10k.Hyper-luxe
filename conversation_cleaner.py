"""
conversation_cleaner.py
Trim old messages or sanitize chat history.
"""

def clean_history(messages: list, max_length: int = 50) -> list:
    return messages[-max_length:]