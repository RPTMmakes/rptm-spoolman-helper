#!/usr/bin/with-contenv bashio
set -euo pipefail

LOG_LEVEL="$(bashio::config 'log_level')"

export RPTM_LOG_LEVEL="${LOG_LEVEL}"

bashio::log.info "Starte RPTM Spoolman Helper v1.0.0-alpha.1"
bashio::log.info "Webserver lauscht auf Port 8765"

exec /opt/rptm-venv/bin/uvicorn app.main:app       --host 0.0.0.0       --port 8765       --proxy-headers       --forwarded-allow-ips="*"
