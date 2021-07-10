from common_things.loggers import LOGGER
from time import time


def time_control_wrapper(func):
    def wrapper(*args, **kwargs):
        start = time()
        res = func(*args, **kwargs)
        # logger.info(f' {func.__name__} was running for {time() - start} seconds.')
        # logger.info(f' -------------------------------------------------------')
        return res

    return wrapper
