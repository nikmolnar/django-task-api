from importlib import import_module

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

TASK_API_BACKEND = getattr(settings, 'TASK_API_BACKEND', 'task_api.backends.celery.CeleryBackend')


def resolve_class(path):
    if isinstance(path, type):
        return path

    try:
        module_name, class_name = path.rsplit('.', 1)
        module = import_module(module_name)
        return getattr(module, class_name)
    except (ImportError, ValueError, AttributeError):
        return None


def get_backend_cls():
    if isinstance(TASK_API_BACKEND, type):
        return TASK_API_BACKEND
    elif isinstance(TASK_API_BACKEND, str):
        cls = resolve_class(TASK_API_BACKEND)
        if cls is not None:
            return cls
        else:
            raise ImproperlyConfigured('TASK_API_BACKEND is invalid: ' + TASK_API_BACKEND)
    else:
        raise ImproperlyConfigured('TASK_API_BACKEND is invalid type: ' + type(TASK_API_BACKEND).__name__)
