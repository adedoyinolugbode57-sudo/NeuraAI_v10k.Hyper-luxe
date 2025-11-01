import random
def generate_token(user_id: str) -> str:
    return f"{user_id}-{random.randint(100000,999999)}"