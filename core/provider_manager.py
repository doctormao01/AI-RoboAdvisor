"""
Provider Manager
"""

from providers.yahoo_provider import YahooProvider


class ProviderManager:

    def __init__(self):

        self.provider = YahooProvider()

    def download(

        self,

        symbol,

        period="10y",

        interval="1d"

    ):

        return self.provider.download(

            symbol,

            period,

            interval

        )

    @property

    def name(self):

        return self.provider.name