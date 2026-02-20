import logging
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

logger = logging.getLogger("django")

@api_view(["GET"])
@renderer_classes([JSONRenderer])
def health_check(request):
    logger.info("Health check called")
    return Response(
        {"status": "ok"},
        status=status.HTTP_200_OK
    )