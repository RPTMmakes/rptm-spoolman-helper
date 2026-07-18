# Changelog

## 1.0.0-alpha.4

- Connected the helper to the Spoolman REST API
- Added configurable Spoolman URL and timeout
- Added inventory counters and location retrieval
- Added the first manual Spoolman sync action

## 1.0.0-alpha.3

- Normalized Home Assistant Ingress root requests from `//` to `/`
- Added regression coverage for repeated leading slashes

## 1.0.0-alpha.2

- Fixed Home Assistant Ingress prefix handling
- Made frontend asset and API URLs Ingress-safe
- Retained direct access through TCP port 8765

## 1.0.0-alpha.1

- Initial Home Assistant app/add-on scaffold
- Sidebar entry through Ingress
- Direct access through TCP port 8765
- FastAPI backend with modular structure
- Health, version and public-settings endpoints
- Initial RPTM dashboard shell
