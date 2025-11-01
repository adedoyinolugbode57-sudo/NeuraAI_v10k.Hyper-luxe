"""
health_advisor.py
Premium Health Advisor for Neuraluxe-AI.
Provides fitness, nutrition, mental health, hydration, sleep, exercise plans, and daily wellness reminders.
"""

import random
from datetime import datetime, timedelta
from collections import defaultdict

# Mock user health profiles
USER_PROFILES = defaultdict(lambda: {
    "age": 25,
    "weight_kg": 70,
    "height_cm": 175,
    "gender": "male",
    "fitness_goal": "maintain",
    "sleep_hours": 7,
    "hydration_liters": 2,
    "mental_health_score": 80
})

# Predefined health tips
FITNESS_TIPS = [
    "Warm-up before workouts to prevent injury.",
    "Include both cardio and strength training in your routine.",
    "Consistency is key: exercise at least 3-5 times per week."
]

NUTRITION_TIPS = [
    "Eat at least 5 servings of fruits and vegetables daily.",
    "Drink plenty of water throughout the day.",
    "Balance your meals with protein, carbs, and healthy fats."
]

MENTAL_HEALTH_TIPS = [
    "Practice mindfulness or meditation daily.",
    "Take short breaks to reduce mental fatigue.",
    "Maintain social connections for better mental well-being."
]

SLEEP_TIPS = [
    "Aim for 7-9 hours of quality sleep each night.",
    "Keep a consistent sleep schedule.",
    "Avoid screens 1 hour before bedtime."
]

class HealthAdvisor:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.profile = USER_PROFILES[user_id]

    # ---------------------------
    # Fitness & Exercise Methods
    # ---------------------------
    def daily_exercise_plan(self):
        exercises = ["Push-ups", "Squats", "Lunges", "Plank", "Jumping Jacks", "Burpees"]
        plan = random.sample(exercises, k=4)
        return f"Today's exercise plan: {', '.join(plan)}."

    def suggest_fitness_tip(self):
        return random.choice(FITNESS_TIPS)

    def weekly_progress_feedback(self):
        completed_sessions = random.randint(0, 5)
        goal = 5
        if completed_sessions >= goal:
            return f"Great job! You completed {completed_sessions}/{goal} sessions this week."
        return f"You completed {completed_sessions}/{goal} sessions. Keep pushing!"

    # ---------------------------
    # Nutrition & Hydration
    # ---------------------------
    def daily_meal_suggestion(self):
        meals = ["Oatmeal with fruits", "Grilled chicken salad", "Quinoa and veggies", "Smoothie bowl"]
        return f"Today's suggested meal: {random.choice(meals)}."

    def hydration_reminder(self):
        return f"Reminder: Drink at least {self.profile['hydration_liters']} liters of water today."

    def nutrition_tip(self):
        return random.choice(NUTRITION_TIPS)

    # ---------------------------
    # Mental Health
    # ---------------------------
    def mental_health_check(self):
        score = self.profile["mental_health_score"] + random.randint(-5, 5)
        status = "Good" if score >= 75 else "Moderate" if score >= 50 else "Needs attention"
        return f"Mental Health Score: {score}/100 - {status}"

    def suggest_mental_health_tip(self):
        return random.choice(MENTAL_HEALTH_TIPS)

    # ---------------------------
    # Sleep
    # ---------------------------
    def sleep_advice(self):
        hours = self.profile["sleep_hours"]
        if hours < 7:
            return "You need more sleep for optimal health."
        elif hours > 9:
            return "You might be oversleeping. Aim for 7-9 hours."
        return "Your sleep duration is healthy."

    def sleep_tip(self):
        return random.choice(SLEEP_TIPS)

    # ---------------------------
    # Health Summary
    # ---------------------------
    def full_daily_health_summary(self):
        summary = {
            "Exercise Plan": self.daily_exercise_plan(),
            "Fitness Tip": self.suggest_fitness_tip(),
            "Meal Suggestion": self.daily_meal_suggestion(),
            "Hydration Reminder": self.hydration_reminder(),
            "Nutrition Tip": self.nutrition_tip(),
            "Mental Health": self.mental_health_check(),
            "Mental Health Tip": self.suggest_mental_health_tip(),
            "Sleep Advice": self.sleep_advice(),
            "Sleep Tip": self.sleep_tip()
        }
        return summary

# Example usage
if __name__ == "__main__":
    advisor = HealthAdvisor("user123")
    summary = advisor.full_daily_health_summary()
    for k, v in summary.items():
        print(f"{k}: {v}")