from datetime import datetime, timedelta

class PremiumLimiter:
    def __init__(self):
        self.user_limits = {}

    def can_use(self, user_id: str):
        now = datetime.now()
        last_used = self.user_limits.get(user_id)
        if last_used and now - last_used < timedelta(hours=12):
            return False
        self.user_limits[user_id] = now
        return True