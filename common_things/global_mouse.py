from pygame import mouse
from settings.window_settings import MAIN_SCREEN


class Mouse:
    MOUSE_SIZE = (21, 32)
    MAIN_SCREEN = MAIN_SCREEN

    def __init__(self, rel=None, pos=None, pressed=None):
        self.mouse = mouse
        self._rel = self.mouse.get_rel() if rel is None else rel
        self._pos = self.mouse.get_pos() if pos is None else pos
        self._pressed = self.mouse.get_pressed() if pressed is None else pressed
        self._scroll_top = 0
        self._scroll_bot = 0

        try:
            from common_things.img_loader import load_image
            self._pic = load_image('sprites/m_cursor.png', Mouse.MOUSE_SIZE, 0)
            mouse.set_pos(500, 500)
        except:
            pass
        else:
            self.mouse.set_visible(0)

    def update(self):
        self._rel = self.mouse.get_rel()
        self._pos = self.mouse.get_pos()
        self._pressed = self.mouse.get_pressed()
        self._scroll_top = 0
        self._scroll_bot = 0

    def set_position(self, pos):
        self.mouse.set_pos(pos)

    def draw(self):
        Mouse.MAIN_SCREEN.blit(self._pic, self._pos)

    @property
    def lmb(self):
        return self._pressed[0]

    @property
    def data(self):
        return self._pressed, self._scroll_top, self._scroll_bot, self._pos, self._rel

    @property
    def scroll_top(self):
        return self._scroll_top

    @scroll_top.setter
    def scroll_top(self, value):
        self._scroll_top = value

    @property
    def scroll_bot(self):
        return self._scroll_bot

    @scroll_bot.setter
    def scroll_bot(self, value):
        self._scroll_bot = value

    @property
    def scroll(self):
        return self._scroll_top, self._scroll_bot

    @property
    def rel(self):
        return self._rel

    @property
    def pos(self):
        return self._pos

    @property
    def pressed(self):
        return self._pressed


GLOBAL_MOUSE = Mouse()
