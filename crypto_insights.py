# crypto_insights.py
"""
NeuraAI_v10k.HyperLuxe — Crypto Insights Engine
Provides live cryptocurrency data, smart signals, and portfolio analytics.
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path

CACHE_FILE = Path(__file__).parent / "data" / "crypto_cache.json"
CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
CACHE_DURATION = 300  # seconds

CRYPTO_LIST = ["bitcoin", "ethereum", "solana", "bnb", "dogecoin", "cardano", "polkadot"]

def _save_cache(data):
    CACHE_FILE.write_text(json.dumps({"time": time.time(), "data": data}, indent=2), encoding="utf-8")

def _load_cache():
    if not CACHE_FILE.exists():
        return None
    content = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    if time.time() - content["time"] > CACHE_DURATION:
        return None
    return content["data"]

def _fetch_api():
    """Get live prices from CoinGecko."""
    try:
        resp = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={"vs_currency": "usd", "ids": ",".join(CRYPTO_LIST)},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print("[!] API error:", e)
        return None

def get_market_data(force_refresh=False):
    if not force_refresh:
        cache = _load_cache()
        if cache:
            return cache
    data = _fetch_api()
    if data:
        _save_cache(data)
    return data or []

def format_price(value):
    return "${:,.2f}".format(value)

def crypto_summary():
    data = get_market_data()
    summary = []
    for coin in data:
        change = coin.get("price_change_percentage_24h", 0)
        advice = "Hold"
        if change > 5:
            advice = "Buy 🚀"
        elif change < -5:
            advice = "Sell ⚠️"
        summary.append({
            "name": coin["name"],
            "symbol": coin["symbol"].upper(),
            "price": format_price(coin["current_price"]),
            "change_24h": f"{change:.2f}%",
            "market_cap": format_price(coin.get("market_cap", 0)),
            "advice": advice,
        })
    return summary

def get_portfolio_value(holdings: dict):
    """
    holdings = {'bitcoin': 0.002, 'ethereum': 0.1}
    """
    data = get_market_data()
    total = 0.0
    details = []
    for coin in data:
        sym = coin["id"]
        if sym in holdings:
            val = holdings[sym] * coin["current_price"]
            total += val
            details.append({
                "coin": sym,
                "amount": holdings[sym],
                "usd_value": val,
                "price": coin["current_price"],
            })
    return {"total_usd": total, "details": details}

def rank_top_coins(limit=5):
    data = get_market_data()
    sorted_coins = sorted(data, key=lambda x: x["market_cap"], reverse=True)
    return [{
        "rank": i + 1,
        "name": c["name"],
        "price": format_price(c["current_price"]),
        "change": f"{c['price_change_percentage_24h']:.2f}%",
    } for i, c in enumerate(sorted_coins[:limit])]

def portfolio_advice(holdings: dict):
    data = get_portfolio_value(holdings)
    total = data["total_usd"]
    advice = "✅ Well balanced."
    if total < 100:
        advice = "💡 Start small — consider buying stable coins."
    elif total > 50000:
        advice = "⚠️ High exposure — rebalance portfolio."
    return {"total": format_price(total), "advice": advice}

def export_report(holdings: dict):
    summary = portfolio_advice(holdings)
    details = get_portfolio_value(holdings)
    report = {
        "time": datetime.utcnow().isoformat(),
        "summary": summary,
        "details": details,
        "market_snapshot": crypto_summary(),
    }
    report_path = Path(__file__).parent / "reports" / f"report_{int(time.time())}.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return str(report_path)

if __name__ == "__main__":
    # Example
    print("Top coins:\n", rank_top_coins())
    print("Portfolio:\n", get_portfolio_value({"bitcoin": 0.01, "ethereum": 0.05}))
    print("Advice:\n", portfolio_advice({"bitcoin": 0.01, "ethereum": 0.05}))