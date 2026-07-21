import json
import threading
from pathlib import Path

from flask import Flask, render_template, request, jsonify

from core.ranking_engine import RankingEngine
from core.portfolio_engine import PortfolioEngine
from core.update_service import update_all
from services.status_service import StatusService

app = Flask(__name__)

# --------------------------------------------------------
# Configurazione
# --------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_DIR = BASE_DIR / "config"
SETTINGS_FILE = CONFIG_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "capital": 4000,
    "currency": "EUR",
    "broker": "paper",
    "risk_level": "medium",
    "rebalance": "monthly"
}


def load_settings():

    CONFIG_DIR.mkdir(exist_ok=True)

    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for key, value in DEFAULT_SETTINGS.items():
        data.setdefault(key, value)

    return data


def save_settings(data):

    CONFIG_DIR.mkdir(exist_ok=True)

    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


@app.route("/")
def index():

    settings = load_settings()
    status = StatusService.load()

    ranking_engine = RankingEngine()
    portfolio_engine = PortfolioEngine(settings["capital"])

    try:
        ranking = ranking_engine.top(10)
        portfolio = portfolio_engine.build()

    finally:
        ranking_engine.close()
        portfolio_engine.close()

    return render_template(
        "index.html",
        ranking=ranking,
        portfolio=portfolio,
        settings=settings,
        status=status
    )


@app.route("/save_settings", methods=["POST"])
def save_settings_route():

    settings = load_settings()

    data = request.get_json()

    if "capital" in data:
        settings["capital"] = float(data["capital"])

    save_settings(settings)

    return jsonify({
        "success": True,
        "capital": settings["capital"]
    })


@app.route("/update_data", methods=["POST"])
def update_data():

    thread = threading.Thread(
        target=update_all,
        daemon=True
    )

    thread.start()

    return jsonify({
        "success": True,
        "message": "Aggiornamento avviato."
    })


@app.errorhandler(Exception)
def handle_exception(e):

    return jsonify({
        "error": str(e)
    }), 500


if __name__ == "__main__":

    print()
    print("=" * 70)
    print("AI Robo Advisor Dashboard")
    print("=" * 70)
    print("Apri il browser su:")
    print()
    print("http://127.0.0.1:5050")
    print("oppure")
    print("http://localhost:5050")
    print("=" * 70)
    print()

    app.run(
        host="127.0.0.1",
        port=5050,
        debug=True,
        use_reloader=False
    )