from abc import abstractmethod


class CollideInterface:

    # did point inside object
    @abstractmethod
    def collide_point(self, xy: list) -> bool:
        raise NotImplementedError

    # did circle inside object
    @abstractmethod
    def collide_circle(self, xy: list, R) -> bool:
        raise NotImplementedError

    # if at least one dot inside object
    @abstractmethod
    def collide_dots(self, other) -> bool:
        raise NotImplementedError

    @abstractmethod
    def collide(self, other) -> bool:
        raise NotImplementedError

    @abstractmethod
    def scale(self, k):
        raise NotImplementedError

    def __contains__(self, item):
        return all(map(self.collide_point, item.dots))