"""invoke tasks"""

import logging
import os
import shutil

from invoke import run as irun
from invoke import task as itask
from invoke import Task

from qwcore.utils import get_plugins

PROJECT_ROOT = os.getcwd()
PROJECT = os.path.basename(PROJECT_ROOT)
PACKAGE = __import__(PROJECT, fromlist=['cli', '__about__'])
PACKAGE_PATH = os.path.join(PROJECT_ROOT, PROJECT)
DOCS_PATH = os.path.join(PROJECT_ROOT, 'docs')
MODULES_PATH = os.path.join(DOCS_PATH, 'modules')

logger = logging.getLogger(PROJECT)


def run(*args, **kwargs):
    """a run that logs red when it fails"""
    r = irun(*args,  warn=True, **kwargs)
    if not r.ok:
        logger.error("Command Failed")
        raise SystemExit(1)
    return r


def task(*args, **kwargs):
    """
    decorator that adds logging to invoke's task decorator
    """
    if len(args) == 1 and callable(args[0]) and not isinstance(args[0], Task):
        withargs = False
    else:
        withargs = True

    def wrapper_maker(mytask):
        def wrapper():
            logger.info("Begin: %s" % mytask.__name__)
            mytask()
            logger.info("Completed: %s" % mytask.__name__)
        wrapper.__name__ = mytask.__name__
        return wrapper
    if withargs:
        def decorator(mytask):
            wrapper = wrapper_maker(mytask)
            return itask(*args, **kwargs)(wrapper)
        return decorator
    else:
        mytask = args[0]
        wrapper = wrapper_maker(mytask)
        return itask(wrapper)


@task
def install_editable():
    cmd = 'pip install -e .'
    logger.info(cmd)
    run(cmd)


@task
def rst_api():
    if os.path.isdir(MODULES_PATH):
        shutil.rmtree(MODULES_PATH)
    api_cmd = 'sphinx-apidoc {pkg_path} {pkg_path}/tests {pkg_path}/tasks.py -o docs/modules -e -T -f'
    run(api_cmd.format(pkg_path=PACKAGE_PATH))


@task(pre=[install_editable])
def rst_cli():
    rst = []
    rst.extend(['.. _%s_reference:' % PROJECT, ''])
    rst.extend(['%s cli' % PROJECT, '='*50, ''])
    rst.extend(['.. contents:: Contents', '   :local:', ''])
    rst.extend([PROJECT, '-'*50, ''])
    r = run('%s --help' % PROJECT)
    out = ['  ' + l for l in r.stdout.splitlines()]
    rst.extend(['::', ''] + out + [''])
    cmds = get_plugins(PACKAGE.cli.COMMAND_GROUP)
    for name, cmd in sorted(cmds.items()):
        full_cmd = "%s %s" % (PROJECT, name)
        rst.extend([full_cmd, '-'*50, ''])
        r = run('%s --help' % full_cmd)
        out = ['  ' + l for l in r.stdout.splitlines()]
        rst.extend(['::', ''] + out + [''])
    with open(os.path.join(DOCS_PATH, 'cli.rst'), 'w') as fh:
        fh.write("\n".join(rst))


@task
def rst_docs_index():
    rst = []
    rst.extend(['='*50, PROJECT, '='*50, ''])
    rst.extend(['.. note::', '', '   a work in progress...', ''])
    rst.extend([PACKAGE.__about__.DESCRIPTION_RST, ''])
    rst.extend(['.. toctree::', '  :maxdepth: 2', '', '  overview', '  guide', '  reference'])
    with open(os.path.join(DOCS_PATH, 'index.rst'), 'w') as fh:
        fh.write("\n".join(rst))


@task
def rst_readme():
    rst = []
    rst.extend(['.. image:: https://secure.travis-ci.org/pyospkg/%s.png?branch=master' % PROJECT,
                '   :target: http://travis-ci.org/pyospkg/%s' % PROJECT, ''])
    rst.extend([PACKAGE.__about__.DESCRIPTION_RST, ''])
    rst.extend(['Docs:  http://%s.readthedocs.org/en/latest/' % PROJECT])
    with open(os.path.join(PROJECT_ROOT, 'readme.rst'), 'w') as fh:
        fh.write("\n".join(rst))


@task
def rst_all():
    rst_api()
    rst_cli()
    rst_docs_index()
    rst_readme()


@task(pre=[install_editable])
def docs():
    run('sphinx-build -W -b html -d docs/_build/doctree docs docs/_build/html')


@task
def test():
    cmd = 'tox -e py27,flake8,py3flake8'
    logger.info(cmd)
    run(cmd)


@task(default=True)
def all():
    rst_all()
    docs()
    test()
