"""Central application configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings shared by all application modules."""

    app_name: str = "RPTM Spoolman Helper"
    slug: str = "rptm_spoolman_helper"
    version: str = "1.0.0-alpha.4"
    port: int = int(os.getenv("RPTM_PORT", "8765"))
    log_level: str = os.getenv("RPTM_LOG_LEVEL", "info").lower()
    data_dir: Path = Path(os.getenv("RPTM_DATA_DIR", "/data"))
    spoolman_url: str = os.getenv(
        "RPTM_SPOOLMAN_URL",
        "http://192.168.178.73:7912",
    ).rstrip("/")
    spoolman_timeout: float = float(
        os.getenv("RPTM_SPOOLMAN_TIMEOUT", "5")
    )


settings = Settings()
