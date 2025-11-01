"""
mock_api_responder.py
Simulate API responses.
"""

def respond(endpoint: str):
    return {"endpoint": endpoint, "status": "success", "data": {}}