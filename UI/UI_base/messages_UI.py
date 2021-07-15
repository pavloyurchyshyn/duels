from UI.UI_base.text_UI import Text
from obj_properties.rect_form import Rectangle
from settings.UI_setings.button_settings import DEFAULT_BUTTON_Y_SIZE, DEFAULT_BUTTON_X_SIZE
from pygame.constants import SRCALPHA
from pygame import Surface
from pygame.draw import lines
from settings.window_settings import MAIN_SCREEN
from common_things.global_clock import GLOBAL_CLOCK
from settings.screen_size import X_SCALE, Y_SCALE


class Messager(Rectangle):
    MESSAGE_TIME = 5  # seconds

    def __init__(self, x, y,
                 size_x=None, size_y=None,
                 message_width=None,
                 message_height=None,
                 background_color=(0, 0, 0, 50),  # r, g, b, t
                 transparent=1,
                 draw_border=True,
                 draw_surface_every_time=True
                 ):
        x = int(x)
        y = int(y)
        size_x = int(size_x * X_SCALE) if size_x else DEFAULT_BUTTON_X_SIZE
        size_y = int(size_y * Y_SCALE) if size_y else DEFAULT_BUTTON_Y_SIZE
        message_width = int(message_width * X_SCALE) if message_width else DEFAULT_BUTTON_X_SIZE
        message_height = int(message_height * Y_SCALE) if message_height else DEFAULT_BUTTON_Y_SIZE

        super().__init__(x, y, size_x, size_y)
        # --------- BACKGROUND ------------------
        self._background_t = transparent
        self._background_color = background_color
        # ---------------------------------------
        self.surface = self.get_surface(self._background_t, color=self._background_color)

        self.messages_width = message_width
        self.messages_height = message_height
        self.messages_surf = self.get_surface(size=(self.messages_width, self.messages_height))

        self.border = draw_border
        self.print_surface_every_time = draw_surface_every_time

        self._messages = []
        self._time = self._d_time = GLOBAL_CLOCK.d_time

        self.fake_update = False

    def update(self):
        self._d_time = GLOBAL_CLOCK.d_time
        self._time += self._d_time

        _d = 0
        for i, message in enumerate(self._messages.copy()):
            if message['endtime'] < self._time:
                del self._messages[self._messages.index(message)]
                _d = 1

        if _d or self.fake_update:
            self.fake_update = 0
            self.surface.fill(self._background_color)
            if self._messages:
                for message in self._messages:
                    self.surface.blit(message['img'], (10, message['y']))

    def get_messages_height(self, idx=None):
        y = 0
        idx = idx - 1 if idx else len(self._messages) - 2
        for message in self._messages[:idx]:
            y_size = message['y_size']
            y += y_size

        return y

    def add_message(self, text, msg_time=None):
        text = Text(f"{text}", screen=self.surface)
        msg_time = msg_time if msg_time else self.MESSAGE_TIME

        for message in self._messages:
            message['y'] += text.size[1]

        new_message = {
            'img': text.sprite,
            'endtime': self._time + msg_time,
            'y_size': text.size[1],
            'x': self.x0,
            'y': 10,
        }

        self._messages.insert(0, new_message)
        self.fake_update = 1

    def get_surface(self, transparent=0, color=None, size=None):
        color = color if color else self._background_color
        flags = 0
        size = size if size else (self.size_x, self.size_y)
        if self._background_t or transparent:
            flags = SRCALPHA

        surface = Surface(size, flags, 32)
        if color:
            surface.fill(color)

        if self._background_t or transparent:
            surface.convert_alpha()

        return surface

    def draw(self, dx=0, dy=0):
        if self._messages or self.print_surface_every_time:
            MAIN_SCREEN.blit(self.surface, (self.x0 + dx, self.y0 + dy))

        if self.border:
            lines(MAIN_SCREEN, (255, 255, 255), True, self._dots[1:], 5)
