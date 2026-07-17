"""
AI Robo Advisor
Release 0.4
"""

from core.data_engine import DataEngine
from core.ranking_engine import RankingEngine
from core.portfolio_engine import PortfolioEngine

try:
    from data.etf_list import ETF_LIST
except ImportError:
    ETF_LIST = ["SPY"]


# Capitale iniziale
INITIAL_CAPITAL = 4000.0


def banner():

    print("=" * 60)
    print("AI Robo Advisor - Release 0.4")
    print("=" * 60)
    print()


def main():

    banner()

    print(f"ETF da aggiornare: {len(ETF_LIST)}")
    print()

    # ----------------------------
    # Aggiornamento dati
    # ----------------------------
    engine = DataEngine()

    try:
        engine.update_symbols(ETF_LIST)

    finally:
        engine.close()

    print()
    print("=" * 60)
    print("Aggiornamento completato")
    print("=" * 60)
    print()

    # ----------------------------
    # Ranking
    # ----------------------------
    ranking = RankingEngine()

    try:
        ranking.print(10)

    finally:
        ranking.close()

    print()

    # ----------------------------
    # Portfolio
    # ----------------------------
    portfolio = PortfolioEngine(INITIAL_CAPITAL)

    try:
        portfolio.run()

    finally:
        portfolio.close()

    print()
    print("=" * 60)
    print("ROBO ADVISOR COMPLETATO")
    print("=" * 60)


if __name__ == "__main__":
    main()