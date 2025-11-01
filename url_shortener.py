"""
url_shortener.py
Shorten URLs (mock).
"""

def shorten(url: str) -> str:
    return "https://short.ly/" + str(abs(hash(url)))[:6]