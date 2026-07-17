"""
AI Score Engine v2
"""

import pandas as pd


class ScoreEngine:

    @staticmethod
    def trend_score(row):
        score = 0.0

        if row["EMA20"] > row["EMA50"]:
            score += 10

        if row["EMA50"] > row["EMA200"]:
            score += 10

        if row["TREND_STRENGTH"] > 2:
            score += 10
        elif row["TREND_STRENGTH"] > 0:
            score += 5

        return score

    @staticmethod
    def rsi_score(row):
        rsi = row["RSI"]

        if pd.isna(rsi):
            return 0

        if 50 <= rsi <= 60:
            return 15
        if 45 <= rsi < 50:
            return 12
        if 60 < rsi <= 65:
            return 10
        if 40 <= rsi < 45:
            return 6
        return 0

    @staticmethod
    def macd_score(row):
        diff = row["MACD"] - row["Signal"]

        if diff > 1:
            return 20
        if diff > 0.5:
            return 15
        if diff > 0:
            return 10
        return 0

    @staticmethod
    def momentum_score(row):
        score = 0

        for col in ("MOMENTUM_1M","MOMENTUM_3M","MOMENTUM_6M","MOMENTUM_12M"):
            v = row[col]
            if pd.isna(v):
                continue
            if v > 10:
                score += 5
            elif v > 5:
                score += 3
            elif v > 0:
                score += 2

        return min(score,20)

    @staticmethod
    def volatility_score(row):
        if pd.isna(row["ATR"]) or pd.isna(row["Close"]) or row["Close"] == 0:
            return 0

        atr = row["ATR"] / row["Close"]

        if atr < 0.02:
            return 15
        if atr < 0.03:
            return 12
        if atr < 0.05:
            return 8
        if atr < 0.07:
            return 4
        return 0

    @staticmethod
    def calculate(df):
        df = df.copy()

        scores = []

        for _, row in df.iterrows():
            score = (
                ScoreEngine.trend_score(row)
                + ScoreEngine.rsi_score(row)
                + ScoreEngine.macd_score(row)
                + ScoreEngine.momentum_score(row)
                + ScoreEngine.volatility_score(row)
            )
            scores.append(round(min(score,100),2))

        df["AI_SCORE"] = scores
        return df

    @staticmethod
    def latest_score(df):
        if df.empty:
            return None

        row = df.iloc[-1]
        return {
            "score": float(row["AI_SCORE"]),
            "trend_strength": float(row["TREND_STRENGTH"]),
            "momentum_3m": float(row["MOMENTUM_3M"]),
            "momentum_6m": float(row["MOMENTUM_6M"]),
            "momentum_12m": float(row["MOMENTUM_12M"]),
            "rsi": float(row["RSI"]),
            "macd": float(row["MACD"]),
            "signal": float(row["Signal"]),
            "atr": float(row["ATR"]),
        }

    @staticmethod
    def rating(score):
        if score >= 90:
            return "STRONG BUY"
        if score >= 75:
            return "BUY"
        if score >= 60:
            return "ACCUMULATE"
        if score >= 40:
            return "HOLD"
        if score >= 20:
            return "REDUCE"
        return "SELL"
