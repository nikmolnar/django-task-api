import json

import pytest
from django.utils.timezone import now
from mock import patch

from task_api.models import TaskInfo
from task_api.params import StringParameter, NumberParameter
from task_api.tasks import Task


class SomeTask(Task):
    inputs = {
        'str': StringParameter(),
        'num': NumberParameter()
    }
    outputs = {
        'result': StringParameter()
    }

    def run(self, str=None, num=None):
        print('Success!')


def test_copy_inputs_outputs():
    task = Task()
    assert task.inputs is not Task.inputs
    assert task.outputs is not Task.outputs


@pytest.mark.django_db(transaction=True)
@patch('task_api.tasks.get_backend_cls')
def test_task_start(backend_cls_mock):
    SomeTask().start({})
    backend_cls_mock()().run_task.assert_called_once()


@pytest.mark.django_db(transaction=True)
@patch('tests.test_tasks.SomeTask.run')
def test_task_execute(run_mock):
    info = TaskInfo.objects.create(
        task='tests.test_tasks.SomeTask',
        inputs=json.dumps({'str': 'Hi', 'num': 5.3}),
        created=now()
    )
    SomeTask().execute(info)
    run_mock.assert_called_with(str='Hi', num=5.3)
    assert TaskInfo.objects.get(pk=info.pk).status == 'succeeded'


@pytest.mark.django_db(transaction=True)
@patch('tests.test_tasks.SomeTask.run')
def test_task_execute_optional_params(run_mock):
    info = TaskInfo.objects.create(
        task='tests.test_task.SomeTack',
        inputs=json.dumps({'num': 5}),
        created=now()
    )
    SomeTask().execute(info)
    run_mock.assert_called_with(num=5)
    assert TaskInfo.objects.get(pk=info.pk).status == 'succeeded'


@pytest.mark.django_db(transaction=True)
@patch('tests.test_tasks.SomeTask.run')
def test_task_execute_exception(run_mock):
    run_mock.side_effect = ValueError()
    info = TaskInfo.objects.create(
        task='tests.test_task.SomeTack',
        inputs=json.dumps({'num': 5}),
        created=now()
    )
    SomeTask().execute(info)
    run_mock.assert_called_with(num=5)
    assert TaskInfo.objects.get(pk=info.pk).status == 'failed'
