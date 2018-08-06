import json

import pytest
from django.conf import settings

from task_api.models import TaskInfo
from task_api.params import StringParameter
from task_api.tasks import Task


class CreateTask(Task):
    name = 'create_task'
    inputs = {'test': StringParameter()}


@pytest.mark.django_db(transaction=True)
def test_create_task(client):
    settings.BACKGROUND_TASKS = ['tests.test_api.CreateTask']

    response = client.post(
        '/tasks/',
        json.dumps({'task': 'create_task', 'inputs': {'test': 'Test'}}), content_type='application/json'
    )

    assert response.status_code == 201
    assert TaskInfo.objects.all().count() == 1

    data = json.loads(response.content)

    assert data['inputs'] == {'test': 'Test'}
    assert data['uuid'] == str(TaskInfo.objects.all().get().uuid)

