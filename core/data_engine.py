"""
AI Robo Advisor
Data Engine v0.1
"""

from database.database import Database
from providers.yahoo_provider import YahooProvider


class DataEngine:

    def __init__(self):

        self.database = Database()

        self.database.initialize()

        self.provider = YahooProvider()

    def update_symbol(

        self,

        symbol,

        period="10y",

        interval="1d"

    ):

        print(f"\nDownload {symbol}")

        dataframe = self.provider.download(

            symbol,

            period,

            interval

        )

        rows = 0

        for index, row in dataframe.iterrows():

            self.database.execute(

                """

                INSERT OR REPLACE INTO prices(

                    symbol,

                    date,

                    open,

                    high,

                    low,

                    close,

                    volume,

                    provider

                )

                VALUES(

                    ?,?,?,?,?,?,?,?

                )

                """,

                (

                    symbol,

                    str(index.date()),

                    float(row["Open"]),

                    float(row["High"]),

                    float(row["Low"]),

                    float(row["Close"]),

                    float(row["Volume"]),

                    self.provider.name

                )

            )

            rows += 1

        print(f"{rows} righe salvate.")

    def close(self):

        self.database.close()