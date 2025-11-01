"""
ai_tutor_helper.py
Premium AI Tutor helper module.
Supports multi-subject tutoring, step-by-step explanations,
adaptive difficulty, quizzes, hints, and progress tracking.
"""

import random
from datetime import datetime
from collections import defaultdict

# Subjects and topics
SUBJECTS = {
    "Math": ["Algebra", "Calculus", "Geometry", "Probability"],
    "Science": ["Physics", "Chemistry", "Biology", "Astronomy"],
    "History": ["Ancient", "Medieval", "Modern", "World Wars"],
    "Technology": ["AI", "Programming", "Networking", "Cybersecurity"]
}

# User progress storage
USER_PROGRESS = defaultdict(lambda: {
    "completed_topics": defaultdict(int),
    "practice_attempts": defaultdict(int),
    "hints_used": defaultdict(int)
})

class AITutorHelper:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.progress = USER_PROGRESS[user_id]

    def get_subject_topics(self, subject: str):
        return SUBJECTS.get(subject, [])

    def provide_hint(self, subject: str, topic: str):
        self.progress["hints_used"][topic] += 1
        hints = [
            f"Focus on key formulas in {topic}.",
            f"Break down the problem in {topic} step by step.",
            f"Think of real-world applications of {topic}.",
            f"Remember the fundamentals before attempting advanced problems."
        ]
        return random.choice(hints)

    def explain_step_by_step(self, subject: str, topic: str, problem: str):
        explanation_steps = [
            f"Step 1: Understand the {topic} problem: {problem}",
            f"Step 2: Identify relevant concepts from {topic}.",
            f"Step 3: Apply formulas or rules systematically.",
            f"Step 4: Solve the problem incrementally.",
            f"Step 5: Verify the solution and double-check calculations."
        ]
        return explanation_steps

    def practice_problem(self, subject: str, topic: str, difficulty: str = "easy"):
        self.progress["practice_attempts"][topic] += 1
        # Mock question generation
        question = f"{topic} question for {difficulty} difficulty"
        answer = f"{topic} answer for {difficulty} difficulty"
        return {"question": question, "answer": answer}

    def record_completion(self, topic: str):
        self.progress["completed_topics"][topic] += 1
        return f"Recorded completion of {topic}."

    def adaptive_difficulty(self, topic: str):
        attempts = self.progress["practice_attempts"].get(topic, 0)
        if attempts < 3:
            return "easy"
        elif attempts < 6:
            return "medium"
        else:
            return "hard"

    def summary_progress(self):
        summary = {
            "completed_topics": dict(self.progress["completed_topics"]),
            "practice_attempts": dict(self.progress["practice_attempts"]),
            "hints_used": dict(self.progress["hints_used"])
        }
        return summary

# Example usage
if __name__ == "__main__":
    tutor = AITutorHelper("user001")
    subject = "Math"
    topic = "Algebra"

    print("Available Topics:", tutor.get_subject_topics(subject))
    print("Hint:", tutor.provide_hint(subject, topic))
    print("Explanation Steps:", tutor.explain_step_by_step(subject, topic, "Solve x + 5 = 12"))
    practice = tutor.practice_problem(subject, topic, tutor.adaptive_difficulty(topic))
    print("Practice Problem:", practice)
    print(tutor.record_completion(topic))
    print("User Progress Summary:", tutor.summary_progress())