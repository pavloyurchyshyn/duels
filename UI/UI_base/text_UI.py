from common_things.font_loader import DEFAULT_FONT_SIZE
from common_things.global_clock import GLOBAL_CLOCK
from pygame import font, Surface
from pygame.transform import rotate, scale, smoothscale
from settings.colors import WHITE


class Text:
    DEFAULT_FONT_SIZE = DEFAULT_FONT_SIZE
    CLOCK = GLOBAL_CLOCK
    MIN_Y = 7

    def __init__(self, text, screen, x=None, y=None,
                 color=WHITE,
                 size=None,
                 shadow=False,
                 animation=False,
                 font_t='Arial',
                 antial=1,
                 angle=0):
        text = str(text)
        self._text = text.replace('\t', '    ')
        self._text_font = font_t

        self._r_text_font = None
        self._r_text_img_original = None
        self._r_text_img = None

        self._screen = screen

        self._screen_x_size, self._screen_y_size = self._screen.get_size()

        self._d_time, self._time = Text.CLOCK()

        self._size = size if size is not None else DEFAULT_FONT_SIZE

        self._angle = angle

        self._color = color
        self._antialias = antial

        self.render_text()

        self.set_x(x)
        self.set_y(y)

        self.draw()

    def set_x(self, x=None):
        if x is None:
            if '\n' not in self._text:
                x_s_s = self._screen.get_width()  # s_s -> screen size
                x_t_s = self._r_text_img.get_width()  # t_s -> text size

                screen_mid_x = x_s_s // 2
                text_mid_x = x_t_s // 2

                self._x = screen_mid_x - text_mid_x
            else:
                x_s_s = self._screen.get_width()  # s_s -> screen size

                l_string = max(self._text.split('\n'), key=len)
                l_str_surf = self._r_text_font.render(l_string, self._antialias, self._color)

                x_t_s = l_str_surf.get_width()  # t_s -> text size
                screen_mid_x = x_s_s // 2
                text_mid_x = x_t_s // 2

                pos = screen_mid_x - text_mid_x
                self._x = pos if pos > 0 else 5

        else:
            self._x = int(x)

    def set_y(self, y=None):
        if y is None:
            y_s_s = self._screen.get_height()  # s_s -> screen size
            y_t_s = self._r_text_img.get_height()  # t_s -> text size

            screen_mid_y = y_s_s // 2
            text_mid_y = y_t_s // 2

            if '\n' not in self._text:
                self._y = screen_mid_y - text_mid_y

            else:
                pos = screen_mid_y - y_t_s * len(self._text.split('\n'))
                self._y = pos + 5 if pos > -screen_mid_y + text_mid_y else Text.MIN_Y

        else:
            self._y = int(y)

    def update(self):
        # TODO: for animation and etc. in the future
        pass

    def change_text(self, text):
        self._text = text
        self.render_text()
        self.draw()

    def add_text(self, text):
        self._text = ' '.join((self._text, text))
        self.render_text()
        self.draw()

    def change_pos(self, x, y):
        """
        Change text position

        :return:
        """
        self._x, self._y = int(x), int(y)

    def draw(self, dx=0, dy=0):
        if '\n' in self._text:
            self._size = [0, 0]
            for i, text in enumerate(self._text.split('\n')):
                t_surf = self._r_text_font.render(text, self._antialias, self._color)
                self._screen.blit(t_surf, (self._x + dx, self._y + dy + (i + 1) * t_surf.get_height()))
                self._size[0] += t_surf.get_width()
                self._size[1] += t_surf.get_height()
        else:
            self._screen.blit(self._r_text_img, (self._x + dx, self._y + dy))

    def render_text(self):
        self._render_font()

        self._r_text_img_original = self._r_text_font.render(self._text, self._antialias, self._color).convert_alpha()

        x_size = self._screen_x_size if self._r_text_img_original.get_width() > self._screen_x_size else self._r_text_img_original.get_width()
        y_size = self._screen_y_size if self._r_text_img_original.get_height() > self._screen_y_size else self._r_text_img_original.get_height()

        self._r_text_img = smoothscale(self._r_text_img_original.copy(), (x_size, y_size))

        self._r_text_img = rotate(self._r_text_img, self._angle)  # .convert()
        self._size = self._r_text_img.get_size()

    def _render_font(self):
        try:
            self._r_text_font = font.SysFont(self._text_font, int(self._size))

        except:
            self._r_text_font = font.SysFont('Arial', int(self._size))

    @staticmethod
    def get_surface(size_x, size_y):
        surface = Surface((size_x, size_y), 0, 32)

        return surface

    @property
    def size(self):
        return self._size

    @property
    def text(self):
        return self._text

    @property
    def r_text(self):
        return self._r_text_font

    @property
    def sprite(self):
        return self._r_text_img
