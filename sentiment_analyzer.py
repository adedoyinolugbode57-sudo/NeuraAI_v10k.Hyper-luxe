"""
sentiment_analyzer.py
Analyze sentiment of messages.
"""

def analyze_sentiment(text: str) -> str:
    if any(word in text.lower() for word in ["happy", "great", "love"]):
        return "positive"
    elif any(word in text.lower() for word in ["sad", "bad", "hate"]):
        return "negative"
    return "neutral"