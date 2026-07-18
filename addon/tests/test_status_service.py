from app.services.status_service import health_payload, version_payload


def test_health_payload_is_ok() -> None:
    payload = health_payload()

    assert payload["status"] == "ok"
    assert payload["service"] == "RPTM Spoolman Helper"
    assert payload["version"] == "1.0.0-alpha.3"


def test_version_payload_contains_version() -> None:
    payload = version_payload()

    assert payload == {
        "name": "RPTM Spoolman Helper",
        "version": "1.0.0-alpha.3",
    }
