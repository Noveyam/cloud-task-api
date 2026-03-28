import json
import logging
import re
import time
import uuid

logger = logging.getLogger("request")

def is_internal_host(raw_host: str) -> bool:
    if not raw_host:
        return False
    return bool(re.match(r"^10\.\d+\.\d+\.\d+(?::\d+)?$", raw_host))

class InternalK8sHostRewriteMiddleware:
    """
    Rewrite internal Kubernetes pod IP host headers like 10.x.x.x:8000
    to localhost before Django host validation runs.

    This keeps public host validation strict while avoiding noisy
    DisallowedHost errors from internal probes / cluster traffic.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        raw_host = request.META.get("HTTP_HOST", "")
        if is_internal_host(raw_host):
            request.META["HTTP_HOST"] = "localhost"
            request.META["SERVER_NAME"] = "localhost"
        return self.get_response(request)

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()
        request_id = (
            request.headers.get("X-Request-ID")
            or request.META.get("HTTP_X_REQUEST_ID")
            or str(uuid.uuid4())
        )
        request.request_id = request_id
        response = self.get_response(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        else:
            client_ip = request.META.get("REMOTE_ADDR")
        user_id = None
        user = getattr(request, "user", None)
        if user is not None and getattr(user, "is_authenticated", False):
            user_id = getattr(user, "id", None)
        logger.info(json.dumps({
            "event": "request",
            "request_id": request_id,
            "method": request.method,
            "path": request.path,
            "status_code": getattr(response, "status_code", 500),
            "duration_ms": duration_ms,
            "client_ip": client_ip,
            "user_id": user_id,
        }))

        response["X-Request-ID"] = request_id
        return response