FROM ghcr.io/home-assistant/base:latest

ARG BUILD_VERSION=1.0.0-alpha.3
ARG BUILD_ARCH=amd64

LABEL \
  io.hass.name="RPTM Spoolman Helper" \
  io.hass.description="Spoolman helper, QR workflows and AMS dashboard" \
  io.hass.type="app" \
  io.hass.version="${BUILD_VERSION}" \
  io.hass.arch="${BUILD_ARCH}"

ENV \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  RPTM_PORT=8765 \
  RPTM_DATA_DIR=/data

RUN apk add --no-cache python3 py3-pip \
  && python3 -m venv /opt/rptm-venv

COPY requirements.txt /tmp/requirements.txt

RUN /opt/rptm-venv/bin/pip install --no-cache-dir --upgrade pip \
  && /opt/rptm-venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt \
  && rm -f /tmp/requirements.txt

WORKDIR /opt/rptm
COPY app ./app
COPY run.sh /run.sh

RUN chmod a+x /run.sh

EXPOSE 8765

CMD ["/run.sh"]
