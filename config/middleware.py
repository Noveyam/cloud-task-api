import logging
import time

logger = logging.getLogger("request")

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()
        response = self.get_response(request)
        duration = round((time.perf_counter() - start) * 1000, 2)

        logger.info(
            "request",
            extra={
                "method": request.method,
                "path": request.path,
                "status": getattr(response, "status_code", "500" ),
                "duration_ms": duration_ms,
            }
        )
        return response
