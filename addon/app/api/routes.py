"""Public API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request, status

from app.core.config import settings
from app.services.spoolman_service import (
    SpoolmanConnectionError,
    spoolman_client,
)
from app.services.status_service import health_payload, version_payload

router = APIRouter()


@router.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    """Return application health information."""
    return health_payload()


@router.get("/version", tags=["system"])
async def version() -> dict[str, str]:
    """Return application version information."""
    return version_payload()


@router.get("/settings", tags=["system"])
async def public_settings(
    request: Request,
) -> dict[str, str | int | float | bool | None]:
    """Expose only non-sensitive runtime settings to the frontend."""
    ingress_path = str(
        getattr(request.state, "ingress_path", "")
    ).rstrip("/")

    return {
        "app_name": settings.app_name,
        "version": settings.version,
        "port": settings.port,
        "ingress": bool(ingress_path),
        "ingress_path": ingress_path or None,
        "spoolman_url": settings.spoolman_url,
        "spoolman_timeout": settings.spoolman_timeout,
    }


async def _spoolman_snapshot() -> dict[str, Any]:
    try:
        return await spoolman_client.get_snapshot()
    except SpoolmanConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc


@router.get("/spoolman/status", tags=["spoolman"])
async def spoolman_status() -> dict[str, Any]:
    """Return connection state and basic Spoolman counters."""
    return await _spoolman_snapshot()


@router.get("/spoolman/locations", tags=["spoolman"])
async def spoolman_locations() -> dict[str, Any]:
    """Return the current Spoolman location list."""
    snapshot = await _spoolman_snapshot()
    return {
        "locations": snapshot["locations"],
        "count": snapshot["location_count"],
        "checked_at": snapshot["checked_at"],
    }


@router.post("/spoolman/sync", tags=["spoolman"])
async def spoolman_sync() -> dict[str, Any]:
    """Manually reload the first Spoolman dashboard snapshot."""
    return await _spoolman_snapshot()
