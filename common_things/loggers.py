import os
import datetime
import logging

from settings.common_settings import LOG_FILE_PATTERN, LOGS_FOLDER


if not os.path.exists(LOGS_FOLDER):
    os.mkdir(LOGS_FOLDER)

start = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
logging.basicConfig(filename=LOG_FILE_PATTERN.format(start), level=0)
LOGGER = logging.getLogger(__name__)
# logger.info(f'Game started {start}')
