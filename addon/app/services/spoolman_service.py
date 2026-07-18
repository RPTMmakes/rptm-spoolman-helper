"""Read-only access to the Spoolman REST API."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from typing import Any

import httpx

from app.core.config import settings


class SpoolmanConnectionError(RuntimeError):
    """Raised when Spoolman cannot be reached or returns invalid data."""


class SpoolmanClient:
    """Small asynchronous client for the Spoolman API."""

    def __init__(
        self,
        base_url: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self.base_url = (base_url or settings.spoolman_url).rstrip("/")
        self.timeout = timeout or settings.spoolman_timeout

    def _url(self, path: str) -> str:
        return f"{self.base_url}/api/v1/{path.lstrip('/')}"

    async def _get(self, client: httpx.AsyncClient, path: str) -> Any:
        try:
            response = await client.get(self._url(path))
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException as exc:
            raise SpoolmanConnectionError(
                f"Spoolman antwortet nicht innerhalb von "
                f"{self.timeout:g} Sekunden."
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise SpoolmanConnectionError(
                f"Spoolman meldet HTTP {exc.response.status_code} "
                f"für {path}."
            ) from exc
        except httpx.RequestError as exc:
            raise SpoolmanConnectionError(
                f"Spoolman ist unter {self.base_url} nicht erreichbar."
            ) from exc
        except ValueError as exc:
            raise SpoolmanConnectionError(
                "Spoolman hat keine gültige JSON-Antwort geliefert."
            ) from exc

    async def get_snapshot(self) -> dict[str, Any]:
        """Load the basic data needed by the first dashboard."""
        async with httpx.AsyncClient(
            timeout=self.timeout,
            follow_redirects=True,
        ) as client:
            (
                health,
                info,
                locations,
                spools,
                filaments,
                vendors,
            ) = await asyncio.gather(
                self._get(client, "health"),
                self._get(client, "info"),
                self._get(client, "location"),
                self._get(client, "spool"),
                self._get(client, "filament"),
                self._get(client, "vendor"),
            )

        if not isinstance(locations, list):
            raise SpoolmanConnectionError(
                "Spoolman hat für Lagerorte ein unerwartetes Format geliefert."
            )

        return {
            "connected": True,
            "url": self.base_url,
            "health": health.get("status", "unknown")
            if isinstance(health, dict)
            else "unknown",
            "version": info.get("version")
            if isinstance(info, dict)
            else None,
            "spool_count": len(spools) if isinstance(spools, list) else 0,
            "filament_count": (
                len(filaments) if isinstance(filaments, list) else 0
            ),
            "vendor_count": (
                len(vendors) if isinstance(vendors, list) else 0
            ),
            "location_count": len(locations),
            "locations": sorted(
                str(location)
                for location in locations
                if location
            ),
            "checked_at": datetime.now(UTC).isoformat(),
        }


spoolman_client = SpoolmanClient()
