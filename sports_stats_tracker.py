"""
sports_stats_tracker.py
Track sports stats, rankings, highlights, and AI predictions.
"""

import random
from datetime import datetime, timedelta
from collections import defaultdict

SPORTS = ["Soccer", "Basketball", "Tennis", "eSports"]
TEAMS = {
    "Soccer": ["FC Barcelona", "Real Madrid", "Manchester City", "Liverpool"],
    "Basketball": ["Lakers", "Warriors", "Bulls", "Celtics"],
    "Tennis": ["Nadal", "Federer", "Djokovic", "Swiatek"],
    "eSports": ["Team Liquid", "Fnatic", "TSM", "G2"]
}

USER_PREFERENCES = defaultdict(lambda: {"sports": ["Soccer"], "favorites": []})
STATS_CACHE = defaultdict(dict)

class SportsStatsTracker:
    def __init__(self, api_available=False):
        self.api_available = api_available
        self.cache = defaultdict(list)

    def fetch_team_stats(self, sport: str, team: str):
        if self.api_available:
            # Placeholder for live API
            stats = {
                "wins": random.randint(0, 50),
                "losses": random.randint(0, 50),
                "draws": random.randint(0, 50),
                "ranking": random.randint(1, 100),
                "points": random.randint(0, 200)
            }
        else:
            stats = {
                "wins": random.randint(5, 25),
                "losses": random.randint(0, 20),
                "draws": random.randint(0, 10),
                "ranking": random.randint(1, 20),
                "points": random.randint(10, 80)
            }
        self.cache[team] = stats
        return stats

    def trending_matches(self, sport: str, top_n=3):
        teams = TEAMS.get(sport, [])
        random.shuffle(teams)
        matches = [(teams[i], teams[i+1]) for i in range(0, len(teams)-1, 2)]
        return matches[:top_n]

    def ai_prediction(self, sport: str, team1: str, team2: str) -> str:
        score1 = random.randint(0, 5)
        score2 = random.randint(0, 5)
        winner = team1 if score1 > score2 else team2 if score2 > score1 else "Draw"
        confidence = random.randint(50, 99)
        return f"{team1} vs {team2}: Predicted Winner: {winner} | Confidence: {confidence}%"

    def generate_leaderboard(self, sport: str):
        teams = TEAMS.get(sport, [])
        leaderboard = {team: self.fetch_team_stats(sport, team)["points"] for team in teams}
        return dict(sorted(leaderboard.items(), key=lambda x: x[1], reverse=True))

# Example usage
if __name__ == "__main__":
    tracker = SportsStatsTracker()
    sport = "Soccer"
    print(tracker.fetch_team_stats(sport, "FC Barcelona"))
    print(tracker.trending_matches(sport))
    print(tracker.ai_prediction(sport, "FC Barcelona", "Real Madrid"))
    print(tracker.generate_leaderboard(sport))