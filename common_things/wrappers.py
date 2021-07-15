from common_things.loggers import LOGGER
from time import time


def time_control_wrapper(func):
    def wrapper(*args, **kwargs):
        start = time()
        res = func(*args, **kwargs)

        LOGGER.info(f' -------------------------------------------------------')
        LOGGER.info(f' {func.__name__} was running for {time() - start} seconds.')
        LOGGER.info(f' -------------------------------------------------------')
        return res

    return wrapper


def memory_keeper(func):
    memory = {}

    def wrapper(*args, **kwargs):
        if str((args, kwargs)) in memory:
            return memory[str((args, kwargs))]
        result = func(*args, **kwargs)
        memory[str((args, kwargs))] = result
        return result

    return wrapper
