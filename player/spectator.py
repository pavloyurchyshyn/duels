from player.base.base_player import BasePlayer


class Spectator(BasePlayer):
    def __init__(self, arena):
        super(Spectator, self).__init__(*arena._center, arena=arena)

    def update(self, commands=(), mouse=(0, 0, 0), mouse_pos=None):
        self.make_step(commands=commands)

    def _additional_lazy_load(self):
        pass

    def _pictures_lazy_load(self):
        pass

    def draw(self):
        pass

    def _draw(self):
        pass
