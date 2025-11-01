"""
notification_manager.py
Mock notification handler.
"""
def send_notification(user_id: str, message: str) -> str:
    return f"Notification sent to {user_id}: {message}"