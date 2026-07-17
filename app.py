"""
AI Robo Advisor
Release 0.1
"""

from core.data_engine import DataEngine

try:
    from data.etf_list import ETF_LIST
except ImportError:
    ETF_LIST = ["SPY"]


def banner():
    print("=" * 60)
    print("AI Robo Advisor - v0.1.0")
    print("=" * 60)
    print()


def main():
    banner()

    print(f"ETF da aggiornare: {len(ETF_LIST)}")
    print()

    engine = DataEngine()

    try:
        engine.update_symbols(ETF_LIST)
    finally:
        engine.close()

    print()
    print("=" * 60)
    print("Aggiornamento completato.")
    print("=" * 60)


if __name__ == "__main__":
    main()
