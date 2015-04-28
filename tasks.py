"""project tasks"""

from qwcore.utils import configure_logging
from qwcore.tasks import *  # noqa

configure_logging(PROJECT)


@task(default=True)
def all():
    test()
