"""Home Assistant Ingress path handling."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

ASGIReceive = Callable[..., Awaitable[Any]]
ASGISend = Callable[..., Awaitable[Any]]
ASGIApp = Callable[[dict[str, Any], ASGIReceive, ASGISend], Awaitable[None]]


class HomeAssistantIngressMiddleware:
    """Handle Home Assistant Ingress with or without a forwarded prefix."""

    def __init__(self, app: ASGIApp, slug: str) -> None:
        self.app = app
        self.slug = slug

    async def __call__(
        self,
        scope: dict[str, Any],
        receive: ASGIReceive,
        send: ASGISend,
    ) -> None:
        if scope.get("type") not in {"http", "websocket"}:
            await self.app(scope, receive, send)
            return

        updated_scope = dict(scope)
        path = str(updated_scope.get("path", "/"))
        headers = {
            key.decode("latin-1").lower(): value.decode("latin-1")
            for key, value in updated_scope.get("headers", [])
        }

        public_prefix = headers.get("x-ingress-path", "").rstrip("/")
        prefix_to_strip = ""

        if public_prefix and (
            path == public_prefix or path.startswith(f"{public_prefix}/")
        ):
            prefix_to_strip = public_prefix
        else:
            first_segment = path.lstrip("/").split("/", 1)[0]
            panel_suffix = f"_{self.slug}"
            if first_segment.endswith(panel_suffix):
                public_prefix = f"/{first_segment}"
                prefix_to_strip = public_prefix

        if prefix_to_strip:
            path = path[len(prefix_to_strip) :] or "/"
            if not path.startswith("/"):
                path = f"/{path}"

            updated_scope["path"] = path
            updated_scope["raw_path"] = path.encode("utf-8")

        state = dict(updated_scope.get("state") or {})
        state["ingress_path"] = public_prefix
        updated_scope["state"] = state

        await self.app(updated_scope, receive, send)
