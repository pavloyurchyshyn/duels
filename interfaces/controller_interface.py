from abc import ABC, abstractmethod


class ControllerInterface(ABC):

    @abstractmethod
    def update(self, d_time):
        raise NotImplementedError

    @abstractmethod
    def reload(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def draw(self):
        raise NotImplementedError

    @abstractmethod
    def add_item(self, item):
        raise NotImplementedError

    @abstractmethod
    def clear(self):
        raise NotImplementedError

    @abstractmethod
    def set_camera(self, camera):
        raise NotImplementedError