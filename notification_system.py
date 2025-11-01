"""
notification_system.py
Send alerts to user for limits or events.
"""

def notify(user_id: str, message: str):
    print(f"Notification for {user_id}: {message}")