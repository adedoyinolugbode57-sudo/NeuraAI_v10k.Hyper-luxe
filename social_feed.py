# social_feed.py
"""
NeuraAI_v10k.HyperLuxe - Social Feed Engine v2.5
Real-time AI-curated news feed + user community posts.
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path
from functools import lru_cache
import random

NEWS_FILE = Path(__file__).parent / "data" / "feed_cache.json"
POSTS_FILE = Path(__file__).parent / "data" / "user_posts.json"
for p in (NEWS_FILE, POSTS_FILE):
    p.parent.mkdir(parents=True, exist_ok=True)
if not POSTS_FILE.exists():
    POSTS_FILE.write_text(json.dumps({"posts": []}, indent=2), encoding="utf-8")

CATEGORIES = ["AI", "Tech", "Crypto", "Education", "Books", "Lifestyle"]
NEWSAPI_KEY = "replace_with_your_key"
CACHE_TIME = 600  # 10 min

def _load_cache():
    if not NEWS_FILE.exists():
        return None
    cache = json.loads(NEWS_FILE.read_text(encoding="utf-8"))
    if time.time() - cache["time"] > CACHE_TIME:
        return None
    return cache["data"]

def _save_cache(data):
    NEWS_FILE.write_text(json.dumps({"time": time.time(), "data": data}, indent=2), encoding="utf-8")

def _fetch_news(category="AI", limit=5):
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {"apiKey": NEWSAPI_KEY, "q": category, "language": "en", "pageSize": limit}
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        articles = res.json().get("articles", [])
        return [{
            "title": a["title"],
            "source": a["source"]["name"],
            "url": a["url"],
            "summary": (a.get("description") or a["title"])[:180] + "...",
            "category": category,
            "time": datetime.utcnow().isoformat()
        } for a in articles]
    except Exception as e:
        print("[Feed Error]", e)
        return []

@lru_cache(maxsize=20)
def get_feed(category="AI"):
    cache = _load_cache()
    if cache:
        return cache.get(category, [])
    data = {}
    for cat in CATEGORIES:
        data[cat] = _fetch_news(cat)
    _save_cache(data)
    return data.get(category, [])

def trending_tags(feed):
    all_words = []
    for item in feed:
        all_words += item["title"].split()
    common = {}
    for w in all_words:
        w = w.strip("#,.!?").lower()
        if len(w) < 4: continue
        common[w] = common.get(w, 0) + 1
    return sorted(common.items(), key=lambda x: x[1], reverse=True)[:5]

# ------------------- USER POSTS ---------------------

def _read_posts():
    return json.loads(POSTS_FILE.read_text(encoding="utf-8"))

def _write_posts(data):
    POSTS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

def add_post(user, content, category="General"):
    posts = _read_posts()
    post = {
        "id": len(posts["posts"]) + 1,
        "user": user,
        "content": content.strip(),
        "category": category,
        "likes": 0,
        "comments": [],
        "created_at": datetime.utcnow().isoformat(),
    }
    posts["posts"].append(post)
    _write_posts(posts)
    return post

def like_post(post_id):
    posts = _read_posts()
    for post in posts["posts"]:
        if post["id"] == post_id:
            post["likes"] += 1
            _write_posts(posts)
            return post
    return None

def comment_post(post_id, user, text):
    posts = _read_posts()
    for post in posts["posts"]:
        if post["id"] == post_id:
            post["comments"].append({"user": user, "text": text, "time": datetime.utcnow().isoformat()})
            _write_posts(posts)
            return post
    return None

def get_trending_posts(limit=5):
    posts = _read_posts()["posts"]
    sorted_posts = sorted(posts, key=lambda x: x["likes"], reverse=True)
    return sorted_posts[:limit]

def generate_daily_digest():
    """Combine top AI/Tech headlines + most liked posts."""
    ai_news = get_feed("AI")[:3]
    tech_news = get_feed("Tech")[:3]
    top_posts = get_trending_posts()
    digest = {
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "headlines": ai_news + tech_news,
        "community_highlights": top_posts
    }
    path = Path(__file__).parent / "reports" / f"digest_{int(time.time())}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(digest, indent=2), encoding="utf-8")
    return str(path)

# Demo
if __name__ == "__main__":
    print("=== Trending AI Feed ===")
    feed = get_feed("AI")
    for item in feed[:3]:
        print("-", item["title"])
    print("\nTrending Tags:", trending_tags(feed))
    print("\nAdding Sample Post...")
    p = add_post("Joshua Dav", "HyperLuxe AI feed is amazing!", "AI")
    like_post(p["id"])
    comment_post(p["id"], "NeuraBot", "🔥 Absolutely agree!")
    print("Daily digest created:", generate_daily_digest())