"""
reaction_engine.py
Generate reactions based on sentiment.
"""

def react_to_sentiment(sentiment: str) -> str:
    mapping = {
        "positive": "😄",
        "negative": "😢",
        "neutral": "😐"
    }
    return mapping.get(sentiment, "🙂")