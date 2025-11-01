"""
response_formatter.py
Format AI responses (markdown, emojis, etc.).
"""

def format_response(response: str, emoji: str = "🤖") -> str:
    return f"{emoji} {response}"

# Example
if __name__ == "__main__":
    print(format_response("Hello there!"))