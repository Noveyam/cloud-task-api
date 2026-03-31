from django.urls import path
from .views import health_check, TaskListCreateView, TaskDetailView, test_500

urlpatterns = [
    path("health/", health_check, name="health_check"),
    path("tasks/", TaskListCreateView.as_view(), name="task_list_create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("test-500/", test_500, name="test_500"),
]