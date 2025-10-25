"""
healthcare.py — NeuraAI_v10k.Hyperluxe
AI-powered Healthcare Assistant
Created by ChatGPT + Joshua Dav
"""

import json, time, random

SYMPTOM_DB = {
    "fever": ["Common cold", "Flu", "Malaria", "COVID-19"],
    "headache": ["Tension", "Migraine", "Dehydration", "Stress"],
    "cough": ["Allergy", "Cold", "Bronchitis", "COVID-19"],
    "fatigue": ["Anemia", "Poor sleep", "Stress", "Vitamin deficiency"],
    "stomach pain": ["Ulcer", "Indigestion", "Food poisoning", "Appendicitis"],
}

LIFESTYLE_TIPS = [
    "Drink at least 2–3 liters of water daily.",
    "Avoid screens for 30 minutes before sleeping.",
    "Include green veggies in 2 meals a day.",
    "Do 15 minutes of breathing exercises daily.",
    "Take short walks after meals for better digestion.",
]

def check_symptoms(symptoms: list[str]):
    matched = {}
    for s in symptoms:
        s = s.lower()
        if s in SYMPTOM_DB:
            matched[s] = random.choice(SYMPTOM_DB[s])
        else:
            matched[s] = "No clear match. Consult a doctor."
    return matched

def get_health_advice(age: int, activity_level: str):
    base = random.sample(LIFESTYLE_TIPS, 3)
    if age > 40:
        base.append("Schedule regular blood pressure and sugar checks.")
    if activity_level.lower() == "low":
        base.append("Try short stretching sessions each morning.")
    return base

def generate_wellness_report(user: dict):
    name = user.get("name", "User")
    symptoms = user.get("symptoms", [])
    diagnosis = check_symptoms(symptoms)
    advice = get_health_advice(user.get("age", 25), user.get("activity", "medium"))
    return {
        "name": name,
        "diagnosis": diagnosis,
        "advice": advice,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }