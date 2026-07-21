from core.data_engine import DataEngine
from services.status_service import StatusService

# Importa qui la lista ETF che usi normalmente.
# Se l'hai già definita in config.py o altrove, sostituisci questa lista.
ETF_LIST = [
    "SPY",
    "QQQ",
    "VTI",
    "SCHD",
    "VXUS"
]


def update_all():

    engine = DataEngine()

    try:
        engine.update_symbols(ETF_LIST)

        StatusService.update_download(
            provider=engine.providers.name
        )

        StatusService.set_ai("ATTIVO")

    finally:
        engine.close()