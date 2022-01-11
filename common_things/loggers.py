import os
import datetime
import logging
from common_things.singletone import Singleton
from settings.common_settings import LOG_FILE_PATTERN, LOGS_FOLDER
from shutil import rmtree


class Logger(metaclass=Singleton):

    def __init__(self):
        if not os.path.exists(LOGS_FOLDER):
            os.mkdir(LOGS_FOLDER)
        else:
            try:
                rmtree(LOGS_FOLDER)
                os.mkdir(LOGS_FOLDER)
            except:
                pass

        start = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
        logging.basicConfig(filename=LOG_FILE_PATTERN.format('last'),
                            format='%(asctime)s|%(levelname)s: %(message)s', datefmt='%H:%M:%S',
                            level=0)
        self.LOGGER = logging.getLogger(__name__)
        self.LOGGER.info(f'Start: {start}')

LOGGER = Logger().LOGGER
# logger.info(f'Game started {start}')
