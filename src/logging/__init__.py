import sys
from loguru import logger

from src.utils.ansi_colors import ANSI


logger.remove()

RECORD_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level.icon} <level>{level: <8}</level> | {file.path} | {module}:{line} | {function} | <level>{message}</level>"
ROTATION = "10 MB"
RETENTION = "7 days"
COMPRESSION = "zip"

# functions
def add(path: str, level: str):
    logger.add(
        sink=path,
        level=level.upper(),
        filter=lambda record: record["level"].name == level.upper(),
        **params,
    )

# Params
params = {
    "rotation": ROTATION,
    "retention": RETENTION,
    "compression": COMPRESSION,
    "format": RECORD_FORMAT,
    "colorize": None,
    "backtrace": True,
    "serialize": True,
    "diagnose": False,
}

# Custom levels
logger.level("REQUEST", no=15, color="<blue>", icon="📩")

# Standard output sinks
logger.add(sys.stderr, level="DEBUG", format=RECORD_FORMAT)

# File sinks
add("logs/request.json", "REQUEST")
add("logs/info.json", "INFO")
add("logs/info.json", "SUCCESS")
add("logs/error.json", "ERROR")
