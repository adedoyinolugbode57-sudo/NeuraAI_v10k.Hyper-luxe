"""
content_recommender.py
AI-driven personalized content suggestion system for Neuraluxe-AI.
"""

import random
from typing import List, Dict

# ------------------------
# Mock user preferences
# ------------------------
USER_PROFILES = {
    "user1": {"topics": ["technology", "ai", "gaming"], "language": "en"},
    "user2": {"topics": ["finance", "investing", "crypto"], "language": "en"},
    "user3": {"topics": ["fashion", "lifestyle", "art"], "language": "en"},
}

CONTENT_LIBRARY = [
    {"title": "AI in 2025", "topic": "ai", "language": "en"},
    {"title": "Crypto Trading Tips", "topic": "crypto", "language": "en"},
    {"title": "Top Gaming PCs", "topic": "gaming", "language": "en"},
    {"title": "Modern Fashion Trends", "topic": "fashion", "language": "en"},
    {"title": "Art Appreciation", "topic": "art", "language": "en"},
    {"title": "Investing in Stocks", "topic": "investing", "language": "en"},
    {"title": "Neural Networks 101", "topic": "ai", "language": "en"},
    {"title": "Lifestyle Hacks", "topic": "lifestyle", "language": "en"},
]

# ------------------------
# Recommender Engine
# ------------------------
def recommend_content(user_id: str, max_results: int = 5) -> List[Dict]:
    """Return a personalized list of content items for the user."""
    user_profile = USER_PROFILES.get(user_id, {"topics": [], "language": "en"})
    recommended = []

    for item in CONTENT_LIBRARY:
        if item["topic"] in user_profile["topics"] and item["language"] == user_profile["language"]:
            recommended.append(item)

    # Fill remaining slots randomly
    while len(recommended) < max_results:
        item = random.choice(CONTENT_LIBRARY)
        if item not in recommended:
            recommended.append(item)

    random.shuffle(recommended)
    return recommended[:max_results]

# ------------------------
# Example
# ------------------------
if __name__ == "__main__":
    user_id = "user1"
    suggestions = recommend_content(user_id)
    print(f"[Recommender] Suggested content for {user_id}:")
    for content in suggestions:
        print(f"- {content['title']} ({content['topic']})")