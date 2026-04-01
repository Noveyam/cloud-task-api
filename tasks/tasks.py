from celery import shared_task
from django.utils import timezone
from .models import Task

@shared_task
def health_log_task():
    return {"status": "ok"}

@shared_task
def count_overdue_tasks():
    return Task.objects.filter(due_date__lt=timezone.now().date()).count()