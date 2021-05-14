from UI.UI_base.menuUI import MenuUI

from common_things.global_mouse import GLOBAL_MOUSE

from settings.UI_setings.menus_settings.main_menu import MAIN_MENU_BUTTONS


class MainMenuSettings(MenuUI):
    def __init__(self):
        super().__init__(buttons=MAIN_MENU_BUTTONS)
        self.create_buttons()

    def update(self):
        for button in self._buttons:
            button.update()

        if GLOBAL_MOUSE.lmb:
            for button in self._buttons:
                button.click(xy=self.GLOBAL_MOUSE.pos)
                if button.clicked:
                    break

    def draw(self, dx=0, dy=0):
        self._draw(dx, dy)

    def _update(self):
        pass


MAIN_MENU_UI = MainMenu()