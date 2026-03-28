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
        scope["headers"] = [
            (b"host", b"localhost")
            if name == b"host" and _is_internal_host_bytes(value)
            else (name, value)
            for name, value in headers
        ]
    await _django_app(scope, receive, send)