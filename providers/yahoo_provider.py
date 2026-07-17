"""
Yahoo Finance Provider
"""

import pandas as pd
import yfinance as yf

from providers.base_provider import BaseProvider


class YahooProvider(BaseProvider):

    @property
    def name(self):
        return "Yahoo Finance"

    def download(
        self,
        symbol,
        period="10y",
        interval="1d"
    ):

        df = yf.download(
            symbol,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=True,
        )

        if df.empty:
            raise RuntimeError(f"Nessun dato trovato per {symbol}")

        # Normalizza eventuali colonne MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        return df