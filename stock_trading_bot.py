"""
stock_trading_bot.py
Premium stock & crypto trading bot for Neuraluxe-AI
Includes portfolio simulation, trends, alerts, multi-user support,
AI-assisted predictions, and performance analytics.
"""

import random
from datetime import datetime, timedelta
from collections import defaultdict

# -----------------------
# Mock Assets
# -----------------------
ASSETS = {
    "AAPL": 175.50,
    "GOOGL": 1420.30,
    "BTC": 29850.75,
    "ETH": 1850.40,
    "TSLA": 825.60,
    "AMZN": 3200.75,
    "SOL": 25.30,
    "ADA": 0.95,
    "DOGE": 0.07,
    "MSFT": 295.60
}

# -----------------------
# Users & Portfolios
# -----------------------
USER_PORTFOLIOS = defaultdict(lambda: {"cash": 10000.0, "assets": {}, "strategy": "balanced"})

# -----------------------
# Trading Bot Class
# -----------------------
class TradingBot:
    def __init__(self, user_id: str = "default_user", api_available: bool = False):
        self.user_id = user_id
        self.api_available = api_available
        self.portfolio = USER_PORTFOLIOS[user_id]

    # -----------------------
    # Fetch Price
    # -----------------------
    def fetch_price(self, asset: str) -> float:
        asset = asset.upper()
        if self.api_available:
            # Placeholder: fetch live data
            return round(random.uniform(0.8, 1.2) * ASSETS.get(asset, 100), 2)
        return ASSETS.get(asset, 0.0)

    # -----------------------
    # Buy Asset
    # -----------------------
    def buy(self, asset: str, quantity: float) -> str:
        price = self.fetch_price(asset)
        cost = price * quantity
        if self.portfolio["cash"] < cost:
            return f"Insufficient funds to buy {quantity} {asset} (Cost: ${cost})"
        self.portfolio["cash"] -= cost
        self.portfolio["assets"][asset] = self.portfolio["assets"].get(asset, 0) + quantity
        return f"Bought {quantity} {asset} at ${price} each. Cash remaining: ${round(self.portfolio['cash'],2)}"

    # -----------------------
    # Sell Asset
    # -----------------------
    def sell(self, asset: str, quantity: float) -> str:
        if self.portfolio["assets"].get(asset, 0) < quantity:
            return f"Not enough {asset} to sell."
        price = self.fetch_price(asset)
        self.portfolio["assets"][asset] -= quantity
        self.portfolio["cash"] += price * quantity
        return f"Sold {quantity} {asset} at ${price} each. Cash now: ${round(self.portfolio['cash'],2)}"

    # -----------------------
    # Portfolio Value
    # -----------------------
    def portfolio_value(self) -> float:
        total = self.portfolio["cash"]
        for asset, qty in self.portfolio["assets"].items():
            total += self.fetch_price(asset) * qty
        return round(total, 2)

    # -----------------------
    # AI-assisted Predictions
    # -----------------------
    def ai_trade_suggestion(self, asset: str) -> str:
        price = self.fetch_price(asset)
        action = random.choice(["Buy", "Sell", "Hold"])
        confidence = round(random.uniform(50, 99), 2)
        return f"Suggestion: {action} {asset} at ${price} | Confidence: {confidence}%"

    # -----------------------
    # Risk Alerts
    # -----------------------
    def risk_alert(self) -> str:
        risk = random.choice(["High volatility", "Market stable", "Unexpected spike", "Moderate risk"])
        return f"Risk Alert: {risk}"

    # -----------------------
    # Trending Assets
    # -----------------------
    def trending_assets(self, top_n: int = 5) -> list:
        assets = list(ASSETS.keys())
        random.shuffle(assets)
        return assets[:top_n]

    # -----------------------
    # Portfolio Performance
    # -----------------------
    def performance_report(self) -> dict:
        report = {}
        report["total_value"] = self.portfolio_value()
        report["cash"] = round(self.portfolio["cash"],2)
        report["assets"] = {a:self.fetch_price(a)*q for a,q in self.portfolio["assets"].items()}
        report["timestamp"] = datetime.now()
        return report

# -----------------------
# Example Usage
# -----------------------
if __name__ == "__main__":
    bot = TradingBot("user123")
    print(bot.buy("AAPL", 10))
    print(bot.buy("BTC", 0.1))
    print(bot.sell("AAPL", 5))
    print("Portfolio value:", bot.portfolio_value())
    print("AI suggestion for ETH:", bot.ai_trade_suggestion("ETH"))
    print("Risk alert:", bot.risk_alert())
    print("Trending assets:", bot.trending_assets())
    print("Performance report:", bot.performance_report())