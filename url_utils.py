"""
url_utils.py
Independent URL utilities for Neuraluxe-AI.
"""
from urllib.parse import urlparse, parse_qs

def get_domain(url: str):
    return urlparse(url).netloc

def get_query_param(url: str, key: str):
    return parse_qs(urlparse(url).query).get(key, [None])[0]