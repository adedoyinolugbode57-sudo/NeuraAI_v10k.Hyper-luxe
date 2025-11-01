"""
conversation_logger.py
Log chat conversations for debugging/review.
"""

logs = []

def log_message(user_id: str, message: str, response: str):
    logs.append({"user": user_id, "message": message, "response": response})

def get_logs():
    return logs

# Example
if __name__ == "__main__":
    log_message("user123", "Hi", "Hello!")
    print(get_logs())