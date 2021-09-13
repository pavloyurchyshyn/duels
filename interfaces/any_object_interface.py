from abc import ABC, abstractmethod


class AnyObjInterface(ABC):
    def __init__(self):
        self.KEY = None

    @abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError

    @property
    @abstractmethod
    def alive(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def dead(self):
        raise NotImplementedError
