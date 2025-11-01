"""
astro_forecaster.py
Premium AI-based astrology module for Neuraluxe-AI.
Includes daily, weekly, monthly horoscopes, compatibility, personality traits,
numerology, and cosmic tips.
"""

import random
from datetime import datetime, timedelta

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

ELEMENTS = {
    "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
    "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
    "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
    "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water"
}

PERSONALITY_TRAITS = {
    "Aries": ["Courageous", "Determined", "Confident", "Enthusiastic"],
    "Taurus": ["Reliable", "Patient", "Practical", "Devoted"],
    "Gemini": ["Gentle", "Curious", "Adaptable", "Outgoing"],
    "Cancer": ["Tenacious", "Highly imaginative", "Loyal", "Emotional"],
    "Leo": ["Creative", "Passionate", "Generous", "Warm-hearted"],
    "Virgo": ["Loyal", "Analytical", "Kind", "Hardworking"],
    "Libra": ["Cooperative", "Diplomatic", "Graceful", "Fair-minded"],
    "Scorpio": ["Resourceful", "Brave", "Passionate", "Stubborn"],
    "Sagittarius": ["Generous", "Idealistic", "Great sense of humor"],
    "Capricorn": ["Responsible", "Disciplined", "Self-control", "Good managers"],
    "Aquarius": ["Progressive", "Original", "Independent", "Humanitarian"],
    "Pisces": ["Compassionate", "Artistic", "Intuitive", "Gentle"]
}

DAILY_PREDICTIONS = [
    "Today is perfect for new beginnings.",
    "Expect surprises in your social circle today.",
    "Financial opportunities are around the corner.",
    "Take care of your health today.",
    "Romantic vibes are strong today."
]

WEEKLY_PREDICTIONS = [
    "A challenging week ahead, focus on priorities.",
    "Creative energy peaks this week; harness it.",
    "Family matters need attention this week.",
    "Expect professional growth opportunities.",
    "Spend time on learning and personal development."
]

MONTHLY_PREDICTIONS = [
    "This month is ideal for self-reflection.",
    "Travel and adventure opportunities abound.",
    "Romantic relationships will face exciting changes.",
    "Financial decisions must be well-considered.",
    "Personal growth takes center stage this month."
]

COMPATIBILITY_FACTORS = ["Love", "Trust", "Communication", "Ambition", "Friendship"]

COSMIC_TIPS = [
    "Align your activities with the moon phase for best results.",
    "Morning meditation enhances clarity for your sign.",
    "Wear your element color to boost energy.",
    "Carry a small crystal to attract positive vibes.",
    "Plan major decisions on a day ruled by your sign's planet."
]

NUMEROLOGY_BASE = {
    "Aries": 1, "Taurus": 2, "Gemini": 3, "Cancer": 4, "Leo": 5, "Virgo": 6,
    "Libra": 7, "Scorpio": 8, "Sagittarius": 9, "Capricorn": 10, "Aquarius": 11, "Pisces": 12
}

def get_daily_horoscope(sign: str) -> str:
    if sign not in ZODIAC_SIGNS:
        return "Unknown zodiac sign."
    return random.choice(DAILY_PREDICTIONS)

def get_weekly_horoscope(sign: str) -> str:
    if sign not in ZODIAC_SIGNS:
        return "Unknown zodiac sign."
    return random.choice(WEEKLY_PREDICTIONS)

def get_monthly_horoscope(sign: str) -> str:
    if sign not in ZODIAC_SIGNS:
        return "Unknown zodiac sign."
    return random.choice(MONTHLY_PREDICTIONS)

def compatibility_analysis(sign1: str, sign2: str) -> dict:
    if sign1 not in ZODIAC_SIGNS or sign2 not in ZODIAC_SIGNS:
        return {"error": "Invalid zodiac signs."}
    return {factor: f"{random.randint(50,100)}%" for factor in COMPATIBILITY_FACTORS}

def personality_traits(sign: str) -> list:
    return PERSONALITY_TRAITS.get(sign, ["Unknown traits."])

def element(sign: str) -> str:
    return ELEMENTS.get(sign, "Unknown")

def numerology(sign: str) -> int:
    return NUMEROLOGY_BASE.get(sign, 0)

def cosmic_tip() -> str:
    return random.choice(COSMIC_TIPS)

def advanced_horoscope(sign: str) -> dict:
    return {
        "daily": get_daily_horoscope(sign),
        "weekly": get_weekly_horoscope(sign),
        "monthly": get_monthly_horoscope(sign),
        "traits": personality_traits(sign),
        "element": element(sign),
        "numerology": numerology(sign),
        "tip": cosmic_tip()
    }

# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    my_sign = "Leo"
    partner_sign = "Sagittarius"
    
    print("=== DAILY HOROSCOPE ===")
    print(get_daily_horoscope(my_sign))
    
    print("\n=== WEEKLY HOROSCOPE ===")
    print(get_weekly_horoscope(my_sign))
    
    print("\n=== MONTHLY HOROSCOPE ===")
    print(get_monthly_horoscope(my_sign))
    
    print("\n=== COMPATIBILITY ===")
    print(compatibility_analysis(my_sign, partner_sign))
    
    print("\n=== ADVANCED HOROSCOPE ===")
    advanced = advanced_horoscope(my_sign)
    for key, val in advanced.items():
        print(f"{key.capitalize()}: {val}")
    
    print("\n=== COSMIC TIP ===")
    print(cosmic_tip())