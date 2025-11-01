"""
ai_trading_bridge.py
Neuraluxe-AI — Trading Bridge (Coordinator for multiple trading bots)

Responsibilities:
- Manage multiple trading bots per user
- Shared market data cache & feature store
- Centralized risk management and exposure limits
- Broker adapter interface (mock included) with safe execution
- Backtest / paper-trade mode and live mode
- Event bus for real-time coordination & telemetry
- Persistence: SQLite primary, JSON fallback
- Simple strategy registration API (programmatic)
- Graceful shutdown, metrics, and audit logging

NOT FINANCIAL ADVICE. Use at your own risk. This module provides orchestration and safety
controls for algorithmic strategies but does NOT guarantee profits or prevent losses.

Author: ChatGPT + Joshua Dav
"""

import os
import time
import json
import uuid
import math
import sqlite3
import random
import threading
import logging
from typing import Dict, Any, List, Optional, Callable, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, deque

# ---------------------------
# Configuration
# ---------------------------
DB_FILE = os.getenv("NEURA_TRADES_DB", "neuraluxe_trades.db")
PERSIST_JSON = os.getenv("NEURA_TRADES_JSON", "trades_state.json")
DEFAULT_MAX_EXPOSURE = float(os.getenv("NEURA_MAX_EXPOSURE_USD", "50000"))  # default per-user exposure
DEFAULT_MAX_POSITIONS = int(os.getenv("NEURA_MAX_POSITIONS", "10"))
HEARTBEAT_INTERVAL = int(os.getenv("NEURA_TRADING_HEARTBEAT", "5"))  # seconds
ORDER_ID_PREFIX = "ntx"

# ---------------------------
# Logging
# ---------------------------
logger = logging.getLogger("neura_trading")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

# ---------------------------
# Persistence helpers (SQLite preferred)
# ---------------------------
def _init_db(path: str = DB_FILE):
    need_init = not os.path.exists(path)
    conn = sqlite3.connect(path, check_same_thread=False)
    if need_init:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                bot_id TEXT,
                symbol TEXT,
                side TEXT,
                qty REAL,
                price REAL,
                status TEXT,
                created_at INTEGER,
                executed_at INTEGER,
                meta JSON
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS positions (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                symbol TEXT,
                qty REAL,
                avg_price REAL,
                updated_at INTEGER
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS audit (
                id TEXT PRIMARY KEY,
                ts INTEGER,
                level TEXT,
                message TEXT,
                meta JSON
            )
        """)
        conn.commit()
    return conn

_db_conn = _init_db()

_db_lock = threading.Lock()

def db_insert_order(record: dict):
    with _db_lock:
        cur = _db_conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO orders (id,user_id,bot_id,symbol,side,qty,price,status,created_at,executed_at,meta)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (
            record["id"], record["user_id"], record["bot_id"], record["symbol"], record["side"],
            record["qty"], record.get("price"), record["status"], int(record["created_at"]), int(record.get("executed_at") or 0),
            json.dumps(record.get("meta", {}))
        ))
        _db_conn.commit()

def db_upsert_position(symbol: str, user_id: str, qty: float, avg_price: float):
    with _db_lock:
        cur = _db_conn.cursor()
        now = int(time.time())
        cur.execute("SELECT id, qty, avg_price FROM positions WHERE user_id = ? AND symbol = ?",
                    (user_id, symbol))
        row = cur.fetchone()
        if row:
            pid = row[0]
            # compute new avg price & qty
            old_qty = float(row[1])
            old_avg = float(row[2])
            new_qty = old_qty + qty
            if new_qty == 0:
                cur.execute("DELETE FROM positions WHERE id = ?", (pid,))
            else:
                new_avg = (old_avg * old_qty + avg_price * qty) / new_qty if new_qty else avg_price
                cur.execute("UPDATE positions SET qty = ?, avg_price = ?, updated_at = ? WHERE id = ?",
                            (new_qty, new_avg, now, pid))
        else:
            pid = f"pos_{uuid.uuid4().hex[:10]}"
            cur.execute("INSERT INTO positions (id,user_id,symbol,qty,avg_price,updated_at) VALUES (?,?,?,?,?,?)",
                        (pid, user_id, symbol, qty, avg_price, now))
        _db_conn.commit()

def db_insert_audit(level: str, message: str, meta: dict = None):
    with _db_lock:
        cur = _db_conn.cursor()
        aid = f"audit_{uuid.uuid4().hex[:10]}"
        now = int(time.time())
        cur.execute("INSERT INTO audit (id,ts,level,message,meta) VALUES (?,?,?,?,?)",
                    (aid, now, level, message, json.dumps(meta or {})))
        _db_conn.commit()

# JSON fallback persistence (in case SQLite unavailable)
def json_load_state(path=PERSIST_JSON):
    if not os.path.exists(path):
        return {"orders": [], "positions": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def json_save_state(state, path=PERSIST_JSON):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

# ---------------------------
# Broker Adapter Interface (pluggable)
# ---------------------------
class BrokerAdapterBase:
    """
    Minimal interface for a broker adapter:
      - execute_order(order) -> dict result
      - get_balance() -> dict
      - get_market_price(symbol) -> float
      - cancel_order(order_id) -> bool
    """
    def execute_order(self, order: dict) -> dict:
        raise NotImplementedError

    def get_balance(self, user_id: str) -> dict:
        raise NotImplementedError

    def get_market_price(self, symbol: str) -> float:
        raise NotImplementedError

    def cancel_order(self, order_id: str) -> bool:
        raise NotImplementedError

# Simple mock broker (safe, deterministic-ish)
class MockBroker(BrokerAdapterBase):
    def __init__(self):
        # per-user balance (USD) and holdings
        self.balances = defaultdict(lambda: {"USD": 100000.0})
        # open orders
        self.open_orders = {}

    def execute_order(self, order: dict) -> dict:
        """
        Simulate market execution with small slippage and immediate fill.
        Returns execution metadata.
        """
        order_id = order["id"]
        user = order["user_id"]
        symbol = order["symbol"]
        side = order["side"]
        qty = float(order["qty"])
        # simple price discovery
        price = order.get("price")
        if price is None:
            price = self.get_market_price(symbol)
        # simulate slippage
        slippage = 0.0005 * price * (random.random() - 0.5)
        exec_price = round(price + slippage, 6)
        cost = exec_price * qty
        # check balance for buys
        if side.lower() == "buy":
            if self.balances[user]["USD"] < cost:
                return {"ok": False, "error": "insufficient_funds"}
            self.balances[user]["USD"] -= cost
            # assign asset in holdings (not implemented in detail)
        else:
            # sell -> add USD
            self.balances[user]["USD"] += cost
        self.open_orders.pop(order_id, None)
        exec_meta = {"ok": True, "exec_price": exec_price, "filled_qty": qty, "timestamp": int(time.time())}
        return exec_meta

    def get_balance(self, user_id: str) -> dict:
        return dict(self.balances[user_id])

    def get_market_price(self, symbol: str) -> float:
        # simple deterministic price by hashing symbol
        base = 100.0 + (abs(hash(symbol)) % 1000) / 10.0
        noise = math.sin(time.time() / 60.0 + hash(symbol) % 100) * 0.5
        return round(base + noise, 6)

    def cancel_order(self, order_id: str) -> bool:
        if order_id in self.open_orders:
            self.open_orders.pop(order_id)
            return True
        return False

# ---------------------------
# Order structure helpers
# ---------------------------
def make_order_id():
    return f"{ORDER_ID_PREFIX}_{int(time.time())}_{uuid.uuid4().hex[:8]}"

def create_order(user_id: str, bot_id: str, symbol: str, side: str, qty: float, price: Optional[float] = None, meta: dict = None) -> dict:
    return {
        "id": make_order_id(),
        "user_id": user_id,
        "bot_id": bot_id,
        "symbol": symbol,
        "side": side.lower(),
        "qty": float(qty),
        "price": float(price) if price is not None else None,
        "status": "new",
        "created_at": int(time.time()),
        "executed_at": None,
        "meta": meta or {}
    }

# ---------------------------
# Risk Manager
# ---------------------------
class RiskManager:
    def __init__(self):
        # per-user risk policy
        self.user_limits: Dict[str, dict] = defaultdict(lambda: {
            "max_exposure": DEFAULT_MAX_EXPOSURE,
            "max_positions": DEFAULT_MAX_POSITIONS,
            "max_order_size_pct": 0.1  # fraction of exposure per order
        })

    def set_user_limits(self, user_id: str, max_exposure: Optional[float] = None,
                        max_positions: Optional[int] = None, max_order_pct: Optional[float] = None):
        l = self.user_limits[user_id]
        if max_exposure is not None:
            l["max_exposure"] = float(max_exposure)
        if max_positions is not None:
            l["max_positions"] = int(max_positions)
        if max_order_pct is not None:
            l["max_order_size_pct"] = float(max_order_pct)

    def assess_order(self, order: dict, current_positions: List[dict], broker: BrokerAdapterBase) -> Tuple[bool, str]:
        """
        Returns (allow: bool, reason: str)
        - checks exposure limits, order size caps, and basic sanity checks
        """
        user = order["user_id"]
        limits = self.user_limits[user]
        # compute notional
        price = order.get("price") or broker.get_market_price(order["symbol"])
        notional = abs(order["qty"]) * price
        if notional <= 0:
            return False, "invalid_order_notional"
        # max order size
        max_per_order = limits["max_exposure"] * limits["max_order_size_pct"]
        if notional > max_per_order:
            return False, f"order_too_large_per_order_limit (>{max_per_order})"
        # existing exposure estimate
        exp = 0.0
        for p in current_positions:
            exp += abs(p.get("qty", 0)) * float(p.get("avg_price", 0) or 0)
        if exp + notional > limits["max_exposure"]:
            return False, "would_exceed_max_exposure"
        # positions count
        symbols = {p["symbol"] for p in current_positions}
        if order["symbol"] not in symbols and len(symbols) >= limits["max_positions"]:
            return False, "max_positions_reached"
        return True, "ok"

# ---------------------------
# Bot base class (strategies implement this)
# ---------------------------
class TradingBotBase:
    def __init__(self, bot_id: str, user_id: str, broker: BrokerAdapterBase, bridge: "TradingBridge"):
        self.bot_id = bot_id
        self.user_id = user_id
        self.broker = broker
        self.bridge = bridge
        self.active = True
        # local memory / cache for bot
        self.memory: Dict[str, Any] = {}
        # callback hook to receive market ticks
        self.on_tick: Optional[Callable[[dict], None]] = None

    def start(self):
        """Start the bot (subclass can override to start threads or schedule tasks)"""
        logger.info(f"Bot {self.bot_id} started for user {self.user_id}")

    def stop(self):
        """Stop the bot"""
        self.active = False
        logger.info(f"Bot {self.bot_id} stopped")

    def handle_market_tick(self, tick: dict):
        """Receive market tick (price update)"""
        if self.on_tick:
            try:
                self.on_tick(tick)
            except Exception:
                logger.exception("Bot on_tick error")

    def generate_signals(self) -> List[dict]:
        """
        Should return a list of signal dicts:
          { "symbol": str, "side": "buy"|"sell", "qty": float, "price": Optional[float], "confidence": 0-1 }
        """
        raise NotImplementedError

# ---------------------------
# TradingBridge (core)
# ---------------------------
class TradingBridge:
    def __init__(self, broker: BrokerAdapterBase = None):
        self.broker = broker or MockBroker()
        self.bots_by_user: Dict[str, Dict[str, TradingBotBase]] = defaultdict(dict)  # user_id -> {bot_id: bot}
        self.risk = RiskManager()
        self.market_cache: Dict[str, dict] = {}  # symbol -> {"price": , "ts": }
        self.event_listeners: Dict[str, List[Callable]] = defaultdict(list)
        self.orders_queue = deque()
        self._stop = threading.Event()
        self._worker_thread = threading.Thread(target=self._main_loop, daemon=True)
        self._worker_thread.start()
        self._heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self._heartbeat_thread.start()

    # --- bot management ---
    def register_bot(self, bot: TradingBotBase):
        self.bots_by_user[bot.user_id][bot.bot_id] = bot
        bot.bridge = self
        bot.start()
        self._emit("bot_registered", {"user": bot.user_id, "bot": bot.bot_id})
        logger.info("Registered bot %s for user %s", bot.bot_id, bot.user_id)

    def unregister_bot(self, user_id: str, bot_id: str):
        bot = self.bots_by_user.get(user_id, {}).pop(bot_id, None)
        if bot:
            bot.stop()
            self._emit("bot_unregistered", {"user": user_id, "bot": bot_id})

    def list_bots(self, user_id: Optional[str] = None) -> List[dict]:
        if user_id:
            return [{"bot_id": b.bot_id, "active": b.active} for b in self.bots_by_user.get(user_id, {}).values()]
        out = []
        for u, bs in self.bots_by_user.items():
            for b in bs.values():
                out.append({"user": u, "bot_id": b.bot_id, "active": b.active})
        return out

    # --- market feed ---
    def update_market_price(self, symbol: str, price: float, ts: Optional[int] = None):
        ts = ts or int(time.time())
        self.market_cache[symbol] = {"price": float(price), "ts": ts}
        # notify bots
        tick = {"symbol": symbol, "price": float(price), "ts": ts}
        for user_bots in self.bots_by_user.values():
            for bot in user_bots.values():
                try:
                    bot.handle_market_tick(tick)
                except Exception:
                    logger.exception("bot handle_market_tick error")

    def get_market_price(self, symbol: str) -> float:
        v = self.market_cache.get(symbol)
        if v:
            return v["price"]
        return self.broker.get_market_price(symbol)

    # --- order lifecycle ---
    def submit_order(self, order: dict, mode: str = "live") -> dict:
        """
        mode: 'live' (send to broker) or 'paper' (simulate)
        Returns execution result dict.
        """
        logger.info("Submitting order: %s", order)
        # Look up current positions from DB (simple)
        positions = self._get_user_positions(order["user_id"])
        allow, reason = self.risk.assess_order(order, positions, self.broker)
        if not allow:
            db_insert_audit("warning", f"Order rejected by risk manager: {reason}", {"order": order})
            logger.warning("Order rejected: %s reason=%s", order["id"], reason)
            order["status"] = "rejected"
            order["meta"]["reject_reason"] = reason
            db_insert_order(order)
            return {"ok": False, "reason": reason}
        # persist new
        db_insert_order(order)
        if mode == "paper":
            # simulate a fill
            price = order.get("price") or self.get_market_price(order["symbol"])
            exec_price = round(price * (1 + (random.random() - 0.5) * 0.001), 6)
            order["executed_at"] = int(time.time())
            order["status"] = "filled"
            db_insert_order(order)
            db_upsert_position(order["symbol"], order["user_id"], order["qty"] if order["side"] == "buy" else -order["qty"], exec_price)
            db_insert_audit("info", "Paper trade executed", {"order_id": order["id"], "exec_price": exec_price})
            self._emit("order_filled", {"order": order, "exec_price": exec_price})
            return {"ok": True, "exec_price": exec_price, "paper": True}
        # live mode -> queue to worker
        self.orders_queue.append(order)
        return {"ok": True, "status": "queued"}

    def _process_order_worker(self, order: dict):
        # send to broker and capture result
        try:
            res = self.broker.execute_order(order)
            if not res.get("ok"):
                order["status"] = "failed"
                order["meta"]["broker_error"] = res.get("error")
                db_insert_order(order)
                db_insert_audit("error", "Broker execute failed", {"order": order, "error": res.get("error")})
                self._emit("order_failed", {"order": order, "error": res.get("error")})
                return
            exec_price = float(res["exec_price"])
            order["executed_at"] = int(time.time())
            order["status"] = "filled"
            db_insert_order(order)
            # update positions
            qty_signed = order["qty"] if order["side"] == "buy" else -order["qty"]
            db_upsert_position(order["symbol"], order["user_id"], qty_signed, exec_price)
            db_insert_audit("info", "Order executed", {"order_id": order["id"], "exec_price": exec_price})
            self._emit("order_filled", {"order": order, "exec_price": exec_price})
        except Exception as e:
            logger.exception("order processing error: %s", e)
            db_insert_audit("error", "Order processing exception", {"order": order, "exc": str(e)})
            self._emit("order_failed", {"order": order, "error": str(e)})

    def _get_user_positions(self, user_id: str) -> List[dict]:
        with _db_lock:
            cur = _db_conn.cursor()
            cur.execute("SELECT symbol, qty, avg_price FROM positions WHERE user_id = ?", (user_id,))
            rows = cur.fetchall()
            return [{"symbol": r[0], "qty": float(r[1]), "avg_price": float(r[2])} for r in rows]

    # --- events and listeners ---
    def on(self, event_name: str, cb: Callable[[dict], None]):
        self.event_listeners[event_name].append(cb)

    def _emit(self, event_name: str, payload: dict):
        for cb in self.event_listeners.get(event_name, []):
            try:
                cb(payload)
            except Exception:
                logger.exception("event listener error for %s", event_name)

    # --- background loops ---
    def _main_loop(self):
        logger.info("TradingBridge main loop started.")
        while not self._stop.is_set():
            try:
                if self.orders_queue:
                    order = self.orders_queue.popleft()
                    # process
                    self._process_order_worker(order)
                else:
                    time.sleep(0.1)
            except Exception:
                logger.exception("main loop exception")
                time.sleep(1)
        logger.info("TradingBridge main loop stopped.")

    def _heartbeat_loop(self):
        while not self._stop.is_set():
            try:
                # heartbeat: emit positions and orders snapshot
                try:
                    self._emit("heartbeat", {"ts": int(time.time()), "users": list(self.bots_by_user.keys())})
                except Exception:
                    pass
                time.sleep(HEARTBEAT_INTERVAL)
            except Exception:
                logger.exception("heartbeat loop exception")
                time.sleep(1)

    def shutdown(self):
        logger.info("TradingBridge shutting down...")
        self._stop.set()
        # try to flush queue
        while self.orders_queue:
            order = self.orders_queue.popleft()
            logger.info("Draining queued order: %s", order["id"])
        logger.info("Shutdown complete.")

# ---------------------------
# Example simple strategy implementation
# ---------------------------
class MeanReversionBot(TradingBotBase):
    """
    Small example bot that buys if price dipped by threshold compared to rolling mean.
    """
    def __init__(self, bot_id: str, user_id: str, broker: BrokerAdapterBase, bridge: TradingBridge,
                 symbol: str, window: int = 10, threshold: float = 0.02, size: float = 1.0):
        super().__init__(bot_id, user_id, broker, bridge)
        self.symbol = symbol
        self.window = window
        self.prices = deque(maxlen=window)
        self.threshold = threshold
        self.size = size
        # register tick handler
        self.on_tick = self._on_tick

    def _on_tick(self, tick: dict):
        if tick["symbol"] != self.symbol:
            return
        self.prices.append(tick["price"])
        if len(self.prices) < self.window: return
        avg = sum(self.prices) / len(self.prices)
        cur = tick["price"]
        # buy signal
        if (avg - cur) / avg > self.threshold:
            # place order
            order = create_order(self.user_id, self.bot_id, self.symbol, "buy", qty=self.size, price=None, meta={"strategy": "mean_reversion"})
            res = self.bridge.submit_order(order, mode="paper")
            logger.info("MeanReversionBot placed buy: %s -> %s", order["id"], res)
        # sell signal
        if (cur - avg) / avg > self.threshold:
            order = create_order(self.user_id, self.bot_id, self.symbol, "sell", qty=self.size, price=None, meta={"strategy": "mean_reversion"})
            res = self.bridge.submit_order(order, mode="paper")
            logger.info("MeanReversionBot placed sell: %s -> %s", order["id"], res)

# ---------------------------
# Utility / Admin helpers
# ---------------------------
def list_open_orders(user_id: Optional[str] = None) -> List[dict]:
    with _db_lock:
        cur = _db_conn.cursor()
        if user_id:
            cur.execute("SELECT id,user_id,bot_id,symbol,side,qty,price,status,created_at,executed_at,meta FROM orders WHERE user_id = ?", (user_id,))
        else:
            cur.execute("SELECT id,user_id,bot_id,symbol,side,qty,price,status,created_at,executed_at,meta FROM orders")
        rows = cur.fetchall()
        result = []
        for r in rows:
            result.append({
                "id": r[0], "user_id": r[1], "bot_id": r[2], "symbol": r[3],
                "side": r[4], "qty": float(r[5]), "price": float(r[6]) if r[6] else None,
                "status": r[7], "created_at": r[8], "executed_at": r[9],
                "meta": json.loads(r[10] or "{}")
            })
        return result

# ---------------------------
# Example usage (if run as script)
# ---------------------------
if __name__ == "__main__":
    bridge = TradingBridge()
    user = "user_demo"
    # set tighter risk for demo
    bridge.risk.set_user_limits(user, max_exposure=5000, max_positions=5, max_order_pct=0.2)

    # register example bots
    bot1 = MeanReversionBot("mr_1", user, bridge.broker, bridge, symbol="BTCUSD", window=6, threshold=0.015, size=0.01)
    bridge.register_bot(bot1)

    # simple feed simulation
    for i in range(60):
        price = bridge.broker.get_market_price("BTCUSD") * (1 + (random.random() - 0.5) * 0.01)
        bridge.update_market_price("BTCUSD", price)
        time.sleep(0.5)

    # list orders
    print("Orders:", list_open_orders(user))

    # shutdown
    bridge.shutdown()