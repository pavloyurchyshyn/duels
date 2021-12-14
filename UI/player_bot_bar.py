from settings.screen_size import X_SCALE, Y_SCALE, GAME_SCALE, SCREEN_H, SCREEN_W, HALF_SCREEN_W, HALF_SCREEN_H
from UI.UI_base.button_UI import Button
from common_things.sprites_functions import get_surface
from settings.UI_setings.player_bot_bar_settigns import BAR_X_SIZE, BAR_Y_SIZE
from settings.window_settings import MAIN_SCREEN


class PlayerBotBar:
    X_SIZE = BAR_X_SIZE * X_SCALE
    Y_SIZE = BAR_Y_SIZE * Y_SCALE
    X_POSITION = SCREEN_W // 2 - X_SIZE // 2
    Y_POSITION = SCREEN_H - Y_SIZE

    def __init__(self, player):
        self._player = player
        self._surface = get_surface(self.X_SIZE, self.Y_SIZE, transparent=1, color=(100, 100, 100))

    def build(self):
        pass

    def update(self):
        pass

    def draw(self):
        MAIN_SCREEN.blit(self._surface, (self.X_POSITION, self.Y_POSITION))
