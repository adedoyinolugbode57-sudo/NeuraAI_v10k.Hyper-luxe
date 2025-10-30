# crypto_insights_hyperluxe.py
"""
NeuraAI_v10k.HyperLuxe — Crypto Insights Engine (Premium Patch)
Integrates with chat UI for neon alerts, voice, and portfolio advice.
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path

CACHE_FILE = Path(__file__).parent / "data" / "crypto_cache.json"
REPORTS_DIR = Path(__file__).parent / "reports"
CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DURATION = 300  # seconds

CRYPTO_LIST = ["bitcoin", "ethereum", "solana", "bnb", "dogecoin", "cardano", "polkadot"]

# ----- Cache Helpers -----
def _save_cache(data):
    CACHE_FILE.write_text(json.dumps({"time": time.time(), "data": data}, indent=2), encoding="utf-8")

def _load_cache():
    if not CACHE_FILE.exists():
        return None
    content = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    if time.time() - content["time"] > CACHE_DURATION:
        return None
    return content["data"]

# ----- API Fetch -----
def _fetch_api():
    """Fetch live prices from CoinGecko."""
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

# ----- Utilities -----
def format_price(value):
    return "${:,.2f}".format(value)

def neon_alert(change):
    """Return alert emoji for neon-style UI."""
    if change > 5:
        return "🚀"
    elif change < -5:
        return "⚠️"
    return "💡"

# ----- Summaries -----
def crypto_summary():
    data = get_market_data()
    summary = []
    for coin in data:
        change = coin.get("price_change_percentage_24h", 0)
        summary.append({
            "name": coin["name"],
            "symbol": coin["symbol"].upper(),
            "price": format_price(coin["current_price"]),
            "change_24h": f"{change:.2f}%",
            "market_cap": format_price(coin.get("market_cap", 0)),
            "advice": neon_alert(change),
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
                "advice": neon_alert((coin.get("price_change_percentage_24h") or 0))
            })
    return {"total_usd": total, "details": details}

def portfolio_advice(holdings: dict):
    data = get_portfolio_value(holdings)
    total = data["total_usd"]
    advice = "✅ Portfolio balanced."
    if total < 100:
        advice = "💡 Start small — stablecoins suggested."
    elif total > 50000:
        advice = "⚠️ High exposure — consider rebalancing."
    return {"total": format_price(total), "advice": advice}

# ----- Report Export -----
def export_report(holdings: dict):
    summary = portfolio_advice(holdings)
    details = get_portfolio_value(holdings)
    report = {
        "time": datetime.utcnow().isoformat(),
        "summary": summary,
        "details": details,
        "market_snapshot": crypto_summary(),
    }
    report_path = REPORTS_DIR / f"report_{int(time.time())}.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return str(report_path)

# ----- Neon Top Coins -----
def rank_top_coins(limit=5):
    data = get_market_data()
    sorted_coins = sorted(data, key=lambda x: x.get("market_cap", 0), reverse=True)
    return [{
        "rank": i + 1,
        "name": c["name"],
        "price": format_price(c["current_price"]),
        "change": f"{c['price_change_percentage_24h']:.2f}%",
        "alert": neon_alert(c["price_change_percentage_24h"] or 0)
    } for i, c in enumerate(sorted_coins[:limit])]

# ----- Example CLI Mode -----
if __name__ == "__main__":
    holdings_example = {"bitcoin": 0.01, "ethereum": 0.05}
    print("🌟 Top Coins:\n", rank_top_coins())
    print("\n💰 Portfolio:\n", get_portfolio_value(holdings_example))
    print("\n📊 Advice:\n", portfolio_advice(holdings_example))
    print("\n📝 Report Export Path:\n", export_report(holdings_example))