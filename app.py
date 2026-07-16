"""
AI Robo Advisor
Versione 0.1.0
"""

from config import (
    APP_NAME,
    VERSION,
    DATABASE_DIR,
    CACHE_DIR,
    LOG_DIR,
    REPORT_DIR,
    DATA_DIR,
)


def banner():
    print("=" * 60)
    print(f"{APP_NAME} - v{VERSION}")
    print("=" * 60)


def check_directories():
    print("\nControllo cartelle:\n")

    folders = [
        DATABASE_DIR,
        CACHE_DIR,
        LOG_DIR,
        REPORT_DIR,
        DATA_DIR,
    ]

    for folder in folders:
        status = "OK" if folder.exists() else "ERRORE"
        print(f"[{status}] {folder.name}")


def main():
    banner()
    check_directories()

    print("\nSistema inizializzato correttamente.")
    print("Pronto per il Data Engine.")


if __name__ == "__main__":
    main()