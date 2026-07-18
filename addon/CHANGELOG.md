# Changelog

## 1.0.0-alpha.4

- Added configurable Spoolman URL and timeout
- Added Spoolman health, version and inventory checks
- Added API endpoints for status, locations and manual sync
- Added first live Spoolman dashboard card

## 1.0.0-alpha.3

- Normalized Home Assistant Ingress root requests from `//` to `/`
- Added regression tests for repeated leading slashes

## 1.0.0-alpha.2

- Home Assistant Ingress path handling fixed
- Static assets and API calls now work below the Ingress prefix
- Direct access through port 8765 remains supported

## 1.0.0-alpha.1

- Home Assistant Ingress
- Sidebar panel
- Direct port 8765
- FastAPI application
- Initial dashboard shell
- Health, version and settings API
