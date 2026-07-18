# Architektur

## Grundsatz

Spoolman bleibt die führende Datenquelle für Hersteller, Filamente und
Spulen. Der RPTM Spoolman Helper ergänzt Bedienung, Presets, QR-Workflows,
AMS-Darstellung und Statistiken.

## Schichten

- `api`: HTTP-Endpunkte
- `core`: Konfiguration und Logging
- `services`: Geschäftslogik und externe Systeme
- `templates`: HTML
- `static`: CSS, JavaScript und Bilder

## Persistenz

- `/data`: interne persistente App-Daten und Cache
- `/config`: nutzerzugängliche Konfiguration über `addon_config`
