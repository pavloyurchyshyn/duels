from abc import abstractmethod


class SimpleWeaponInterface:
    @abstractmethod
    def attack(self):
        raise NotImplementedError

    @abstractmethod
    @property
    def damage(self):
        raise NotImplementedError

    @abstractmethod
    def cooldown(self):
        raise NotImplementedError

    @abstractmethod
    def alt_attack(self):
        raise NotImplementedError