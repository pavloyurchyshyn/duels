from abc import abstractmethod


class Destroyable:
    def __init__(self, hp):
        self._hp = hp
        self._alive = 1

    @abstractmethod
    def damage(self, damage):
        self._damage(damage)

    def _damage(self, damage):
        self._hp -= damage
        if self._hp < 0:
            self._alive = 0

    @property
    def alive(self):
        return self._alive


CanDie = Destroyable
AliveObject = Destroyable


class Visible:
    """
    Object can change visibility.
    """

    def __init__(self, visible=1):
        """
        :param visible: if 1|True -> visible else invisible
        """
        self._visible = visible

        self._origin_draw = self.draw  # for fake draw

        if not visible:
            self.draw = self.fake_draw

    def change_visibility(self, value=-1):
        """
        Making fake draw.

        :param value: if value = -1 -> inverse visibility
        :return:
        """
        if value == -1:
            self._visible = not self._visible
        else:
            self._visible = value

        if self._visible:
            self.draw = self._origin_draw
        else:
            self.draw = self.fake_draw

    def fake_draw(self, *args, **kwargs):
        pass

    @property
    def visible(self):
        return self._visible


class Pickable:
    """
    If can be picked.
    """

    def __init__(self, picked=1, collide=1):
        self._picked = picked
        self._collide_able = collide

    def change_collide(self, c=-1):
        if c == -1:
            self._collide_able = not self._collide_able
        else:
            self._collide_able = c

    def pick(self):
        self._picked = 1

    def drop(self):
        self._picked = 0

    @property
    def picked(self):
        return self._picked
