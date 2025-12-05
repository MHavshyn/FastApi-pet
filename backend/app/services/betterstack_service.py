import logging
import sys

from logtail import LogtailHandler
from settings import settings


def get_betterstack_logger():
    handler = LogtailHandler(
        source_token=settings.BETTER_STACK_TOKEN,
        host=settings.BETTER_STACK_URL,
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.handlers = []
    logger.addHandler(handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


get_betterstack_logger = get_betterstack_logger()
