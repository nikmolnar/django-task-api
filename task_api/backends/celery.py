from __future__ import absolute_import

import json

from celery import shared_task

from task_api.backends.base import TaskBackend
from task_api.models import TaskInfo


class CeleryBackend(TaskBackend):
    def run_task(self, info, class_str):
        result = execute.delay(info.pk, class_str)
        info.backend_data = json.dumps({'celery_id': result.id})

@shared_task
def execute(task_id, class_str):
    info = TaskInfo.objects.get(pk=task_id)
    cls = CeleryBackend().resolve_class(class_str)
    cls().execute(info)
