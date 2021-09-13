from UI.UI_base.menu_UI import MenuUI
from settings.UI_setings.menus_settings.loading import PLAYER_PIC


class Loading_menu(MenuUI):
    def __init__(self):
        super().__init__(buttons={})
        self.create_buttons()

    def update(self):
        PLAYER_PIC.update()

    def draw(self, dx=0, dy=0):
        self._draw(dx, dy)
        PLAYER_PIC.draw()


LOADING_MENU_UI = Loading_menu()
