# bot_engine.py
# Unique Core Bot Engine for NeuraAI_v10k.Hyperluxe
# Handles AI responses, context memory, dynamic triggers, mini-games, premium features, and social feed hooks

import os
import requests
import logging
import random
from datetime import datetime
from utils import is_premium, add_premium, format_response
from ai_memory import get_memory, store_memory
from mini_games import launch_game, get_game_list
import social_feed

# --- Configuration ---
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")
DEFAULT_MODEL = "gpt-5-mini"
MAX_TOKENS = 300
TEMPERATURE = 0.7

# --- Bot Engine Class ---
class BotEngine:
    def __init__(self, user_id=None):
        self.user_id = user_id or "guest"
        self.premium = False
        self.memory = get_memory(self.user_id)

    def check_premium(self):
        self.premium = is_premium(self.user_id)
        return self.premium

    def update_memory(self, user_message, bot_response):
        store_memory(self.user_id, user_message, bot_response)
        self.memory = get_memory(self.user_id)

    def call_gpt(self, prompt):
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": DEFAULT_MODEL,
            "prompt": prompt,
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE
        }
        try:
            response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            text = data.get("choices", [{}])[0].get("text", "").strip()
            return text
        except Exception as e:
            logging.error(f"[BotEngine GPT Error] {e}")
            return "Sorry, the AI is currently unavailable."

    def generate_response(self, user_message):
        """
        Generate a smart response with:
        - memory context
        - premium flair
        - dynamic triggers for mini-games & social feed
        """
        # Update premium status
        self.check_premium()
        # Build prompt with memory
        prompt = f"{self.memory}\nUser: {user_message}\nAI:"
        # Call GPT
        response_text = self.call_gpt(prompt)
        # Update memory
        self.update_memory(user_message, response_text)
        # Add premium flair
        response_text = format_response(response_text, theme="neon", premium=self.premium)
        # Dynamic triggers
        response_text += self._handle_triggers(user_message)
        return response_text

    def _handle_triggers(self, user_message):
        """
        Handle special keywords:
        - 'play game' -> list mini-games
        - 'social feed' -> fetch recent posts
        """
        triggers = ""
        msg_lower = user_message.lower()
        if "play game" in msg_lower:
            games = get_game_list()
            triggers += f"\n🎮 Mini-games available: {', '.join(games)}"
        if "social feed" in msg_lower:
            posts = social_feed.get_feed(limit=3)
            posts_preview = "\n".join([f"- {p}" for p in posts])
            triggers += f"\n📣 Recent social feed posts:\n{posts_preview}"
        return triggers

    def start_game(self, game_name):
        """
        Launch a mini-game directly from bot engine
        """
        if game_name not in get_game_list():
            return f"Game '{game_name}' not found. Use 'play game' to see available games."
        return launch_game(game_name, self.user_id, self.premium)

    def upgrade_premium(self, days=30):
        """
        Grant premium access directly via bot engine
        """
        add_premium(self.user_id, days)
        self.premium = True
        return f"Premium granted for {days} days."

# --- Example Usage ---
if __name__ == "__main__":
    bot = BotEngine(user_id="test_user")
    print(bot.generate_response("Hello, can you play game with me?"))
    print(bot.start_game("trivia"))
    print(bot.upgrade_premium(60))