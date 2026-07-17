"""
AI Robo Advisor
Data Engine v0.2
"""
from database.database import Database
from core.provider_manager import ProviderManager
from core.logger import log

class DataEngine:
    def __init__(self):
        self.database=Database()
        self.database.initialize()
        self.providers=ProviderManager()

    def update_symbol(self,symbol,period="10y",interval="1d"):
        log.info(f"Download {symbol}")
        df=self.providers.download(symbol,period,interval)
        inserted=0
        for index,row in df.iterrows():
            self.database.execute(
                """INSERT OR REPLACE INTO prices
                (symbol,date,open,high,low,close,volume,provider)
                VALUES (?,?,?,?,?,?,?,?)""",
                (symbol,str(index.date()),float(row.Open),float(row.High),float(row.Low),float(row.Close),float(row.Volume),self.providers.name)
            )
            inserted+=1
        log.info(f"{symbol}: {inserted} righe salvate.")

    def update_symbols(self,symbols):
        for symbol in symbols:
            try:
                self.update_symbol(symbol)
                print(f"✓ {symbol} aggiornato")
            except Exception as exc:
                log.error(f"{symbol}: {exc}")
                print(f"✗ {symbol}: {exc}")

    def close(self):
        self.database.close()
