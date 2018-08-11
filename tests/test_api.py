import json

import pytest
from django.utils.timezone import now
from mock import patch

from task_api.models import TaskInfo
from task_api.params import StringParameter, NumberParameter
from task_api.tasks import Task


class CreateTask(Task):
    name = 'create_task'
    inputs = {
        'test': StringParameter(),
        'optional': StringParameter(required=False)
    }


@pytest.mark.django_db(transaction=True)
@patch('task_api.backends.celery.CeleryBackend')
def test_create_task(_, client):
    response = client.post(
        '/tasks/',
        json.dumps({'task': 'create_task', 'inputs': {'test': 'Test', 'optional': 'Test'}}),
        content_type='application/json'
    )

    assert response.status_code == 201
    assert TaskInfo.objects.all().count() == 1

    data = json.loads(response.content.decode())

    assert data['inputs'] == {'test': 'Test', 'optional': 'Test'}
    assert data['uuid'] == str(TaskInfo.objects.all().get().uuid)


def test_create_task_missing_inputs(client):
    response = client.post(
        '/tasks/',
        json.dumps({'task': 'create_task', 'inputs': {}}), content_type='application/json'
    )

    assert response.status_code == 400
    assert 'test' in response.content.decode()


@pytest.mark.django_db(transaction=True)
@patch('task_api.backends.celery.CeleryBackend')
def test_create_task_optional_input(_, client):
    response = client.post(
        '/tasks/',
        json.dumps({'task': 'create_task', 'inputs': {'test': 'Test'}}),
        content_type='application/json'
    )

    assert response.status_code == 201
    assert TaskInfo.objects.all().count() == 1

    data = json.loads(response.content.decode())

    assert data['inputs'] == {'test': 'Test'}
    assert data['uuid'] == str(TaskInfo.objects.all().get().uuid)


class CreateTackInvalidInputs(Task):
    name = 'create_task_invalid_inputs'
    inputs = {'test': NumberParameter()}


def test_create_task_invalid_inputs(client):
    response = client.post(
        '/tasks/',
        json.dumps({'task': 'create_task_invalid_inputs', 'inputs': {'test': 'foo'}}), content_type='application/json'
    )

    assert response.status_code == 400
    assert 'test' in response.content.decode()


@pytest.mark.django_db(transaction=True)
def test_get_task(client):
    info = TaskInfo.objects.create(
        task='tests.test_api.CreateTask',
        backend_data='Not public',
        status='running',
        inputs=json.dumps({'input': 'some input'}),
        outputs=json.dumps({'output': 'some output'}),
        messages=json.dumps(['message 1', 'message 2']),
        created=now(),
        started=now(),
        finished=now()
    )

    response = client.get('/tasks/{}/'.format(info.uuid))

    assert response.status_code == 200

    data = json.loads(response.content.decode())

    assert 'backend_data' not in data
    assert data['inputs']['input'] == 'some input'
    assert data['outputs']['output'] == 'some output'
    assert data['messages'] == ['message 1', 'message 2']
