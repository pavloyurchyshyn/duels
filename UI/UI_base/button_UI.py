from obj_properties.rect_form import Rectangle

from pygame import transform, Surface, mouse
from pygame.draw import rect as DrawRect
from pygame.constants import SRCALPHA
from pygame import draw

from UI.UI_base.text_UI import Text
from common_things.global_clock import GLOBAL_CLOCK

from settings.UI_setings.button_settings import DEFAULT_BUTTON_X_SIZE, \
    DEFAULT_BUTTON_Y_SIZE, DEFAULT_CLICK_DELAY, DEFAULT_BORDER_WIDTH, CLICK_ANIMATION_DURATION
from settings.colors import simple_colors
from settings.global_parameters import GLOBAL_SETTINGS
from settings.common_settings import DEFAULT_FONT_SIZE
from settings.window_settings import MAIN_SCREEN


class Button(Rectangle):
    HELP_TEXT_TIME = 3
    BUTTON_X_SIZE = DEFAULT_BUTTON_X_SIZE
    BUTTON_Y_SIZE = DEFAULT_BUTTON_Y_SIZE
    CLICK_DELAY = DEFAULT_CLICK_DELAY
    CLOCK = GLOBAL_CLOCK
    MAIN_SCREEN = MAIN_SCREEN

    CLICK_ANIMATION_DUR = CLICK_ANIMATION_DURATION

    def __init__(self, x: int, y: int,
                 screen,

                 size_x: int = 0, size_y: int = 0,

                 text: str = '',
                 non_active_text=None,
                 text_x=None, text_y=None,
                 change_after_click=0,
                 text_color=simple_colors['white'],
                 text_non_active_color=simple_colors['grey'],
                 text_size=None,

                 active=True,
                 active_pic=None,

                 on_click_action=None,
                 on_click_action_args: tuple = (),
                 on_click_action_kwargs: dict = {},
                 return_action_value=0,

                 non_active_after_click=0,
                 visible=1,
                 non_visible_after_click=0,

                 picture=None,
                 pic_x=0, pic_y=0,

                 border_color=simple_colors['white'],
                 border_width=DEFAULT_BORDER_WIDTH,
                 border_non_active_color=simple_colors['grey'],

                 background_color=(0, 0, 0, 120),  # r, g, b, t
                 transparent=0,

                 click_delay=1,
                 time_b_click=None,
                 **kwargs):

        size_x = size_x if size_x else Button.BUTTON_X_SIZE
        size_y = size_y if size_y else Button.BUTTON_Y_SIZE
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)
        self.x = x
        self.y = y

        self.on_click_action = on_click_action
        self.on_click_args = on_click_action_args
        self.on_click_kwargs = on_click_action_kwargs

        self._active = active
        self._visible = visible

        self._change_after_click = change_after_click

        # ---------- TEXT ----------------------
        self._text_text = text
        self._non_active_text_text = non_active_text if non_active_text else text
        self._original_text_size = text_size if text_size else DEFAULT_FONT_SIZE
        self._text_size = self._original_text_size
        self._text_x, self._text_y = text_x, text_y

        self._active_text_color = text_color
        self._inactive_text_color = text_non_active_color

        self._active_text = None
        self._non_active_text = None

        self._active_text_img = None
        self._non_active_text_img = None

        # ---------- BORDER ---------------------
        self._border = None
        self._border_active_color = border_color
        self._border_non_active_color = border_non_active_color
        self._border_width = border_width

        # --------- BACKGROUND ------------------
        self._background_t = transparent
        self._background_color = background_color

        # ---------- CLICK ----------------------
        self._on_click_action = on_click_action
        self._return_action = return_action_value

        self._non_active_after_click = non_active_after_click
        self._non_visible_after_click = non_visible_after_click

        # ------ PICTURE ------------
        self._picture = picture
        if self._picture:
            self.__scale_picture()
        self._pic_x, self._pic_y = pic_x, pic_y

        # ---------- FINAL PREPARE ---------
        self._screen = screen
        self._button_surface = None  # surface of button for drawing
        self._r_active_button = None
        self._r_non_active_button = None
        self.build()

        if active_pic is None:
            self._current_button_pic = self._r_active_button if active else self._r_non_active_button
        else:
            self._current_button_pic = self._r_active_button if active_pic else self._r_non_active_button

        self._next_click_time = -1
        self._click_with_delay = click_delay
        self._time_b_click = time_b_click if time_b_click is not None else Button.CLICK_DELAY

        self._clicked = False
        self._value = None

        self._animation_finish_time = 0
        self._clicked_border = self.get_surface(1, (0, 0, 0, 0))

        DrawRect(self._clicked_border, self._border_active_color, self._clicked_border.get_rect(),
                 int(self._border_width * 2))

    def build(self, k=1):
        self._button_surface = self.get_surface()  # surface of button for drawing

        self._border = self._button_surface.get_rect()

        active_button_s = self.get_surface()  # create background surface
        non_active_button_s = self.get_surface()

        active_button_s.fill(self._background_color)  # fill background surface
        non_active_button_s.fill(self._background_color)
        self._text_size = self._text_size * k if self._text_size * k >= 1 else self._text_size

        if len(self._text_text) > 0:
            # render text
            self._active_text = Text(text=self._text_text,
                                     screen=active_button_s,
                                     x=self._text_x, y=self._text_y,
                                     color=self._active_text_color,
                                     size=self._text_size)
            self._active_text.draw()  # draw on surface

            self._non_active_text = Text(text=self._non_active_text_text,
                                         screen=non_active_button_s,
                                         x=self._text_x, y=self._text_y,
                                         color=self._inactive_text_color,
                                         size=self._text_size)
            self._non_active_text.draw()

        if self._border_width > 0:
            DrawRect(active_button_s, color=self._border_active_color,
                     rect=self._border, width=self._border_width)

            DrawRect(non_active_button_s, color=self._border_non_active_color,
                     rect=self._border, width=self._border_width)

        self._r_active_button = active_button_s  # should be created button picture
        self._r_active_button.convert_alpha()

        self._r_non_active_button = non_active_button_s  # should be created button picture
        self._r_non_active_button.convert_alpha()

    def make_original_size(self):
        self._make_original_size()
        self._text_size = self._original_text_size
        self.build()

    def scale(self, k):
        self._scale(k)
        self.build(k)
        if self._picture:
            self.__scale_picture()

    def __scale_picture(self):
        xs, ys = self._picture.get_size()
        if xs > self.size_x or ys > self.size_y:
            if xs > ys:
                k = xs / ys
                self._picture = transform.scale(self._picture, (int(self.size_x), int(self.size_y * k)))
            else:
                k = ys / xs
                self._picture = transform.scale(self._picture, (int(self.size_x * k), int(self.size_y)))

    def set_screen(self, screen):
        self._screen = screen

    def click(self, xy, *args, **kwargs):
        if self._active and self.collide_point(xy):
            self._clicked = 1

            if self._click_with_delay:
                time = Button.CLOCK.time
                if self._next_click_time < time:
                    self._next_click_time = time + self._time_b_click
                else:
                    return 0

            self._animation_finish_time = Button.CLOCK.time + self.CLICK_ANIMATION_DUR

            if self._non_active_after_click:
                self._current_button_pic = self._r_non_active_button
                self._active = 0

            if self._non_visible_after_click:
                self._visible = 0

            if self._on_click_action:
                self._value = self._on_click_action(*self.on_click_args, *args, **self.on_click_kwargs, **kwargs)

            if self._change_after_click:
                self.change_picture()
            else:
                self._current_button_pic = self._r_active_button if self._active else self._r_non_active_button

            return 1

    def activate_click(self, *args, **kwargs):
        self.click(self._center, *args, **kwargs)

    def change_picture(self, active=None):
        if active == 1:
            self._current_button_pic = self._r_active_button
        elif active == 0:
            self._current_button_pic = self._r_non_active_button
        else:
            self._current_button_pic = self._r_active_button if self._current_button_pic == self._r_non_active_button else self._r_non_active_button

    def draw(self, dx=0, dy=0):
        self._draw(dx, dy)

    def _draw(self, dx=0, dy=0):
        if self._visible:
            if self._picture:
                self._screen.blit(self._picture, (self._pic_x + dx, self._pic_y + dy))

            self._screen.blit(self._current_button_pic, (self.x0 + dx, self.y0 + dy))
            if self.CLOCK.time < self._animation_finish_time:
                self._screen.blit(self._clicked_border, (self.x0 + dx, self.y0 + dy))

            # if self._active:
            #     self._screen.blit(self._r_active_button, (self.x0 + dx, self.y0 + dy))
            # else:
            #     self._screen.blit(self._r_non_active_button, (self.x0 + dx, self.y0 + dy))

            if GLOBAL_SETTINGS['test_draw']:
                color = simple_colors['yellow']
                for dotx, doty in self._dots[1:]:
                    draw.circle(Button.MAIN_SCREEN, color, (dotx + dx, doty + dy), 2)

    def update(self):
        self._update()

    def _update(self):
        self._clicked = 0
        self._value = None

    def get_surface(self, transparent=None, back_color=None):
        flags = 0
        transparent = transparent if transparent else self._background_t
        color = back_color if back_color else self._background_color

        if transparent:
            flags = SRCALPHA

        surface = Surface((self.size_x, self.size_y), flags, 32)
        if color:
            surface.fill(color)

        surface.convert_alpha()

        return surface

    def set_active_text(self, text):
        self._text_text = text
        self.build()

    def set_non_active_text(self, text):
        self._non_active_text_text = text
        self.build()

    def set_text_size(self, size):
        self._text_size = size
        self.build()

    def make_visible(self):
        self._visible = 1

    def make_invisible(self):
        self._visible = 0

    def make_active(self):
        self.active = 1

    def make_inactive(self):
        self.active = 0

    @property
    def text(self):
        return self._text_text

    @text.setter
    def text(self, message):
        self._text_text = message
        self.build()

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        self._active = value

        if self._change_after_click:
            self._current_button_pic = self._r_active_button if self._current_button_pic == self._r_non_active_button else self._r_non_active_button
        else:
            self._current_button_pic = self._r_active_button if self._active else self._r_non_active_button

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def rect(self):
        return self._button_surface.get_rect()

    @property
    def size(self):
        return self.size_x, self.size_y

    @property
    def height(self):
        return self.size_y

    @property
    def width(self):
        return self.size_x

    @property
    def clicked(self):
        return self._clicked

    @property
    def is_active(self):
        return self._active

    @property
    def is_visible(self):
        return self._visible

    def __str__(self):
        return f'Button {self._text_text}'
