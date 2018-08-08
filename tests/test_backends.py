import pytest

from task_api.backends.base import TaskBackend
from task_api.tasks import Task


class SomeTask(Task):
    pass


def test_resolve_class():
    assert TaskBackend().resolve_class('tests.test_backends.SomeTask') == SomeTask


def test_resolve_invalid_class():
    with pytest.raises(ImportError):
        TaskBackend().resolve_class('tests.test_backends.NoTask')


