from pathlib import Path

APP_NAME = "AI Robo Advisor"
VERSION = "0.1.0"

ROOT = Path(__file__).resolve().parent

DATABASE_DIR = ROOT / "database"
CACHE_DIR = ROOT / "cache"
LOG_DIR = ROOT / "logs"
REPORT_DIR = ROOT / "reports"
DATA_DIR = ROOT / "data"

# Creazione automatica delle cartelle
for directory in (
    DATABASE_DIR,
    CACHE_DIR,
    LOG_DIR,
    REPORT_DIR,
    DATA_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)

DATABASE_FILE = DATABASE_DIR / "market.db"

PRIMARY_PROVIDER = "Yahoo"

DEFAULT_PERIOD = "10y"
DEFAULT_INTERVAL = "1d"

UPDATE_HOUR = 22
MAX_RETRY = 3