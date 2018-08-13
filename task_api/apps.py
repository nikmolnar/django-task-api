from django.apps import AppConfig

class TaskAPIConfig(AppConfig):
    name = 'task_api'
    verbose_name = 'Django Task API'

    def ready(self):
        from .backends import celery  # Make sure task is registered
