"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.asgi import get_asgi_application

_django_app = get_asgi_application()

_INTERNAL_IP_RE = re.compile(rb"^10\.\d+\.\d+\.\d+(?::\d+)?$")


async def application(scope, receive, send):
    if scope["type"] == "http":
        rewritten_headers = []

        for name, value in scope.get("headers", []):
            if name == b"host" and _INTERNAL_IP_RE.match(value):
                rewritten_headers.append((b"host", b"localhost"))
            else:
                rewritten_headers.append((name, value))

        scope["headers"] = rewritten_headers

    await _django_app(scope, receive, send)