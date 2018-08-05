from importlib import import_module

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

TASK_API_BACKEND = settings.get('TASK_API_BACKEND', 'task_api.backends.celery.CeleryBackend')


def get_backend_cls():
    if isinstance(TASK_API_BACKEND, type):
        return TASK_API_BACKEND
    elif isinstance(TASK_API_BACKEND, str):
        try:
            module_name, class_name = TASK_API_BACKEND.rsplit('.', 1)
            module = import_module(module_name)
            cls = getattr(module, class_name)
        except (ImportError, ValueError, AttributeError):
            raise ImproperlyConfigured('TASK_API_BACKEND is invalid: ' + TASK_API_BACKEND)
        return cls
    else:
        raise ImproperlyConfigured('TASK_API_BACKEND is invalid type: ' + type(TASK_API_BACKEND).__name__)
