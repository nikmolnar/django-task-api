import os
from distutils.cmd import Command
from distutils.log import ERROR
from subprocess import Popen

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist

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


class BuildCommand(build_py):
    def run(self):
        self.run_command('build_js')
        super().run()


class SDistCommand(sdist):
    def run(self):
        self.run_command('build_js')
        super().run()


class DevelopCommand(develop):
    def run(self):
        self.run_command('build_js')
        super().run()


setup(
    name='django-task-api',
    description='A REST API for managing background tasks in Django',
    keywords='django,task,api,background,rest',
    version='0.0.0',
    packages=['task_api', 'task_api.backends', 'task_api.migrations'],
    package_data={'task_api': ['static/*.js']},
    install_requires=['djangorestframework==3.*', 'django>=1.11', 'celery==4.*', 'six'],
    tests_require=['pytest-django', 'mock'],
    url='https://github.com/nikmolnar/django-task-api',
    license='MIT',
    cmdclass={
        'build_js': BuildJSCommand,
        'build_py': BuildCommand,
        'sdist': SDistCommand,
        'develop': DevelopCommand
    }
)
