import copy
import json
import logging
from inspect import getmodule

from django.utils.timezone import now

from task_api.models import TaskInfo
from task_api.utils import get_backend_cls

logger = logging.getLogger(__name__)


class Task(object):
    name = ''

    inputs = {}
    outputs = {}

    def __init__(self):
        self.inputs = copy.copy(self.inputs)
        self.outputs = copy.copy(self.outputs)

    def start(self, inputs):
        """ Starts the task on a background process """

        backend_cls = get_backend_cls()
        info = TaskInfo.objects.create(
            inputs=json.dumps(inputs or {}),
            created=now()
        )
        backend_cls().run_task(info, '.'.join((getmodule(self.__class__).__name__, self.__class__.__name__)))
        info.save()
        return info

    def execute(self, info):
        """ Execute the task """

        inputs = json.loads(info.inputs)

        TaskInfo.objects.filter(pk=info.pk).update(status='running')
        try:
            outputs = self.run(**{k: v.to_python(inputs[k]) for k, v in self.inputs.items() if k in inputs})
        except:  # Log and ignore exceptions
            TaskInfo.objects.filter(pk=info.pk).update(status='failed')
            logger.exception('Task {} failed with inputs: {}'.format(self.__class__.__name__, inputs))
            return

        TaskInfo.objects.filter(pk=info.pk).update(status='succeeded')

        if outputs is None:
            return
        elif isinstance(outputs, dict):
            info.outputs = json.dumps({k: v.to_json(outputs[k]) for k, v in self.outputs.items() if k in outputs})
        elif len(self.outputs) == 1:
            k = list(self.outputs.keys())[0]
            info.outputs = json.dumps({k: self.outputs[k].to_json(outputs)})

    def run(self, **kwargs):
        """ Task implementation """

        raise NotImplemented
