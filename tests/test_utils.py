from django.core.exceptions import ImproperlyConfigured
from mock import patch
from pytest import raises

from task_api.utils import resolve_class, get_backend_cls


class Test(object):
    pass


def test_resolve_class():
    assert resolve_class('tests.test_utils.Test') == Test


def test_resolve_invalid_class():
    assert resolve_class('tests.test_utils.Foo') is None
    assert resolve_class('tests.foobar.Test') is None


@patch('task_api.utils.TASK_API_BACKEND', 'tests.test_utils.Test')
def test_get_backend_cls():
    assert get_backend_cls() == Test


@patch('task_api.utils.TASK_API_BACKEND', 'tests.test_utils.Foo')
def test_get_invalid_backend_cls():
    with raises(ImproperlyConfigured):
        get_backend_cls()


@patch('task_api.utils.TASK_API_BACKEND', 'tests.foobar.Test')
def test_get_invalid_backend_cls_module():
    with raises(ImproperlyConfigured):
        get_backend_cls()
