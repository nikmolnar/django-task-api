from time import sleep

from task_api import params
from task_api.tasks import Task


class JustWaitTask(Task):
    name = 'wait'

    inputs = {
        'start': params.IntParameter(required=False)
    }

    def run(self, start=1):
        self.set_target(start + 10)
        self.set_progress(start)

        for _ in range(10):
            sleep(1)
            self.inc_progress(1)
