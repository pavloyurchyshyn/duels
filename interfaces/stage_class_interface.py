from abc import abstractmethod, ABC


class StageInterface(ABC):
    @abstractmethod
    def draw(self, dx, dy):
        raise NotImplementedError

    @abstractmethod
    def update(self):
        raise NotImplementedError