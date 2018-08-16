from time import sleep

from task_api import params
from task_api.tasks import Task


class JustWaitTask(Task):
    name = 'wait'

    inputs = {
        'seconds': params.IntParameter(required=False)
    }

    def run(self, seconds=10):
        self.set_target(seconds)
        self.set_progress(0)

        for _ in range(10):
            self.inc_progress(1)
            sleep(1)
