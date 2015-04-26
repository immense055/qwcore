"""project tasks"""

from qwcore.tasks import *  # noqa


@task(default=True)
def all():
    test()
