"""
Base Provider
AI Robo Advisor
"""

from abc import ABC, abstractmethod
import pandas as pd


class BaseProvider(ABC):

    @abstractmethod
    def download(
        self,
        symbol: str,
        period: str = "10y",
        interval: str = "1d"
    ) -> pd.DataFrame:
        """
        Scarica i dati storici di uno strumento.
        Deve restituire un DataFrame Pandas.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass