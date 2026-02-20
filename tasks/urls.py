from django.urls import path
from .views import health_check
from .views import TaskCreateView

urlpatterns = [
    path("", health_check, name="root"),
    path("health/", health_check, name="health_check"),
    path("tasks/", TaskCreateView.as_view(), name="task_create"),
]