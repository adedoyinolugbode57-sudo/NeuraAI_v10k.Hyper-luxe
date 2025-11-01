"""
news_fetcher.py
Premium news fetcher for Neuraluxe-AI
Supports multiple categories, languages, sentiment analysis,
summaries, trending topics, caching, and user preferences.
"""

import random
from datetime import datetime, timedelta
from collections import defaultdict

# -----------------------
# Categories & Languages
# -----------------------
CATEGORIES = ["Technology", "Finance", "Entertainment", "Science", "AI", "Health", "Sports", "Politics"]
LANGUAGES = ["en", "es", "fr", "de", "zh", "jp"]

# -----------------------
# Mock Headlines (expanded)
# -----------------------
MOCK_HEADLINES = {
    "Technology": [
        "AI assistant now handles millions of queries per day!",
        "Quantum computing breakthroughs in 2025.",
        "New smartphone launches with foldable display.",
        "VR headset sales skyrocket in global market.",
        "Cloud computing adoption hits record levels."
    ],
    "Finance": [
        "Stock market sees major rally in tech sector.",
        "Cryptocurrency regulations updated in Europe.",
        "Central banks signal interest rate changes.",
        "Fintech startups gain $2B in funding.",
        "Global inflation trends shift investor strategy."
    ],
    "Entertainment": [
        "Blockbuster movie shatters box office records.",
        "Celebrity launches eco-friendly fashion line.",
        "Music streaming hits record subscriptions.",
        "Virtual concerts gain massive popularity.",
        "Award shows celebrate emerging artists."
    ],
    "Science": [
        "Mars rover discovers new signs of water.",
        "Breakthrough in fusion energy announced.",
        "Scientists decode rare animal genomes.",
        "New exoplanet discoveries excite astronomers.",
        "Climate change research highlights urgent action."
    ],
    "AI": [
        "Neuraluxe-AI expands to 300+ AI models.",
        "AI art generator wins international contest.",
        "OpenAI releases latest LLM version.",
        "AI-powered assistants outperform humans in testing.",
        "Machine learning models optimize logistics worldwide."
    ]
}

# -----------------------
# User Preferences Storage
# -----------------------
USER_PREFERENCES = defaultdict(lambda: {"categories": ["Technology"], "language": "en"})

# -----------------------
# Trending Topics
# -----------------------
TRENDING_TOPICS = defaultdict(list)  # category: list of trending keywords

# -----------------------
# NewsFetcher Class
# -----------------------
class NewsFetcher:
    def __init__(self, api_available: bool = False):
        self.api_available = api_available
        self.cache = defaultdict(list)
        self.archive = defaultdict(list)

    # -----------------------
    # Fetch Headlines
    # -----------------------
    def fetch_headlines(self, category: str = "Technology", top_n: int = 5, user_id: str = None, language: str = "en"):
        category = category.capitalize()
        if category not in CATEGORIES:
            return [f"No headlines available for category: {category}"]

        if user_id:
            user_pref = USER_PREFERENCES[user_id]
            if category not in user_pref["categories"]:
                user_pref["categories"].append(category)
            language = user_pref.get("language", language)

        if self.api_available:
            # Placeholder for real API integration
            headlines = [f"Live headline {i+1} in {category}" for i in range(top_n)]
        else:
            headlines = MOCK_HEADLINES.get(category, [])
            random.shuffle(headlines)
            headlines = headlines[:top_n]

        # Cache headlines
        self.cache[category] = headlines
        self.archive[category].append({"date": datetime.now(), "headlines": headlines})

        return headlines

    # -----------------------
    # Summarize Headlines
    # -----------------------
    def summarize_headlines(self, headlines: list) -> str:
        if not headlines:
            return "No news to summarize."
        summary = " | ".join(headlines)
        if len(summary) > 500:
            summary = summary[:500] + "..."
        return summary

    # -----------------------
    # Sentiment Analysis (mock)
    # -----------------------
    def analyze_sentiment(self, headline: str) -> str:
        sentiment = random.choice(["Positive", "Neutral", "Negative"])
        score = round(random.uniform(0.0, 1.0), 2)
        return f"{headline} | Sentiment: {sentiment} ({score})"

    # -----------------------
    # Trending Topics
    # -----------------------
    def update_trending_topics(self, category: str):
        keywords = ["AI", "blockchain", "quantum", "startup", "innovation", "research", "investment", "healthcare"]
        random.shuffle(keywords)
        TRENDING_TOPICS[category] = keywords[:5]
        return TRENDING_TOPICS[category]

    # -----------------------
    # Generate Daily Digest
    # -----------------------
    def daily_digest(self, user_id: str = None) -> dict:
        digest = {}
        categories = USER_PREFERENCES[user_id]["categories"] if user_id else CATEGORIES
        for cat in categories:
            headlines = self.fetch_headlines(cat, top_n=5, user_id=user_id)
            digest[cat] = {
                "headlines": headlines,
                "summary": self.summarize_headlines(headlines),
                "trending": self.update_trending_topics(cat)
            }
        return digest

# -----------------------
# Example Usage
# -----------------------
if __name__ == "__main__":
    fetcher = NewsFetcher()
    user_id = "user123"
    digest = fetcher.daily_digest(user_id)
    for cat, info in digest.items():
        print(f"Category: {cat}")
        print("Headlines:", info["headlines"])
        print("Summary:", info["summary"])
        print("Trending:", info["trending"])
        print("---")