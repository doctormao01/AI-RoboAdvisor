"""
Database Models
AI Robo Advisor
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Price:

    symbol: str

    date: datetime

    open: float

    high: float

    low: float

    close: float

    volume: float

    provider: str = "Yahoo"


@dataclass
class PortfolioPosition:

    symbol: str

    quantity: float

    average_price: float

    current_price: float = 0.0

    def market_value(self):

        return self.quantity * self.current_price

    def profit_loss(self):

        return (

            self.current_price -

            self.average_price

        ) * self.quantity