from settings.window_settings import MAIN_SCREEN, HALF_SCREEN_H, SCREEN_W
from settings.colors import simple_colors, EMPTY
from settings.common_settings import DEFAULT_FONT
from pygame import draw
from pygame import Rect


class Progress_Bar:
    MAIN_SCREEN = MAIN_SCREEN
    BAR_X_SIZE = 1200
    BAR_Y_SIZE = 10

    def __init__(self, screen=None, stage=0, stages_num=1,
                 text=None, text_color=(255, 255, 255),
                 bar_pos: (int, int) = None,
                 bar_inner_color=(255, 255, 255),
                 bar_x_size: int = BAR_X_SIZE,
                 bar_y_size: int = BAR_Y_SIZE,
                 text_pos: (int, int) = None):

        self._current_stage = stage
        self.stages_num = stages_num

        self.screen = screen if screen else Progress_Bar.MAIN_SCREEN
        self.percent = 0

        self._message = text

        self.border_color = simple_colors['white']
        self.bar_color = bar_inner_color
        self.x_size = bar_x_size
        self.y_size = bar_y_size

        # =========== text ===================
        self._text = None
        self._text_color = text_color

        if self._message:
            self._render_text()

        self.bar_position = ((SCREEN_W - self.x_size) // 2, HALF_SCREEN_H) if bar_pos is None else bar_pos

        if text_pos:
            self.text_position = text_pos
        else:
            self.text_position = self.bar_position[0], self.bar_position[1] + self.y_size * 2
        # ======================================

        self.borders_rect = Rect(self.bar_position[0] - 5,
                                 self.bar_position[1] - 9,
                                 self.x_size + 10,
                                 self.y_size + 10)

    def _get_percent(self):
        self.percent = round(self._current_stage / self.stages_num * 100, 2)

    def _render_text(self):
        self._text = DEFAULT_FONT.render(self._message, 1, self._text_color)

    def _bar_endpos(self):
        endpos = (int(self.bar_position[0] + self.x_size * (self._current_stage / self.stages_num)),
                  self.bar_position[1])

        return endpos

    def update(self, current_stage=None, text=None, stages_num=None, text_pos=None, bar_pos=None, bar_color=None):
        if text_pos:
            self.text_position = text_pos

        if bar_color:
            self.bar_color = bar_color

        if bar_pos:
            self.bar_position = bar_pos

        if stages_num is not None:
            self.stages_num = stages_num

        if current_stage is None:
            self._current_stage += 1
        else:
            self._current_stage = current_stage

        self._get_percent()

        if text:
            self._message = str(text)
            self._render_text()
        else:
            self._text = None

    def draw(self, dx=0, dy=0):
        if self.screen and self.screen != self.MAIN_SCREEN:
            self.screen.fill(EMPTY)

        # BORDER
        draw.rect(surface=self.screen,
                  color=self.border_color,
                  rect=self.borders_rect,
                  width=1)

        # BAR
        if self._current_stage > 0:
            draw.line(surface=self.screen,
                      color=self.bar_color,
                      start_pos=self.bar_position,
                      end_pos=self._bar_endpos(),
                      width=self.y_size)

        if self._text:
            self.screen.blit(self._text, self.text_position)

        if self.screen and self.screen != self.MAIN_SCREEN:
            MAIN_SCREEN.blit(self.screen, (0, 0))
