import logging
import sys


def configure_logging(namespace, log_format='%(message)s', log_level='INFO'):
    """Setup logging"""
    logger = logging.getLogger(namespace)
    formatter = logging.Formatter(log_format)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.setLevel(getattr(logging, log_level))
    logger.addHandler(handler)
