from abc import abstractmethod


class CreaturePart:
    def __init__(self, hp):
        self._hp = hp
        self._alive = 1

    @abstractmethod
    def collide(self):
        raise NotImplementedError

    @abstractmethod
    def damage(self, dmg):
        self._damage(dmg)

    def _damage(self, dmg):
        self._hp -= dmg
        if self._hp < 0:
            self._alive = 0

    @property
    def alive(self):
        return self._alive
