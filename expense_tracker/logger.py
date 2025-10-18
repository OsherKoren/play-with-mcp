"""Shared logger"""

import os
import sys

from loguru import logger as log

log.remove()  # Remove default logger

log_level = os.environ.get("LOG_LEVEL", "DEBUG").upper()

log.add(
    sys.stdout,
    level=log_level,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>",
)
