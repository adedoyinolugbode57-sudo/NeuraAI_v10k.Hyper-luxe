"""
quiz_generator.py
Premium AI-driven quiz generator with multi-subjects, scoring, and hints.
"""

import random
from collections import defaultdict
from datetime import datetime

SUBJECTS = ["Math", "Science", "History", "Geography", "Technology", "AI"]
USER_SCORES = defaultdict(lambda: {"total_score":0, "history":[]})

QUESTIONS_BANK = {
    "Math": [
        {"question": "What is 12 * 8?", "answer": "96", "difficulty": "easy"},
        {"question": "Solve for x: 2x + 7 = 15", "answer": "4", "difficulty": "medium"},
        {"question": "Integral of x dx?", "answer": "0.5x^2 + C", "difficulty": "hard"}
    ],
    "Science": [
        {"question": "What is the chemical symbol for Gold?", "answer": "Au", "difficulty": "easy"},
        {"question": "What planet is known as the Red Planet?", "answer": "Mars", "difficulty": "easy"},
        {"question": "What is the powerhouse of the cell?", "answer": "Mitochondria", "difficulty": "medium"}
    ]
}

class QuizGenerator:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.user_data = USER_SCORES[user_id]

    def generate_question(self, subject: str, difficulty: str = None):
        subject_questions = QUESTIONS_BANK.get(subject, [])
        if difficulty:
            subject_questions = [q for q in subject_questions if q["difficulty"]==difficulty]
        if not subject_questions:
            return {"question":"No questions available", "answer": None}
        return random.choice(subject_questions)

    def submit_answer(self, question: dict, answer: str):
        correct = question["answer"].lower() == answer.lower()
        score = 10 if correct else 0
        self.user_data["total_score"] += score
        self.user_data["history"].append({
            "question": question["question"],
            "your_answer": answer,
            "correct_answer": question["answer"],
            "score": score,
            "timestamp": datetime.now()
        })
        return correct, score

    def get_score(self):
        return self.user_data["total_score"]

# Example usage
if __name__ == "__main__":
    quiz = QuizGenerator("user123")
    q = quiz.generate_question("Math", "easy")
    print(q)
    print(quiz.submit_answer(q, "96"))
    print("Total Score:", quiz.get_score())