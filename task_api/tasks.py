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
        self.info = None

    def start(self, inputs):
        """ Starts the task on a background process """

        backend_cls = get_backend_cls()
        info = TaskInfo.objects.create(
            task=self.name,
            inputs=json.dumps(inputs or {}),
            created=now()
        )
        backend_cls().run_task(info, '.'.join((getmodule(self.__class__).__name__, self.__class__.__name__)))
        info.save()
        return info

    def execute(self, info):
        """ Execute the task """

        inputs = json.loads(info.inputs)

        TaskInfo.objects.filter(pk=info.pk).update(status='running', started=now())
        self.info = TaskInfo.objects.get(pk=info.pk)

        try:
            outputs = self.run(**{k: v.to_python(inputs[k]) for k, v in self.inputs.items() if k in inputs})
        except:  # Log and ignore exceptions
            TaskInfo.objects.filter(pk=info.pk).update(status='failed', finished=now())
            logger.exception('Task {} failed with inputs: {}'.format(self.__class__.__name__, inputs))
            return

        self.info = None

        if outputs is None:
            output_data = {}
        elif isinstance(outputs, dict):
            output_data = {k: v.to_json(outputs[k]) for k, v in self.outputs.items() if k in outputs}
        elif len(self.outputs) == 1:
            k = list(self.outputs.keys())[0]
            output_data = {k: self.outputs[k].to_json(outputs)}

        TaskInfo.objects.filter(pk=info.pk).update(status='succeeded', finished=now(), outputs=json.dumps(output_data))

    def add_message(self, message):
        """ Add a message to the task, which can be accessed from the API """

        messages = json.loads(self.info.messages)
        messages.append(message)
        self.info.messages = json.dumps(messages)
        self.info.save()

    def set_target(self, target):
        """ Set progress target """

        self.info.target = target
        self.info.save()

    def set_progress(self, progress):
        """ Set task progress """

        self.info.progress = progress
        self.info.save()

    def inc_progress(self, increment=1):
        """ Increment the task progress by some amount """

        self.info.progress += increment
        self.info.save()

    def run(self, **kwargs):
        """ Task implementation """

        raise NotImplemented
