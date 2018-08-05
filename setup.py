from setuptools import setup

setup(
    name='django-task-api',
    description='A REST API for managing background tasks in Django',
    keywords='django,task,api,background,rest',
    version='0.0.0',
    packages=['task_api', 'task_api.backends'],
    install_requires=['djangorestframework==3.*', 'django>=1.11', 'celery==4.*', 'six'],
    url='https://github.com/nikmolnar/django-task-api',
    license='MIT'
)
