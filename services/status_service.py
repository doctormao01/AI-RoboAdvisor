import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
STATUS_FILE = BASE_DIR / "config" / "status.json"


DEFAULT_STATUS = {
    "last_update": "Mai",
    "provider": "Yahoo Finance",
    "status": "OFFLINE",
    "last_rebalance": "Mai",
    "market": "Sconosciuto",
    "ai_engine": "OFF"
}


class StatusService:

    @staticmethod
    def load():

        if not STATUS_FILE.exists():
            StatusService.save(DEFAULT_STATUS)
            return DEFAULT_STATUS.copy()

        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def save(data):

        with open(STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def update_download(provider="Yahoo Finance"):

        status = StatusService.load()

        status["last_update"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        status["provider"] = provider
        status["status"] = "ONLINE"

        StatusService.save(status)

    @staticmethod
    def update_rebalance():

        status = StatusService.load()

        status["last_rebalance"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        StatusService.save(status)

    @staticmethod
    def set_market(value):

        status = StatusService.load()

        status["market"] = value

        StatusService.save(status)

    @staticmethod
    def set_ai(value):

        status = StatusService.load()

        status["ai_engine"] = value

        StatusService.save(status)