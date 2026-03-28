import logging
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner

from .models import Task
from .serializers import TaskSerializer

from django.http import HttpResponse
from django.conf import settings

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

import logging
from django.conf import settings
from django.http import HttpResponse

logger = logging.getLogger(__name__)

def alarm_test_500(request):
    if getattr(settings, "SENTRY_ENVIRONMENT", "") != "staging":
        return HttpResponse(status=404)

    logger.error("test error log for cloudwatch alarm via HTTP")
    raise Exception("Intentional staging alarm test 500")

logger = logging.getLogger("django")

@api_view(["GET"])
@renderer_classes([JSONRenderer])
def health_check(request):
    logger.info("Health check called")
    return Response(
        {"status": "ok"},
        status=status.HTTP_200_OK
    )