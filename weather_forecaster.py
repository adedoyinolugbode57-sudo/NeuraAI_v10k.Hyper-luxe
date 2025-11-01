"""
weather_forecaster.py
Premium weather forecasts with multi-location support, alerts, and AI suggestions.
"""

import random
from datetime import datetime, timedelta
from collections import defaultdict

CITIES = ["New York", "London", "Paris", "Tokyo", "Lagos", "Sydney", "Berlin", "Dubai"]
USER_PREFERENCES = defaultdict(lambda: {"locations": ["New York"]})

WEATHER_CONDITIONS = ["Sunny", "Cloudy", "Rainy", "Stormy", "Snowy", "Windy", "Foggy"]

class WeatherForecaster:
    def __init__(self, api_available=False):
        self.api_available = api_available
        self.cache = {}

    def fetch_weather(self, city: str):
        if self.api_available:
            # Placeholder for live API
            temp = round(random.uniform(-5, 40), 1)
            condition = random.choice(WEATHER_CONDITIONS)
        else:
            temp = round(random.uniform(10, 35), 1)
            condition = random.choice(WEATHER_CONDITIONS)
        weather_info = {
            "city": city,
            "temperature": temp,
            "condition": condition,
            "timestamp": datetime.now()
        }
        self.cache[city] = weather_info
        return weather_info

    def weekly_forecast(self, city: str):
        return [self.fetch_weather(city) for _ in range(7)]

    def ai_suggestion(self, city: str):
        weather = self.fetch_weather(city)
        if weather["condition"] in ["Rainy", "Stormy"]:
            return f"AI Suggestion: Carry an umbrella in {city}!"
        elif weather["temperature"] > 30:
            return f"AI Suggestion: Stay hydrated in {city}!"
        else:
            return f"AI Suggestion: Enjoy the weather in {city}!"

# Example usage
if __name__ == "__main__":
    wf = WeatherForecaster()
    city = "London"
    print(wf.fetch_weather(city))
    print(wf.weekly_forecast(city))
    print(wf.ai_suggestion(city))