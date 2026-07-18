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
    version: str = "1.0.0-alpha.3"
    port: int = int(os.getenv("RPTM_PORT", "8765"))
    log_level: str = os.getenv("RPTM_LOG_LEVEL", "info").lower()
    data_dir: Path = Path(os.getenv("RPTM_DATA_DIR", "/data"))


settings = Settings()
