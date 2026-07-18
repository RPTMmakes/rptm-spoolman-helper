import asyncio

from app.core.ingress import HomeAssistantIngressMiddleware


def run_middleware(path: str) -> dict:
    captured_scope: dict = {}

    async def downstream(scope, receive, send) -> None:
        captured_scope.update(scope)

    async def receive():
        return {"type": "http.request"}

    async def send(message) -> None:
        return None

    middleware = HomeAssistantIngressMiddleware(
        downstream,
        slug="rptm_spoolman_helper",
    )

    scope = {
        "type": "http",
        "path": path,
        "raw_path": path.encode("utf-8"),
        "headers": [],
    }

    asyncio.run(middleware(scope, receive, send))
    return captured_scope


def test_double_slash_is_normalized_to_root() -> None:
    scope = run_middleware("//")

    assert scope["path"] == "/"
    assert scope["raw_path"] == b"/"


def test_repeated_slashes_before_api_are_normalized() -> None:
    scope = run_middleware("///api/health")

    assert scope["path"] == "/api/health"
