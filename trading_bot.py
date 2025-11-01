"""
trading_bot.py
Advanced AI-driven trading bot that reacts to live signals,
tracks performance, and adapts trading behavior dynamically.
"""

import asyncio
import random
import statistics
from datetime import datetime

class TradingBot:
    def __init__(self, symbol: str, strategy: str, broker):
        self.symbol = symbol
        self.strategy = strategy
        self.broker = broker
        self.balance = 10000.0
        self.position = None  # ("BUY"/"SELL", price)
        self.trades = []
        self.pnl_history = []
        self.confidence_memory = []
        self.status = "IDLE"
        self.running = True

    async def react_to_signal(self, signal: str, confidence: float):
        """React to AI signal (BUY/SELL/HOLD) with confidence-weighted logic."""
        if not self.running:
            return

        self.status = f"Reacting to {signal} ({confidence*100:.1f}%)"
        print(f"⚡ {self.symbol} received signal → {signal} ({confidence:.2f})")

        # Apply adaptive sensitivity
        decision_threshold = self._calculate_threshold()

        if confidence < decision_threshold:
            print(f"🧠 Ignored weak signal for {self.symbol} ({confidence:.2f} < {decision_threshold:.2f})")
            return

        if signal == "BUY":
            await self._enter_trade("BUY")
        elif signal == "SELL":
            await self._enter_trade("SELL")
        elif signal == "HOLD":
            await self._hold_position()

        await self._evaluate_position()

    async def _enter_trade(self, direction: str):
        """Open or flip position."""
        price = self._get_market_price()
        if self.position:
            prev_dir, prev_price = self.position
            if prev_dir != direction:
                await self._close_trade(prev_price)
        self.position = (direction, price)
        self.trades.append((datetime.utcnow(), direction, price))
        print(f"💰 Opened {direction} at {price:.2f} for {self.symbol}")

    async def _close_trade(self, entry_price):
        """Close existing trade and record profit/loss."""
        price = self._get_market_price()
        pnl = price - entry_price if self.position[0] == "BUY" else entry_price - price
        self.balance += pnl
        self.pnl_history.append(pnl)
        self.position = None
        print(f"📉 Closed trade with PnL {pnl:.2f}, Balance: {self.balance:.2f}")

    async def _hold_position(self):
        """Hold current position without new entries."""
        self.status = "HOLDING"
        print(f"⏸️ Holding position for {self.symbol}")

    async def _evaluate_position(self):
        """Evaluate open position for stop or take-profit triggers."""
        if not self.position:
            return

        direction, entry = self.position
        price = self._get_market_price()
        change = ((price - entry) / entry) * 100

        # Smart dynamic stop loss & take profit
        if direction == "BUY" and change <= -0.5:
            print(f"🔻 Auto-stopping {self.symbol} long position")
            await self._close_trade(entry)
        elif direction == "SELL" and change >= 0.5:
            print(f"🔺 Auto-stopping {self.symbol} short position")
            await self._close_trade(entry)
        elif abs(change) >= 1.5:
            print(f"🏁 Take-profit hit on {self.symbol}")
            await self._close_trade(entry)

    async def stop(self):
        """Stop bot execution and close positions."""
        self.running = False
        if self.position:
            await self._close_trade(self.position[1])
        print(f"🛑 Bot stopped for {self.symbol}")

    def _get_market_price(self):
        """Mock market price generator (can link to live feed)."""
        return random.uniform(90, 110)

    def _calculate_threshold(self) -> float:
        """Adaptive confidence threshold (based on history)."""
        if not self.confidence_memory:
            return 0.55
        avg_conf = statistics.mean(self.confidence_memory[-10:])
        return min(0.9, max(0.5, avg_conf))

    def get_profit_loss(self) -> float:
        """Return current total PnL."""
        return sum(self.pnl_history)

    def performance_summary(self) -> dict:
        """Summarize performance stats for dashboards."""
        avg_pnl = statistics.mean(self.pnl_history) if self.pnl_history else 0
        success_rate = sum(1 for p in self.pnl_history if p > 0) / max(len(self.pnl_history), 1)
        return {
            "symbol": self.symbol,
            "strategy": self.strategy,
            "trades": len(self.trades),
            "avg_pnl": round(avg_pnl, 2),
            "success_rate": round(success_rate * 100, 2),
            "balance": round(self.balance, 2),
        }

# Example use
# async def main():
#     from broker_adapter import BrokerAdapter
#     broker = BrokerAdapter("demo-key")
#     bot = TradingBot("BTCUSD", "adaptive", broker)
#     await bot.react_to_signal("BUY", 0.8)
#     await asyncio.sleep(3)
#     await bot.react_to_signal("SELL", 0.9)
#     print(bot.performance_summary())
#
# asyncio.run(main())