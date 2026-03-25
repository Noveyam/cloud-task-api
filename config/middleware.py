import logging
import time

logger = logging.getLogger("request")


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()

        request_id = (
            request.headers.get("x-request-id") 
            or request.META.get("HTTP_X_REQUEST_ID")
            or str(uuid.uuid4())
        )

        request.request_id = request_id

        response = self.get_response(request)

        duratiom_ms = round((time.perf_counter() - start) * 1000, 2)

        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        else:
            client_ip = request.META.get("REMOTE_ADDR")

        user_id: Any = None
        user = getattr(request, "user", None)
        if user is not None and getattr(user, "is_authenticated", False):
            user_id = getattr(user, "id", None)

        log_payload = {
            "event": "request",
            "request_id": request_id,
            "method": request.method,
            "path": request.path,
            "status_code": getattr(response, "status_code", 500),
            "duration_ms": duratiom_ms,
            "user_id": user_id,
            "client_ip": client_ip,
        }

        logger.info(json.dumps(log_payload))

        response["X-Request-ID"] = request_id
        return response