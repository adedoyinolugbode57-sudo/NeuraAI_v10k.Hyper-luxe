"""
reminder_system.py
Set and check reminders for users.
"""

REMINDERS = {}  # user_id -> list of reminders

def set_reminder(user_id: str, reminder: str):
    REMINDERS.setdefault(user_id, []).append(reminder)

def get_reminders(user_id: str):
    return REMINDERS.get(user_id, [])