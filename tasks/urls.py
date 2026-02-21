from django.urls import path
from .views import health_check, TaskListCreateView, TaskDetailView

urlpatterns = [
    path("", health_check, name="root"),
    path("health/", health_check, name="health_check"),
    path("tasks/", TaskListCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
]