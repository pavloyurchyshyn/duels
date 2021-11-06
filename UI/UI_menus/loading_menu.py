from UI.UI_base.menu_UI import MenuUI
from settings.UI_setings.menus_settings.loading import PLAYER_PIC
from settings.game_stages_constants import LOADING_STAGE


class Loading_menu(MenuUI):
    def __init__(self):
        super().__init__(name=LOADING_STAGE)
        self.create_buttons()

    def update(self):
        PLAYER_PIC.update()

    def draw(self, dx=0, dy=0):
        self._draw(dx, dy)
        PLAYER_PIC.draw()


LOADING_MENU_UI = Loading_menu()
