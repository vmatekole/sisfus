import logging
from logging import Logger

from dotenv import load_dotenv
from rich.logging import RichHandler

from base.config import ConfigSettings


def init() -> Logger:
    level = ConfigSettings.log_level
    logFormatter = logging.Formatter(
        '%(levelname)s %(asctime)s %(processName)s %(message)s'
    )
    richhandler: RichHandler = RichHandler()

    rootLogger = logging.getLogger()
    rootLogger.setLevel(level=level)

    for hdlr in [richhandler]:
        rootLogger.addHandler(hdlr)
        hdlr.setFormatter(logFormatter)
        hdlr.setLevel(level)
    return rootLogger

logger: Logger = init()
