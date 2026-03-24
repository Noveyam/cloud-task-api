import logging
import time

logger = logging.getLogger("request")


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()

        response = self.get_response(request)

        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        logger.info(
            f"{request.method} {request.path} {getattr(response, 'status_code', 500)} {duration_ms}ms"
        )

        return response