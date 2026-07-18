"""Status payloads used by API and watchdog endpoints."""

from __future__ import annotations

from datetime import UTC, datetime

from app.core.config import settings


def health_payload() -> dict[str, str]:
    """Build a serializable health response."""
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.version,
        "time_utc": datetime.now(UTC).isoformat(),
    }


def version_payload() -> dict[str, str]:
    """Build a serializable version response."""
    return {
        "name": settings.app_name,
        "version": settings.version,
    }
