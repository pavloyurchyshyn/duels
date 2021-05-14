from abc import ABC, abstractmethod
from common_things.global_clock import ROUND_CLOCK

class AnyObjInt(ABC):
    def __init__(self):
        self._clock = ROUND_CLOCK
        self._time, self._d_time = self._clock()

    @abstractmethod
    def draw(self, d_time):
        raise NotImplementedError

    @abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError
