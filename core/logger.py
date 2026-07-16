"""
Logger AI Robo Advisor
"""

from pathlib import Path
from loguru import logger

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.remove()

logger.add(
    LOG_DIR / "roboadvisor.log",
    rotation="5 MB",
    retention="30 days",
    level="INFO",
    enqueue=True,
)

logger.add(
    lambda msg: print(msg, end=""),
    level="INFO",
)

log = logger