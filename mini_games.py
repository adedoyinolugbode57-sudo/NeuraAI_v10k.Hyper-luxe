"""
mini_games.py – Hyperluxe 10k Edition
Author: ChatGPT + Joshua Dav
Supports 1,000+ dynamic games with AI-generated challenges.
Integrated with NeuraAI core and user rewards.
"""

import random
import json
import time
from typing import Dict, Any, List

GAMES_FILE = "game_data.json"
REWARDS_FILE = "rewards_store.json"

def _load_json(path: str) -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def _save_json(path: str, data: Dict[str, Any]):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_games() -> List[Dict[str, Any]]:
    data = _load_json(GAMES_FILE)
    if not data:
        _save_json(GAMES_FILE, {"games": []})
        return []
    return data.get("games", [])

def add_game(title: str, category: str, difficulty: str, prompt: str, answer: str):
    data = _load_json(GAMES_FILE)
    game_id = f"game_{int(time.time()*1000)}"
    game = {
        "id": game_id,
        "title": title,
        "category": category,
        "difficulty": difficulty,
        "prompt": prompt,
        "answer": answer,
        "timestamp": time.time(),
    }
    data.setdefault("games", []).append(game)
    _save_json(GAMES_FILE, data)
    return game

def generate_ai_game(ai_engine, category="general"):
    """Ask AI to create a fresh question and answer dynamically."""
    prompt = f"Generate a fun interactive {category} quiz with a clear correct answer."
    try:
        result = ai_engine.generate(prompt)
        return {"category": category, "question": result["question"], "answer": result["answer"]}
    except Exception as e:
        return {"error": str(e)}

def play_game(game: Dict[str, Any]):
    print(f"\n🎮 {game['title']} ({game['category']} – {game['difficulty']})")
    print("Question:", game["prompt"])
    ans = input("Your answer: ").strip().lower()
    correct = ans == game["answer"].lower()
    print("✅ Correct!" if correct else f"❌ Wrong! Correct answer: {game['answer']}")
    reward_user("player", 10 if correct else 2)
    return correct

def reward_user(user: str, points: int):
    data = _load_json(REWARDS_FILE)
    data[user] = data.get(user, 0) + points
    _save_json(REWARDS_FILE, data)

def get_user_score(user: str):
    data = _load_json(REWARDS_FILE)
    return data.get(user, 0)

def bootstrap_games():
    """Preload hundreds of games in various categories"""
    categories = ["math", "science", "anime", "geography", "coding", "history", "logic"]
    for i in range(1, 1001):
        add_game(
            title=f"Hyper Challenge {i}",
            category=random.choice(categories),
            difficulty=random.choice(["easy", "medium", "hard"]),
            prompt=f"What is {i} + {random.randint(1,100)}?",
            answer=str(i + random.randint(1,100)),
        )
    print("✅ 1,000 games preloaded successfully!")

if __name__ == "__main__":
    print("🕹️ Welcome to NeuraAI Hyperluxe Games")
    games = load_games()
    if not games:
        bootstrap_games()
    game = random.choice(games)
    play_game(game)