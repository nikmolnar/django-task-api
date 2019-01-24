Django Task API
===============

Django Task API lets you quickly write background tasks for your Django project and easily call then using the provided
REST API, or the included JavaScript library.

What does it look like?
-----------------------

Tasks are defined as classes with typed input and output parameters, and a `run` function with the task implementation,
to be called by a worker processes.

.. code-block:: python

    from task_api.tasks import Task
    from task_api.params import ListParameter, NumberParameter

    class SumNumbers(Task):
        name = 'sum'

        inputs = {
            'numbers': ListParameter(NumberParameter())
        }

        outputs = {
            'sum': NumberParameter()
        }

        def run(self, numbers):
            return sum(numbers)

Tasks are easily called and monitored in front-end code using the included JavaScript API. The API supports both
promises (will Polyfill for older browsers) and traditional callbacks.

.. code-block:: html

    <script src="{% static 'django-task-api.min.js' %}"></script>

    <script type="text/javascript">
        function sumTask(numbers) {
            TaskAPI
                .run('sum', {'numbers': numbers})
                .then(function(json) {
                    console.log('Sum: ' + json.outputs.sum)
                })
        }
    </script>

Next Steps
----------

* `Getting Started <https://django-task-api.readthedocs.io/en/latest/start.html>`_
* `GitHub <https://github.com/nikmolnar/django-task-api>`_
