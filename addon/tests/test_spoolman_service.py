from app.services.spoolman_service import SpoolmanClient


def test_spoolman_api_url_is_normalized() -> None:
    client = SpoolmanClient("http://spoolman.local:7912/")

    assert (
        client._url("/health")
        == "http://spoolman.local:7912/api/v1/health"
    )
