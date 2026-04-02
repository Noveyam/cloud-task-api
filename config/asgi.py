"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import ipaddress

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.asgi import get_asgi_application

_ALLOWED_HOST_SUFFIXES = (b"noveycloud.com", b"localhost", b"127.0.0.1")

_django_app = get_asgi_application()

def _is_internal_host_bytes(value: bytes) -> bool:
    try:
        host = value.decode("ascii").split(":", 1)[0]
        return ipaddress.ip_address(host).is_private
    except Exception:
        return False

async def application(scope, receive, send):
    if scope["type"] == "http":
        headers = scope.get("headers", [])
        host = next((v for k, v in headers if k == b"host"), b"")

        if _is_internal_host(host):
            scope["headers"] = [
                (b"host", b"localhost") if k == b"host" else (k, v)
                for k, v in headers
            ]
        elif not any(host.endswith(s) for s in _ALLOWED_HOST_SUFFIXES):
            await send({"type": "http.response.start", "status": 400, "headers": []})
            await send({"type": "http.response.body", "body": b""})
            return

    await _django_app(scope, receive, send)