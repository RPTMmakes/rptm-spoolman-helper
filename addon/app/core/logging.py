"""Logging configuration for the application."""

from __future__ import annotations

import logging

from app.core.config import settings

_LEVEL_MAP = {
    "trace": logging.DEBUG,
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "notice": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "fatal": logging.CRITICAL,
}


def configure_logging() -> None:
    """Configure predictable log output for Home Assistant logs."""
    logging.basicConfig(
        level=_LEVEL_MAP.get(settings.log_level, logging.INFO),
        format="[RPTM] %(asctime)s %(levelname)s %(name)s: %(message)s",
        force=True,
    )
