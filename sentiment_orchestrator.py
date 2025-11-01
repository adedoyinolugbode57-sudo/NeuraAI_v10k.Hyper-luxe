"""
sentiment_orchestrator.py
Analyze multiple text inputs and produce an overall sentiment (mock).
"""

import random

SENTIMENTS = ["positive", "negative", "neutral", "mixed"]

def analyze_sentiment(texts: list) -> dict:
    """Return sentiment score for each text and overall summary."""
    result = {}
    scores = {"positive": 0, "negative": 0, "neutral": 0, "mixed": 0}
    for t in texts:
        sentiment = random.choice(SENTIMENTS)
        result[t[:50]] = sentiment
        scores[sentiment] += 1
    overall = max(scores, key=scores.get)
    return {"individual": result, "overall": overall}

# Example usage
if __name__ == "__main__":
    texts = [
        "I love this AI project!",
        "This is frustrating and slow.",
        "Not sure about the outcome.",
        "Could be better, could be worse."
    ]
    print(analyze_sentiment(texts))