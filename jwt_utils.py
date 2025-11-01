"""
jwt_utils.py
Independent JWT utilities for Neuraluxe-AI.
"""
import jwt
import datetime

SECRET = "neuraluxe-secret-demo"

def create_token(payload: dict, expire_minutes=60):
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=expire_minutes)
    return jwt.encode(payload, SECRET, algorithm="HS256")

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except Exception:
        return None