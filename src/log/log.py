from datetime import datetime
import logging
import os

# Logging Level Values:
#  CRITICAL 50
#  ERROR    40
#  WARNING  30
#  INFO     20
#  DEBUG    10
#  UNSET     0

logfile = os.path.join(os.path.dirname(__file__), 'external_ip_notifier.log')
logging.basicConfig(filename=logfile, level=20)

timeformat = '%d/%m/%Y %H:%M:%S.%f'


def log_error(msg):
    _log(msg, level=40)


def log_warning(msg):
    _log(msg, level=30)


def log_general(msg):
    _log(msg, level=20)


def _log(log_msg, level=20):
    #
    log_msg = _add_timestamp(log_msg)
    #
    if level == 50:
        logging.critical(log_msg)
    elif level == 40:
        logging.error(log_msg)
    elif level == 30:
        logging.warning(log_msg)
    elif level == 20:
        logging.info(log_msg)
    else:
        logging.debug(log_msg)


def _add_timestamp(log_msg):
    return '{timestamp} - {log_msg}'.format(timestamp=datetime.now().strftime(timeformat),
                                            log_msg=log_msg)
