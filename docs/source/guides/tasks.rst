Tasks
=====

Task classes implement code to execute on a background process, and specify input and output names and types. Task
classes also provide methods for communicating progress and messages as the task runs.

Here's a basic task:

.. code-block:: python

    from task_api.tasks import Task
    from task_api.params import IntParameter, StringParameter

    class MyTask(Task):
        name = 'my-task'

        inputs = {
            'name':  StringParameter(),
            'count': IntParameter(required=False)
        }

        outputs = {'output': StringParameter()}

    def run(name, count=5):
        # Do stuff here
        return 'Some output'

First, note that all tasks must subclass ``task_api.tasks.Task``. All tasks must specify a ``name`` property, and
can optionally specify inputs and outputs. Parameters define input and output types: the determine how values are
converted from JSON to Python objects, and they return errors to the client on invalid values.

.. code-block:: python

    class MyTask(Task):
        name = 'my-task'  # The name used to call this task from the API

        inputs = { ... } # Task inputs
        outputs = { ... } # Task outputs

The task logic should be defined in a `run()` method, which accepts inputs named in accordance with the ``inputs``. Any
inputs marked with ``required=False`` must specify a default in the function declaration. The above example has a
required ``name`` input and an optional ``count`` input. Thus the run method looks like this:

.. code-block:: python

    def run(name, count=5):
        ...

Since the task has a single output, the return value of ``run()`` will be used as the output value. For tasks with
multiple outputs, ``run()`` should return a dictionary with keys matching the ``outputs`` property.

In order for tasks to be available through the API, they must be added to ``TASK_API_BACKGROUND_TASKS`` in
``settings.py``.

.. code-block:: python

    TASK_API_BACKGROUND_TASKS = [
        'myapp.background.MyTask'
    ]


Parameters
----------

The ``inputs`` and ``outputs`` properties determine which inputs the a client may and must provide to the API, and what
outputs it receives back. Parameter types are determined by parameter classes. Parameter provide type conversion and
enforcement. E.g., an ``IntParameter`` given a string input of ``"6"`` will yield an integer ``6``, whereas that same
parameter given a string input of ``"not a number"`` will raise an exception.

When specifying ``inputs``, all parameter constructors can optionally be given a ``required=`` argument. Inputs are
required by default, an API call with missing inputs will be rejected. Any parameters with ``required=False`` can be
omitted by the client. Some parameters may have additional optional or required arguments. For example, the
``ListParameter`` requires an argument with the type of elements in the list:

.. code-block:: python

    inputs = [
        'items': ListParameter(StringParameter())
    ]

``run()`` Method
----------------

Your task logic all goes in the ``run()`` method of your task class. ``run()`` should accept arguments corresponding
your ``inputs`` property. Django Task API will process each of parameters sent by the client and convert then to Python
objects as as specified in ``inputs`` (e.g., strings, ints, list, etc.). Any optional parameters must be given default
values:

.. code-block:: python

    inputs = [
        'must_have': StringParameter(required=True),
        'nice_to_have': StringParameter(required=False)
    ]

    def run(self, must_have, nice_to_have=None):
        ...

Parameters are required by default, so ``required=True`` isn't strictly necessary.

``run()`` must return values in accordance with parameters specified in the ``outputs`` property. If ``outputs`` only
specifies a single parameter, than ``run()`` may simply return that parameter:

.. code-block:: python

    outputs = [
        'out': StringParameter()
    ]

    def run(self):
        return 'Foo'

If the task has multiple outputs, then ``run()`` must return a dictionary of output values:

.. code-block:: python

    outputs = [
        'out': StringParameter()
        'count': IntParameter()
    ]

    def run(self):
        return {
            'out': 'Foo,
            'count': 5
        }

Progress & Messages
-------------------

Tasks can communicate with front-end code in two ways: updating progress, and adding messages. To use progress, first
set a target, then increment progress regularly throughout the task. Target and progress should both be integers.

.. code-block:: python

    def run(self):
        with open('lines.txt', 'r') as f:
            f.seek(0, os.SEEK_END)
            self.set_target(f.tell())
            f.seek(0, os.SEEK_SET)

            for line in f:
                process_line(line)
                self.set_progress(f.tell())

Authorization & Permissions
---------------------------

Django Task API uses Django Rest Framework (DRF) to define its API view. You can specify DRF authorization and
permissions classes to be used by the Task API with the ``TASK_API_AUTHENTICATION_CLASSES`` and
``TASK_API_PERMISSIONS_CLASSES`` settings.

.. code-block:: python

    TASK_API_AUTHENTICATION_CLASSES = ['rest_framework.authentication.SessionAuthentication']
    TASK_API_PERMISSIONS_CLASSES = ['rest_framework.permissions.IsAuthenticated']

The above restricts the Task API to logged in users.
