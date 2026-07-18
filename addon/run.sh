#!/usr/bin/with-contenv bashio
set -euo pipefail

LOG_LEVEL="$(bashio::config 'log_level')"
SPOOLMAN_URL="$(bashio::config 'spoolman_url')"
SPOOLMAN_TIMEOUT="$(bashio::config 'spoolman_timeout')"

export RPTM_LOG_LEVEL="${LOG_LEVEL}"
export RPTM_SPOOLMAN_URL="${SPOOLMAN_URL}"
export RPTM_SPOOLMAN_TIMEOUT="${SPOOLMAN_TIMEOUT}"

bashio::log.info "Starte RPTM Spoolman Helper v1.0.0-alpha.5"
bashio::log.info "Webserver lauscht auf Port 8765"
bashio::log.info "Spoolman wird über ${SPOOLMAN_URL} angesprochen"

exec /opt/rptm-venv/bin/uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8765 \
  --proxy-headers \
  --forwarded-allow-ips="*"
