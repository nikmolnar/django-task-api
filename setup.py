import os
import sys
from distutils.cmd import Command
from distutils.log import ERROR
from subprocess import Popen

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist

import task_api

DIR = os.path.dirname(__file__)


class BuildJSCommand(Command):
    description = 'Run webpack build'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.announce('Building JavaScript...')
        p = Popen(['npm', 'install'], cwd=os.path.join(DIR, 'javascript'))
        if p.wait() > 0:
            self.announce(p.stderr, level=ERROR)
            raise OSError('npm install failed')

        p = Popen(['npm', 'run-script', 'build'], cwd=os.path.join(DIR, 'javascript'))
        if p.wait() > 0:
            self.announce(p.stderr, level=ERROR)
            raise OSError('JavaScript build failed')


class BuildCommand(build_py, object):
    def run(self):
        self.run_command('build_js')
        super(BuildCommand, self).run()


class SDistCommand(sdist, object):
    def run(self):
        self.run_command('build_js')
        super(SDistCommand, self).run()


class DevelopCommand(develop, object):
    def run(self):
        self.run_command('build_js')
        super(DevelopCommand, self).run()


with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r') as f:
    long_description = f.read()

if sys.version_info[0] > 2:
    install_requires = ['djangorestframework==3.*', 'django>=1.11.23', 'celery==4.*', 'six']
else:
    install_requires = ['djangorestframework<3.10', 'django>=1.11.23,<1.12', 'celery==4.*', 'six', 'zipp<2']


setup(
    name='django-task-api',
    description='A REST API for managing background tasks in Django',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    keywords='django,task,api,background,rest',
    version=task_api.__version__,
    packages=['task_api', 'task_api.backends', 'task_api.migrations'],
    package_data={'task_api': ['static/*.js']},
    install_requires=install_requires,
    tests_require=['pytest-django', 'mock'],
    python_requires='>=3.6',
    url='https://github.com/nikmolnar/django-task-api',
    license='MIT',
    cmdclass={
        'build_js': BuildJSCommand,
        'build_py': BuildCommand,
        'sdist': SDistCommand,
        'develop': DevelopCommand
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
