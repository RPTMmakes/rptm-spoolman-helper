# RPTM Spoolman Helper – Dokumentation

## Erster Start

1. App/Add-on installieren.
2. `In Seitenleiste anzeigen` aktivieren, falls Home Assistant dies nicht
   automatisch übernimmt.
3. App/Add-on starten.
4. Weboberfläche über den Sidebar-Eintrag öffnen.

Direkter Zugriff im lokalen Netz:

`http://HOME-ASSISTANT-IP:8765`

## Test-Endpunkte

- `/health`
- `/version`
- `/api/health`
- `/api/version`
- `/api/settings`

## Persistente Daten

Interne persistente Daten werden später unter `/data` gespeichert.
Nutzerzugängliche Konfigurationsdateien können unter `/config` abgelegt
werden. Dieser Pfad wird durch `addon_config` bereitgestellt.
