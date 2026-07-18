"""Public API routes."""

from __future__ import annotations

from fastapi import APIRouter, Request

from app.core.config import settings
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
) -> dict[str, str | int | bool | None]:
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
    }
