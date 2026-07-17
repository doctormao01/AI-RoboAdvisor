"""
AI Robo Advisor
Data Engine v0.4
"""

import pandas as pd

from database.database import Database
from core.provider_manager import ProviderManager
from core.indicators import Indicators
from core.score_engine import ScoreEngine
from core.logger import log


class DataEngine:

    def __init__(self):
        self.database = Database()
        self.database.initialize()
        self.providers = ProviderManager()

    @staticmethod
    def _value(value):
        if pd.isna(value):
            return None
        return float(value)

    def update_symbol(self, symbol, period="10y", interval="1d"):
        log.info(f"Download {symbol}")

        df = self.providers.download(symbol, period, interval)
        indicators = Indicators.calculate(df)
        indicators = ScoreEngine.calculate(indicators)

        inserted = 0
        latest_score = None

        for index, row in indicators.iterrows():
            date = str(index.date())

            self.database.execute(
                """
                INSERT OR REPLACE INTO prices
                (
                    symbol,
                    date,
                    open,
                    high,
                    low,
                    close,
                    volume,
                    provider
                )
                VALUES
                (
                    ?,?,?,?,?,?,?,?
                )
                """,
                (
                    symbol,
                    date,
                    self._value(row["Open"]),
                    self._value(row["High"]),
                    self._value(row["Low"]),
                    self._value(row["Close"]),
                    self._value(row["Volume"]),
                    self.providers.name,
                ),
            )

            self.database.save_indicator(
                symbol=symbol,
                date=date,
                ema20=self._value(row["EMA20"]),
                ema50=self._value(row["EMA50"]),
                ema200=self._value(row["EMA200"]),
                rsi=self._value(row["RSI"]),
                macd=self._value(row["MACD"]),
                signal=self._value(row["Signal"]),
                histogram=self._value(row["Histogram"]),
                atr=self._value(row["ATR"]),
            )

            score = self._value(row["AI_SCORE"])

            self.database.save_score(
                symbol=symbol,
                date=date,
                score=score,
            )

            latest_score = score
            inserted += 1

        log.info(f"{symbol}: {inserted} righe salvate.")

        if latest_score is not None:
            print()
            print("-" * 40)
            print(f"ETF: {symbol}")
            print(f"AI Score : {latest_score:.2f}")
            print(f"Rating   : {ScoreEngine.rating(latest_score)}")
            print("-" * 40)

    def update_symbols(self, symbols):
        total = len(symbols)

        print()

        for position, symbol in enumerate(symbols, start=1):
            print(f"[{position}/{total}] Aggiornamento {symbol}")

            try:
                self.update_symbol(symbol)
                print(f"✓ {symbol} aggiornato")
            except Exception as exc:
                log.error(f"{symbol}: {exc}")
                print(f"✗ {symbol}: {exc}")

            print()

    def close(self):
        self.database.close()
