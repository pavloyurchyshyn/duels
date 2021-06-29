from UI.UI_base.text_UI import Text

from obj_properties.rect_form import Rectangle
from common_things.global_mouse import GLOBAL_MOUSE
from common_things.global_keyboard import GLOBAL_KEYBOARD
from common_things.global_clock import GLOBAL_CLOCK
from common_things.font_loader import DEFAULT_FONT_SIZE


from settings.window_settings import MAIN_SCREEN
from settings.colors import YELLOW, WHITE, GREY
from settings.global_parameters import GLOBAL_SETTINGS
from pygame import draw, Surface
from pygame.constants import SRCALPHA


from settings.UI_setings.button_settings import DEFAULT_BUTTON_X_SIZE, DEFAULT_BUTTON_Y_SIZE, DEFAULT_BORDER_WIDTH


class InputElement(Rectangle):
    INPUT_DELAY = 0.1
    DEF_X_SIZE = DEFAULT_BUTTON_X_SIZE
    DEF_Y_SIZE = DEFAULT_BUTTON_Y_SIZE

    def __init__(self, x, y, size_x=DEF_X_SIZE, size_y=DEF_Y_SIZE,
                 surface=None,
                 text='',
                 default_text='',
                 background_color=(0, 0, 0, 120),  # r, g, b, t
                 transparent=1,
                 focused_border_color=WHITE,
                 unfocused_border_color=GREY,
                 active=1,
                 autobuild=1,
                 text_active_color=WHITE,
                 text_non_active_color=GREY,
                 text_size=DEFAULT_FONT_SIZE,
                 active_border_width=DEFAULT_BORDER_WIDTH,
                 active_border_color=WHITE,
                 non_active_border_width=DEFAULT_BORDER_WIDTH,
                 non_active_border_color=GREY,

                 on_change_action=None,
                 ):
        super().__init__(x, y, size_x, size_y)
        self._mouse = GLOBAL_MOUSE
        self._key = GLOBAL_KEYBOARD

        self._default_text = default_text
        self._first_enter = 1

        self._text_text = text if text else default_text
        self._r_text_active = None
        self._text_active_color = text_active_color
        self._r_text_non_active = None
        self._text_non_active_color = text_non_active_color

        self._text_size = text_size

        self._focused = 0

        self._clock = GLOBAL_CLOCK
        self._next_input = -1

        # --------- BACKGROUND ------------------
        self._background_t = transparent
        self._background_color = background_color

        self._surface = surface if surface else MAIN_SCREEN

        self._active_text_surface = self.get_surface()
        self._non_active_text_surface = self.get_surface()

        self._focused_b_color = focused_border_color
        self._unfocused_b_color = unfocused_border_color

        self.active = active

        self._active_border_w = active_border_width
        self._active_border_color = active_border_color
        self._non_active_border_w = non_active_border_width
        self._non_active_border_color = non_active_border_color

        self._surface_to_draw = self.get_surface()
        self._border = self._surface_to_draw.get_rect()

        self._on_change_action = on_change_action

        if autobuild:
            self.build()

    def update(self):
        if self._mouse.lmb:
            if self.collide_point(self._mouse.pos):
                self._focused = 1
            else:
                self._focused = 0
                if not self._text_text:
                    self.set_default_text()
                    self.build()

        if self._focused:
            prev_text = self._text_text
            add_text = self._key.text
            if prev_text == self._default_text and self._first_enter:
                self._text_text = ''
                self._first_enter = 0

            if add_text and prev_text.endswith(add_text[:0]):
                if self._clock.time > self._next_input:
                    self._next_input = self._clock.time + self.INPUT_DELAY
                    self._text_text = f'{self._text_text}{add_text}'
            else:
                self._text_text = f'{self._text_text}{add_text}'

            if self._key.BACKSPACE:
                if self._clock.time > self._next_input:
                    self._next_input = self._clock.time + self.INPUT_DELAY
                    self._text_text = self._text_text[:-1]

            if self._key.ENTER or self._key.ESC:
                self._focused = 0
                self.set_default_text()

            if prev_text != self._text_text:
                if self._on_change_action:
                    self._on_change_action()
                self.build()

    def set_default_text(self):
        if not self._text_text:
            self._text_text = self._default_text
            self._first_enter = 1

    def draw(self, dx=0, dy=0):
        self._surface_to_draw.fill(self._background_color)
        if self.active:
            self._surface_to_draw.blit(self._active_text_surface, (0, 0))
        else:
            self._surface_to_draw.blit(self._non_active_text_surface, (0, 0))

        if self._focused:
            draw.rect(self._surface_to_draw, self._active_border_color, self._border, self._active_border_w)
        else:
            draw.rect(self._surface_to_draw, self._non_active_border_color, self._border, self._non_active_border_w)

        MAIN_SCREEN.blit(self._surface_to_draw, (self.x0, self.y0))

        if GLOBAL_SETTINGS['test_draw']:
            for dot in self._dots:
                draw.circle(MAIN_SCREEN, YELLOW, (dot[0] + dx, dot[1] + dy), 1)

    def build(self):
        self._active_text_surface.fill(self._background_color)
        self._non_active_text_surface.fill(self._background_color)

        self._r_text_active = Text(text=self._text_text,
                                   screen=self._active_text_surface,
                                   color=self._text_active_color,
                                   size=self._text_size)
        self._r_text_non_active = Text(text=self._text_text,
                                       screen=self._non_active_text_surface,
                                       color=self._text_non_active_color,
                                       size=self._text_size)

        self._r_text_active.draw()
        self._r_text_non_active.draw()

    @property
    def text(self):
        if self._text_text == self._default_text:
            return ''
        else:
            return self._text_text

    @text.setter
    def text(self, new_text):
        self._text_text = new_text
        self.build()

    def get_surface(self):
        flags = 0
        if self._background_t:
            flags = SRCALPHA

        surface = Surface((self.size_x, self.size_y), flags, 32)
        if self._background_color:
            surface.fill(self._background_color)

        surface.convert_alpha()

        return surface
