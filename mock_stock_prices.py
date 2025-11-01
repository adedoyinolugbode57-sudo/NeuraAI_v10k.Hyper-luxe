"""
mock_stock_prices.py
Return random stock prices (mock).
"""

import random

def get_stock_price(symbol: str) -> float:
    return round(random.uniform(10, 500), 2)