"""Shared logger"""

import os
import sys

from loguru import logger as log

log.remove()

log_level = os.environ.get("LOG_LEVEL", "DEBUG").upper()

# 1️⃣ Local console with colors (for PyCharm / terminal)
if os.environ.get("RUNNING_LOCALLY", "1") == "1":
    log.add(
        sys.stderr,
        level=log_level,
        colorize=True,  # colored output
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>",
    )

# 2️⃣ Claude Desktop (or any environment that needs JSON-safe stdout)
else:
    log.add(
        sys.stdout,
        level=log_level,
        colorize=False,  # no colors → safe for Claude
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name}:{function}:{line} - {message}",
    )
