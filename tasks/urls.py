from django.urls import path
from .views import health_check, TaskListCreateView, TaskDetailView
from tasks.views import alarm_test_500

urlpatterns = [
    path("health/", health_check, name="health_check"),
    path("tasks/", TaskListCreateView.as_view(), name="task_list_create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("alarm-test-500/", alarm_test_500),
]