class FeedbackCollector:
    def __init__(self):
        self.feedback = []

    def add_feedback(self, user_id: str, text: str):
        self.feedback.append({"user_id": user_id, "text": text})
        return "Feedback recorded."

    def analyze_feedback(self):
        return {"total_feedback": len(self.feedback)}