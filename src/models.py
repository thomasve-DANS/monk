from enum import Enum
import logging
import datetime

from pydantic import BaseModel

class LogEventChoices(Enum):
    info = 'info'
    error = 'error'
    warning = 'warning'
    critical = 'critical'
    exception = 'exception'


class LogEvent(BaseModel):

    message: dict
    level: LogEventChoices | None = LogEventChoices.info
    propagation_id: str | None = None

    def logger(self):
        return setup_root_logger(level = self.propagation_id)

    def log(self):
        logger = self.logger()
        func = getattr(logger, self.level.value)
        func(
            {'message': self.message,
             'level': self.level.value,
             'propagation_id': self.propagation_id}
        )

class CompletedLogEvent(LogEvent):

    timestamp: datetime.datetime | None = datetime.datetime.now()


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"


def setup_root_logger(level: str):
    """ Setup configuration of the root logger of the application """

    # get instance of root logger
    logger = logging.getLogger(level)

    # configure formatter for logger
    formatter = logging.Formatter(LOG_FORMAT)

    # configure console handler
    console = logging.StreamHandler()
    console.setFormatter(formatter)

    # configure rotating file handler
    logfile = logging.handlers.RotatingFileHandler(filename="logs/monk.log", mode='a',
                                                maxBytes=15000000, backupCount=5)
    logfile.setFormatter(formatter)

    # add handlers
    logger.addHandler(console)
    logger.addHandler(logfile)
    return logger
