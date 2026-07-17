import pandas as pd


class Indicators:

    @staticmethod
    def ema(series, period):
        return series.ewm(span=period, adjust=False).mean()

    @staticmethod
    def rsi(series, period=14):
        delta = series.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()

        rs = avg_gain / avg_loss

        return 100 - (100 / (1 + rs))

    @staticmethod
    def macd(series):

        ema12 = Indicators.ema(series, 12)
        ema26 = Indicators.ema(series, 26)

        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal

        return macd, signal, histogram

    @staticmethod
    def atr(df, period=14):

        high = df["High"]
        low = df["Low"]
        close = df["Close"]

        tr1 = high - low
        tr2 = (high - close.shift()).abs()
        tr3 = (low - close.shift()).abs()

        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        return tr.rolling(period).mean()

    @staticmethod
    def momentum(series, periods):
        return ((series / series.shift(periods)) - 1) * 100

    @staticmethod
    def calculate(df):

        df = df.copy()

        # =====================
        # Trend
        # =====================

        df["EMA20"] = Indicators.ema(df["Close"], 20)
        df["EMA50"] = Indicators.ema(df["Close"], 50)
        df["EMA200"] = Indicators.ema(df["Close"], 200)

        # =====================
        # RSI
        # =====================

        df["RSI"] = Indicators.rsi(df["Close"])

        # =====================
        # MACD
        # =====================

        macd, signal, histogram = Indicators.macd(df["Close"])

        df["MACD"] = macd
        df["Signal"] = signal
        df["Histogram"] = histogram

        # =====================
        # ATR
        # =====================

        df["ATR"] = Indicators.atr(df)

        # =====================
        # Momentum
        # =====================

        df["MOMENTUM_1M"] = Indicators.momentum(df["Close"], 21)
        df["MOMENTUM_3M"] = Indicators.momentum(df["Close"], 63)
        df["MOMENTUM_6M"] = Indicators.momentum(df["Close"], 126)
        df["MOMENTUM_12M"] = Indicators.momentum(df["Close"], 252)

        # =====================
        # Trend Strength
        # =====================

        df["TREND_STRENGTH"] = (
            (
                (df["EMA20"] - df["EMA200"])
                / df["EMA200"]
            ) * 100
        ).fillna(0)

        return df