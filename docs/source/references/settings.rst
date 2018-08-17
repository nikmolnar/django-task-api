Settings
========

TASK_API_AUTHENTICATION_CLASSES
-------------------------------

Authentication classes to be used by the Task API view. These should be Django Rest Framework (DRF) authentication
classes. See DRF's `Authentication <http://www.django-rest-framework.org/api-guide/authentication/>`_ guide for more
info.

TASK_API_BACKEND
----------------

The task backend class. Defaults to ``task_api.backends.celery.CeleryBackend``, which is the only built-in backend.

TASK_API_BACKGROUND_CLASSES
---------------------------

A list of ``Task`` classes to be provided by the API. For example:

.. code-block:: python

    TASK_API_BACKGROUND_CLASSES = [
        'myapp.background.MyTask'
    ]

You can also use class objects directly. For example:

.. code-block:: python

    from myapp.background import MyTask

    TASK_API_BACKGROUND_CLASSES = [MyTask]

Note that the above example uses the class definition, *not* a class instance.

TASK_API_PERMISSIONS_CLASSES
----------------------------

Permissions classes to be used by the Task API view. These should be Django Rest Framework (DRF) permissions classes.
See DRF's `Permissions <http://www.django-rest-framework.org/api-guide/permissions/>`_ guide for more info.
