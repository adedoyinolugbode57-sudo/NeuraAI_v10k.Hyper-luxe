# ai_signal_generator.py
import asyncio
import random
import numpy as np
from datetime import datetime
from collections import deque

class AISignalGenerator:
    """
    AI-powered trading signal generator.
    Blends moving averages, volatility, and simulated sentiment data
    to produce buy/sell/hold signals in real time.
    """

    def __init__(self, symbol: str, window_size: int = 30):
        self.symbol = symbol
        self.prices = deque(maxlen=window_size)
        self.sentiment = deque(maxlen=window_size)
        self.volatility = deque(maxlen=window_size)
        self.trend_strength = 0.0
        self.last_signal = "hold"
        self.confidence = 0.0

    async def fetch_market_data(self):
        """
        Mock function for live market data.
        In production, plug into Binance, AlphaVantage, or Polygon.io APIs.
        """
        price = random.uniform(90, 110)
        sentiment_value = random.uniform(-1, 1)
        volatility_index = random.uniform(0, 5)
        return {
            "symbol": self.symbol,
            "price": price,
            "sentiment": sentiment_value,
            "volatility": volatility_index,
            "timestamp": datetime.utcnow().isoformat()
        }

    def calculate_trend(self):
        """
        Compute simple trend direction using moving averages.
        """
        if len(self.prices) < 5:
            return 0.0

        short_ma = np.mean(list(self.prices)[-5:])
        long_ma = np.mean(self.prices)
        self.trend_strength = (short_ma - long_ma) / (long_ma + 1e-6)
        return self.trend_strength

    def predict_signal(self):
        """
        Combine trend, sentiment, and volatility to choose action.
        """
        trend = self.calculate_trend()
        sentiment = np.mean(self.sentiment) if self.sentiment else 0.0
        vol = np.mean(self.volatility) if self.volatility else 0.0

        # Decision weight
        score = (trend * 0.6) + (sentiment * 0.3) - (vol * 0.1)
        self.confidence = min(1.0, abs(score) * 2.5)

        if score > 0.02:
            signal = "buy"
        elif score < -0.02:
            signal = "sell"
        else:
            signal = "hold"

        self.last_signal = signal
        return signal, self.confidence

    async def run_stream(self, callback=None):
        """
        Continuously generates signals every few seconds.
        Pass each signal to a callback (e.g., your bot manager).
        """
        print(f"🚀 AI Signal Generator started for {self.symbol}")
        while True:
            data = await self.fetch_market_data()
            self.prices.append(data["price"])
            self.sentiment.append(data["sentiment"])
            self.volatility.append(data["volatility"])

            signal, conf = self.predict_signal()
            timestamp = datetime.utcnow().strftime("%H:%M:%S")
            print(f"[{timestamp}] {self.symbol}: {signal.upper()} (conf={conf:.2f})")

            if callback:
                await callback(self.symbol, signal, conf)

            await asyncio.sleep(random.uniform(2, 5))

# Example of integration
# async def send_to_bot(symbol, signal, confidence):
#     print(f"Sending signal {signal} to {symbol} bot (confidence {confidence:.2f})")
#
# async def main():
#     ai_gen = AISignalGenerator("BTCUSD")
#     await ai_gen.run_stream(callback=send_to_bot)
#
# asyncio.run(main())