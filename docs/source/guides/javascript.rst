JavaScript Client Library
=========================

The built-in JavaScript Client Library lets you run a task, and let's you know when when it's complete using a callback
or a promise. You can also use status callbacks to track or communicate task status, such as updating a gauge.

Installing
----------

There are two ways to get the JS library:

1. Include the script from your static files into an HTML template:

    .. code-block:: html

        {% load static %}

        {# ... #}

        <script src="{% static 'django-task-api.min.js' %}"></script>

2. Install with ``npm``. If you are using a build process for your front-end code, this is a good option::

    $ npm i --save django-task-api

Basic usage
-----------

Start tasks with the `run()` function. How you use this depends on how you installed the library. If you included
``django-task-api.min.js`` in your HTML template, you can access the library through the ``TaskAPI`` global variable:

.. code-block:: javascript

    TaskAPI.run(/* ... */)

Or if you installed the library using ``npm``, you can use ``import`` or ``require``:

.. code-block:: javascript

    import tasks from 'django-task-api'
    // Or
    var tasks = require('django-task-api')

    tasks.run(/* ... */)

The ``run()`` function takes two required inputs: the task name, and the task inputs. It also accepts an optional
progress callback function.

.. code-block:: javascript

    TaskAPI.run('my-task', {text: 'Hi'}, function(json) {
        console.log('Status: ' + json.status)
    })

You can use ``run()`` with either a promise, or success and error callbacks to receive notification upon a completed
task.

.. code-block:: javascript

    // Using promise
    TaskAPI
        .run('my-task', {text: 'Hi'})
        .then(function(json) { console.log('Success!' )})
        .catch(function(json) { console.log('Error.' )})

    // Using callbacks
    TaskAPI.run('my-task', {text: 'Hi!'}, null, function(json) {
        console.log('Success!')
    }, function(json) {
        console.log('Error!')
    })

Task API URL
------------

By default, the JS client will use `/tasks/` as the base URL for the Django Task API. If you choose to publish the API
at a different endpoint, you can change the JS client options to reflect this. For example, if you add the Django Task
API urls under ``/task-api/``, the full base URL will become ``/task-api/tasks``:

.. code-block:: python
    :caption: urls.py

    urlpatterns = [
        url(r'^task-api/', include('task_api.urls'))
    ]

Then you can set the ``baseURL`` option to match:

.. code-block:: javascript

    TaskAPI.options.baseURL = '/task-api/tasks/'
    TaskAPI.run(/* ... */)

Override CSRF names
-------------------

Django's built-in `CSRF protection <https://docs.djangoproject.com/en/1.11/ref/csrf/>`_ is a valuable security tool.
By default, the Djanto Task API JS library will work with the default CSRF cookie and header names. If you want to
change either of those, you can update the JS library to match:

.. code-block:: javascript

    TaskAPI.options.csrfCookieName = 'csrf-tok'
    TaskAPI.options.csrfHeaderName = 'X-CSRF'
    TaskAPI.run(/* ... */)
