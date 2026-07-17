"""
Yahoo Finance Provider
"""

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
            raise RuntimeError(
                f"Nessun dato trovato per {symbol}"
            )

        return df
