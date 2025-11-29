"""Centralised logging configuration using Loguru and Rich."""

from loguru import logger
from rich.console import Console
from rich.traceback import install
from .config import settings
import sys

console = Console()

# Install Rich traceback handler for better error formatting
install(show_locals=True)

def configure_logger() -> None:
    """Configure the global Loguru logger.

    This sets up a file sink and ensures logs are written with rotation.
    """
    # Remove default handlers to avoid duplicate logs
    logger.remove()

    # Output logs to stderr for console
    logger.add(sys.stderr, level=settings.log_level)

    # Output logs to file with rotation
    logger.add(
        "logs/app.log",
        rotation="5 MB",
        retention="7 days",
        compression="zip",
        level=settings.log_level,
    )


# Configure logger at import time
configure_logger()


def get_logger():
    """Return the configured Loguru logger instance."""
    return logger