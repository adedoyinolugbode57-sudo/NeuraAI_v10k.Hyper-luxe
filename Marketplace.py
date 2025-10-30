"""
marketplace.py — Neuraluxe-AI Marketplace Backend (scalable simulation)
- Blueprint providing paginated/searchable items and purchase flow
- Items simulated on-the-fly (supports millions without heavy memory)
- Prices start at $29.99
- Purchase flow returns a checkout URL (mock). Developer bypass auto-confirms.
"""

import os
import json
import uuid
import math
import random
from datetime import datetime
from flask import Blueprint, request, jsonify

market_bp = Blueprint("market_bp", __name__)

# -----------------------------
# Configuration
# -----------------------------
DEV_EMAIL = "adedoyinolugbode57@gmail.com"  # developer / founder free account
PURCHASES_FILE = "marketplace_purchases.json"

# Marketplace simulation parameters
TOTAL_SIMULATED_ITEMS = 1_000_000  # simulate up to one million items
DEFAULT_PAGE_SIZE = 24
MIN_PRICE = 29.99
MAX_PRICE = 999999.00
CATEGORIES = [
    "AI Tools", "Automation Bots", "Trading Scripts", "Freelancer Tools",
    "Design Studio", "Crypto Assets", "Voice & Language", "Education Packs",
    "Developer Plugins", "Global Add-Ons"
]

# Ensure purchases file exists
if not os.path.exists(PURCHASES_FILE):
    with open(PURCHASES_FILE, "w", encoding="utf-8") as f:
        json.dump({"purchases": []}, f, indent=2)


# -----------------------------
# Helpers
# -----------------------------
def _gen_item_by_index(idx: int) -> dict:
    """Deterministically generate an item dict from an index (1-based)."""
    # Keep index within reasonable bounds
    if idx < 1:
        idx = 1
    if idx > TOTAL_SIMULATED_ITEMS:
        idx = idx % TOTAL_SIMULATED_ITEMS or TOTAL_SIMULATED_ITEMS

    # deterministic pseudo-randomness based on index
    rnd = random.Random(idx)
    category = rnd.choice(CATEGORIES)
    base_name = {
        "AI Tools": "Neuraluxe AI Tool",
        "Automation Bots": "AutoFlow Bot",
        "Trading Scripts": "Neuraluxe Trader",
        "Freelancer Tools": "Freelance Boost Kit",
        "Design Studio": "Studio Pack",
        "Crypto Assets": "Crypto Signal Module",
        "Voice & Language": "Voice Pack",
        "Education Packs": "Learning Module",
        "Developer Plugins": "Dev Plugin",
        "Global Add-Ons": "Legacy Add-On"
    }.get(category, "Neuraluxe Asset")

    # price scaled by index (but bounded)
    price = MIN_PRICE + ((idx % 1000) * ( (MAX_PRICE - MIN_PRICE) / 1000 ))
    # small variation
    price = round(price + rnd.uniform(0, 49.99), 2)
    item_id = f"nli-{idx:07d}"  # e.g., nli-0000001

    return {
        "id": item_id,
        "index": idx,
        "name": f"{base_name} #{idx}",
        "category": category,
        "price": price,
        "currency": "USD",
        "rarity": rnd.choice(["Common", "Rare", "Ultra", "Limited"]),
        "description": f"A premium {category.lower()} designed for instant productivity and AI-enhanced workflows.",
        "created_at": datetime.utcnow().isoformat()
    }


def _read_purchases():
    try:
        with open(PURCHASES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"purchases": []}


def _save_purchase(record: dict):
    data = _read_purchases()
    data["purchases"].append(record)
    with open(PURCHASES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# -----------------------------
# Marketplace Endpoints
# -----------------------------

@market_bp.route("/api/market/items", methods=["GET"])
def list_items():
    """
    Query params:
      - page (1-based)
      - page_size
      - q (search query)
      - category
      - min_price
      - max_price
    Returns:
      {
        "items": [...],
        "total": int,
        "page": int,
        "page_size": int,
        "total_pages": int
      }
    """
    try:
        page = max(int(request.args.get("page", 1)), 1)
    except Exception:
        page = 1
    try:
        page_size = min(int(request.args.get("page_size", DEFAULT_PAGE_SIZE)), 200)
    except Exception:
        page_size = DEFAULT_PAGE_SIZE

    q = (request.args.get("q") or "").strip().lower()
    category = (request.args.get("category") or "").strip()
    try:
        min_price = float(request.args.get("min_price")) if request.args.get("min_price") else MIN_PRICE
    except Exception:
        min_price = MIN_PRICE
    try:
        max_price = float(request.args.get("max_price")) if request.args.get("max_price") else MAX_PRICE
    except Exception:
        max_price = MAX_PRICE

    # To support large simulated dataset, we'll scan through index ranges and apply simple filter heuristics.
    # For performance we won't scan 1M items each request — instead, allow:
    # - exact category filter: choose an index step that matches category distribution for deterministic results
    # - query search: naive substring on generated names (will examine a window around requested page)
    # We'll pick an index window corresponding to page to keep O(page_size) work.

    # Compute start index for the page (1-based)
    start_index = (page - 1) * page_size + 1
    end_index = start_index + page_size - 1

    items = []
    # generate only the needed items for this page
    for idx in range(start_index, end_index + 1):
        if idx > TOTAL_SIMULATED_ITEMS:
            break
        item = _gen_item_by_index(idx)

        # filters
        if category and item["category"].lower() != category.lower():
            continue
        if item["price"] < min_price or item["price"] > max_price:
            continue
        if q:
            if q not in item["name"].lower() and q not in item["category"].lower():
                continue

        items.append(item)

    # For a simulated dataset, approximate total as TOTAL_SIMULATED_ITEMS (or filtered estimate)
    total_estimate = TOTAL_SIMULATED_ITEMS
    # If filters significantly reduce matches, this API still returns a page of results
    total_pages = math.ceil(total_estimate / page_size)

    return jsonify({
        "items": items,
        "total": total_estimate,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    })


@market_bp.route("/api/market/item/<item_id>", methods=["GET"])
def get_item(item_id):
    """
    Fetch a single item by deterministic id: nli-0000001 etc.
    """
    if not item_id or not item_id.startswith("nli-"):
        return jsonify({"error": "invalid_id"}), 400
    try:
        idx = int(item_id.split("-")[1])
    except Exception:
        return jsonify({"error": "invalid_id_format"}), 400
    item = _gen_item_by_index(idx)
    return jsonify({"item": item})


@market_bp.route("/api/market/purchase", methods=["POST"])
def purchase_item():
    """
    Body JSON:
      {
        "user_email": "user@example.com",
        "item_id": "nli-0000007",
        "payment_method": "payoneer" (optional),
        "quantity": 1
      }

    Response:
      {
        "status": "pending"|"success",
        "checkout_url": "...",
        "transaction_id": "...",
        "message": "..."
      }
    """
    data = request.get_json() or {}
    user_email = (data.get("user_email") or "").strip()
    item_id = data.get("item_id")
    payment_method = (data.get("payment_method") or "payoneer").lower()
    quantity = int(data.get("quantity", 1))

    if not user_email:
        return jsonify({"status": "error", "message": "user_email required"}), 400
    if not item_id:
        return jsonify({"status": "error", "message": "item_id required"}), 400

    # fetch item (deterministic)
    try:
        idx = int(item_id.split("-")[1])
        item = _gen_item_by_index(idx)
    except Exception:
        return jsonify({"status": "error", "message": "invalid item_id"}), 400

    total_amount = round(item["price"] * max(1, quantity), 2)

    # Developer bypass: instant success (no checkout required)
    if user_email.lower() == DEV_EMAIL.lower():
        tx_id = f"dev_{uuid.uuid4().hex[:10]}"
        purchase_record = {
            "transaction_id": tx_id,
            "user_email": user_email,
            "item_id": item_id,
            "amount": 0.0,
            "currency": item["currency"],
            "status": "completed",
            "created_at": datetime.utcnow().isoformat(),
            "payment_method": "dev-bypass"
        }
        _save_purchase(purchase_record)
        return jsonify({
            "status": "success",
            "message": "Developer bypass: purchase completed for free.",
            "transaction_id": tx_id,
            "receipt": purchase_record
        })

    # Normal flow: create transaction record and return a mock checkout URL
    txn_id = f"txn_{uuid.uuid4().hex[:12]}"
    checkout_url = f"https://payoneer.com/checkout?session={txn_id}&amount={total_amount}&currency={item['currency']}&item={item_id}"

    purchase_record = {
        "transaction_id": txn_id,
        "user_email": user_email,
        "item_id": item_id,
        "amount": total_amount,
        "currency": item["currency"],
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
        "payment_method": payment_method,
        "checkout_url": checkout_url
    }
    _save_purchase(purchase_record)

    return jsonify({
        "status": "pending",
        "message": "Checkout session created. Redirect user to checkout_url to complete payment.",
        "transaction_id": txn_id,
        "checkout_url": checkout_url
    })


@market_bp.route("/api/market/purchase/status/<transaction_id>", methods=["GET"])
def purchase_status(transaction_id):
    """Return purchase status for a transaction id."""
    data = _read_purchases()
    rec = next((r for r in data.get("purchases", []) if r.get("transaction_id") == transaction_id), None)
    if not rec:
        return jsonify({"status": "error", "message": "transaction not found"}), 404
    return jsonify({"status": rec.get("status", "unknown"), "transaction": rec})


# Optional admin endpoint to list recent purchases (safe to protect later)
@market_bp.route("/admin/market/purchases", methods=["GET"])
def admin_list_purchases():
    data = _read_purchases()
    # return last 100 purchases
    purchases = data.get("purchases", [])[-100:][::-1]
    return jsonify({"count": len(purchases), "recent": purchases})


# -----------------------------
# Register helper
# -----------------------------
def register_marketplace(app):
    """Register this blueprint on a Flask app"""
    app.register_blueprint(market_bp)


# -----------------------------
# Standalone debug run
# -----------------------------
if __name__ == "__main__":
    from flask import Flask
    a = Flask(__name__)
    register_marketplace(a)
    a.run(host="0.0.0.0", port=5055, debug=True)