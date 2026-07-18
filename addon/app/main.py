"""FastAPI entry point for the RPTM Spoolman Helper."""

from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes import router
from app.core.config import settings
from app.core.logging import configure_logging
from app.services.status_service import health_payload, version_payload

configure_logging()
LOGGER = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    docs_url="/api/docs",
    redoc_url=None,
    openapi_url="/api/openapi.json",
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.include_router(router, prefix="/api")


@app.on_event("startup")
async def on_startup() -> None:
    """Log startup information once the ASGI app is ready."""
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    LOGGER.info(
        "RPTM Spoolman Helper %s gestartet; Datenpfad: %s",
        settings.version,
        settings.data_dir,
    )


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request) -> HTMLResponse:
    """Render the first dashboard shell."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": settings.app_name,
            "version": settings.version,
        },
    )


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    """Health endpoint used by the Home Assistant watchdog."""
    return health_payload()


@app.get("/version", tags=["system"])
async def version() -> dict[str, str]:
    """Convenient root-level version endpoint."""
    return version_payload()
