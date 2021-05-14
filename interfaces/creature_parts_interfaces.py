from abc import ABC, abstractmethod


class CreatureBrainInterface(ABC):

    @abstractmethod
    def update(self):
        """
        Use parts of creature

        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def set_body(self, body):
        raise NotImplementedError


class CreatureBodyInterface(ABC):

    @abstractmethod
    def use_commands(self, commands):
        raise NotImplementedError

    @abstractmethod
    def see_player(self):
        raise NotImplementedError
