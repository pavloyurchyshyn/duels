from UI.UI_base.menu_UI import MenuUI

from settings.colors import BLACK, HALF_EMPTY_L, WHITE
from settings.window_settings import HALF_SCREEN_W, SCREEN_H
from settings.UI_setings.menus_settings.multiplayer import MULTIPLAYER_BUTTONS, SERVER_PASSWORD, IP_VALUE, \
    P_NUM, PLAYERS_NUMBER, SERVER_ADDRESS_TEXT, SERVER_ADDRESS, NICKNAME_INPUT, NICKNAME_TEXT, \
    PASSWORD_INPUT_CLIENT, PASSWORD_TEXT_CLIENT, PASSWORD_TEXT_HOST
from settings.UI_setings.button_settings import DEFAULT_BUTTON_X_SIZE, DEFAULT_BUTTON_Y_SIZE
from pygame.draw import line as DrawLine
from UI.UI_base.messages_UI import Messager


class Multiplayer(MenuUI):
    def __init__(self):
        super().__init__(buttons=MULTIPLAYER_BUTTONS)
        self.create_buttons()
        self._exit_warning = False
        self._fade_surface = self.get_surface(transparent=True)
        self._fade_surface.fill(HALF_EMPTY_L)
        self._fade_surface.convert_alpha()
        self._server_pswrd = SERVER_PASSWORD
        self.network_messager = Messager(HALF_SCREEN_W - 400, 700,
                                         size_x=int(DEFAULT_BUTTON_X_SIZE * 5.5),
                                         size_y=DEFAULT_BUTTON_Y_SIZE * 5,
                                         message_width=DEFAULT_BUTTON_X_SIZE * 5,
                                         transparent=0, background_color=(1, 1, 1, 255))

    def update(self):
        PASSWORD_INPUT_CLIENT.update()
        self._server_pswrd.update()

        for button in self._elements:
            button.update()

        if self.click():
            xy = self.GLOBAL_MOUSE.pos
            for button in self._buttons:
                button.click(xy)

        NICKNAME_INPUT.update()

        self.network_messager.update()

    def draw(self, dx=0, dy=0):
        self._draw(dx, dy)
        DrawLine(self.surface, WHITE, (HALF_SCREEN_W, 0), (HALF_SCREEN_W, SCREEN_H), 2)

        if self._exit_warning:
            self.surface.blit(self._fade_surface, (0, 0))

        self._server_pswrd.draw(dx, dy)
        IP_VALUE.draw(dx, dy)
        P_NUM.draw(dx, dy)
        PASSWORD_TEXT_HOST.draw(dx, dy)
        PLAYERS_NUMBER.draw(dx, dy)
        SERVER_ADDRESS_TEXT.draw(dx, dy)
        SERVER_ADDRESS.draw(dx, dy)

        NICKNAME_TEXT.draw(dx, dy)
        NICKNAME_INPUT.draw(dx, dy)

        PASSWORD_INPUT_CLIENT.draw(dx, dy)
        PASSWORD_TEXT_CLIENT.draw(dx, dy)


        self.network_messager.draw()

    def _update(self):
        pass


MULTIPLAYER_UI = Multiplayer()
