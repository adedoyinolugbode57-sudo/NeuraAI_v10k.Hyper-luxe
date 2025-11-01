"""
session_utils.py
Independent session utilities for Neuraluxe-AI.
"""
sessions = {}

def create_session(user_id):
    sessions[user_id] = {}
    return sessions[user_id]

def get_session(user_id):
    return sessions.get(user_id, {})