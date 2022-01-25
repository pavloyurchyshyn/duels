from obj_properties.rect_form import Rectangle
from settings.screen_size import X_SCALE, Y_SCALE
from settings.window_settings import MAIN_SCREEN
from common_things.sound_loader import GLOBAL_MUSIC_PLAYER
from common_things.sprites_functions import get_surface
from common_things.global_mouse import GLOBAL_MOUSE
from UI.UI_base.progress_bar_UI import ProgressBar
from UI.UI_base.button_UI import Button
from pygame.draw import rect as draw_rect
from pygame.draw import circle as draw_circle
from UI.font_loader import custom_font_size
from common_things.global_clock import GLOBAL_CLOCK
from math import cos
from settings.colors import WHITE


class MusicPlayerUI(Rectangle):

    def __init__(self, x, y,
                 size_x=300, size_y=100,
                 background_color=(150, 50, 255, 150),  # r, g, b, t
                 ):
        size_x = int(size_x * X_SCALE)
        size_y = int(size_y * Y_SCALE)
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self._player = GLOBAL_MUSIC_PLAYER
        self._surface = get_surface(self.size_x, self.size_y, transparent=1)

        self._current_song = self._player.current_song

        self._background_color = background_color

        step = self.size_x // 15
        self._step_from_border = step
        self._progress_bar = ProgressBar(bar_pos=(self.x0 + step, self.y0 + step // 2),
                                         bar_x_size=self.size_x - step - step,
                                         stages_num=100)

        self._text_font = custom_font_size(int(18 * X_SCALE))
        self._text = self._text_font.render('', 1, (255, 255, 255))
        self._player_rect = self.get_rect()
        self._text_rect = [0, 0, self.size_x * 0.75, self.size_y // 4]
        self._text_position = [self.x0 + step, self.y0 + self.size_y // 3]

        draw_rect(self._surface, self._background_color,
                  (0, 0, self._surface.get_width(), self._surface.get_height()),
                  0, 5)

        self._music_length_text_font = custom_font_size(int(15 * X_SCALE))
        self._music_length_text = self._music_length_text_font.render(
            self._player.song_length if self._player.busy() else '0:00', 1, (255, 255, 255))
        self._music_length_text_pos = [self.x1 - step - self._music_length_text.get_width(),
                                       self.y0 + step // 2 + self._progress_bar.y_size]

        self._current_song_pos_text = self._music_length_text_font.render(
            self._player.get_music_pos() if self._player.busy() else '0:00', 1, (255, 255, 255))
        self._current_song_pos_text_pos = [self.x0 + step,
                                           self.y0 + step // 2 + self._progress_bar.y_size]

        self._sin_pos = 0

        self._move_song_name = 0

        button_x_size = self.size_x // 9
        button_y_size = self.size_x // 15
        self._hide_button = Button(self.x1 - button_x_size * 1.5, self.y1,
                                   size_x=button_x_size,
                                   size_y=button_y_size,
                                   border_width=1,
                                   text='▲',
                                   background_color=self._background_color,
                                   on_click_action=self._hide_show_func,
                                   non_active_after_click=0,
                                   visible=1, active=1, transparent=1,
                                   border_parameters={'border_bottom_left_radius': 3,
                                                      'border_bottom_right_radius': 3})
        self._hide_button.build()

        button_x_size = self.size_x // 3
        button_y_size = self.size_x // 12
        self._show_button = Button(self.x1 - button_x_size * 1.5, self.y0,
                                   size_x=button_x_size,
                                   size_y=button_y_size,
                                   text_size=12 * X_SCALE,
                                   border_width=1,
                                   text='Show player ▼',
                                   background_color=self._background_color,
                                   on_click_action=self._hide_show_func,
                                   non_active_after_click=0,
                                   visible=1, active=1, transparent=1,
                                   border_parameters={'border_bottom_left_radius': 3,
                                                      'border_bottom_right_radius': 3})
        self._show_button.build()

        self._hidden = self._player.muted

        pause_button_x_size = 50 * X_SCALE
        pause_button_y_size = self._text_rect[3]
        self._pause_button = Button(x=self.x0 + self.size_x // 2 - pause_button_x_size // 2,
                                    y=self._text_position[1] + self._text_rect[3],
                                    size_x=pause_button_x_size,
                                    size_y=pause_button_y_size,
                                    active=not self._player.busy(),
                                    on_click_action=self.pause_unpause_music,
                                    text='||', change_after_click=1,
                                    non_active_text='>', text_non_active_color=(255, 255, 255),
                                    border_width=0, border_color=(255, 255, 255),
                                    border_non_active_color=(255, 255, 255),
                                    border_parameters={'border_radius': 1},
                                    click_anim_dur=-1,
                                    transparent=1,
                                    background_color=(0, 0, 0, 0), )

        self._next_button = Button(x=self._pause_button.x1 + self._pause_button.size_x + step,
                                   y=self._pause_button.y0, on_click_action=self._player.play_next,
                                   text='>>', size_x=pause_button_x_size, size_y=pause_button_y_size,
                                   border_width=0, click_anim_dur=-1,
                                   transparent=1, background_color=(0, 0, 0, 0))

        self._mute_unmute_button = Button(x=self.x0 + step, y=self._next_button.y0,
                                          text='X', text_color=(100, 100, 100),
                                          non_active_text='X', click_anim_dur=-1,
                                          on_click_action=self.mute_unmute_func,
                                          size_x=pause_button_x_size, size_y=pause_button_y_size,
                                          change_after_click=1, border_width=0, active_pic=not GLOBAL_MUSIC_PLAYER.muted,
                                          transparent=1, background_color=(0, 0, 0, 0),
                                          border_non_active_color=WHITE,
                                          text_non_active_color=WHITE, )

    def mute_unmute_func(self):
        if GLOBAL_MUSIC_PLAYER.muted:
            GLOBAL_MUSIC_PLAYER.unmute()
        else:
            GLOBAL_MUSIC_PLAYER.mute()

    def pause_unpause_music(self):
        self._player.pause_unpause_music()

    def _hide_show_func(self):
        self._hidden = not self._hidden

    def update(self):
        mus_pos = self._player.get_music_pos()
        mus_len = self._player.song_length

        if not self._hidden:
            if mus_len and mus_pos:
                self._progress_bar.update(current_stage=mus_pos / mus_len * 100)

            if self._current_song != self._player.current_song:
                self._current_song = self._player.current_song
                self._text = self._text_font.render(self._current_song.replace('.wav', ''), 1, (255, 255, 255))
                self._text_rect[0] = 0
                self._move_song_name = self._text_rect[2] < self._text.get_width()

                self._music_length_text = self._music_length_text_font.render(
                    f'{int(mus_len // 60)}:{int(mus_len % 60)}' if self._player.busy() else '0:00', 1, (255, 255, 255))
                self._music_length_text_pos = [self.x1 - self._step_from_border - self._music_length_text.get_width(),
                                               self.y0 + self._step_from_border // 2 + self._progress_bar.y_size]

            if self._move_song_name:
                self._sin_pos += GLOBAL_CLOCK.d_time * 0.3
                s = cos(self._sin_pos)
                self._text_rect[0] = (s if s > 0 else 0) * self._text.get_width() // 2

            if self._player.busy():
                self._current_song_pos_text = self._music_length_text_font.render(
                    f'{int(mus_pos // 60)}:{"0" + str(int(mus_pos % 60)) if mus_pos % 60 < 10 else int(mus_pos % 60)}' if self._player.busy() else '0:00',
                    1, (255, 255, 255))

        if GLOBAL_MOUSE.lmb:
            m_pos = GLOBAL_MOUSE.pos
            if self._hidden:
                self._show_button.update()
                self._show_button.click(m_pos)
            else:
                for button in (self._hide_button, self._pause_button, self._next_button, self._mute_unmute_button):
                    button.update()
                    button.click(m_pos)

    def draw(self):
        if self._hidden:
            self._show_button.draw()

        else:
            MAIN_SCREEN.blit(self._surface, (self.x0, self.y0))
            self._progress_bar.draw()

            draw_rect(MAIN_SCREEN, (255, 255, 255), self._player_rect, 1, 5)
            MAIN_SCREEN.blit(self._text, self._text_position, self._text_rect)

            MAIN_SCREEN.blit(self._music_length_text, self._music_length_text_pos)
            MAIN_SCREEN.blit(self._current_song_pos_text, self._current_song_pos_text_pos)

            draw_circle(MAIN_SCREEN, (255, 0, 0), (self._text_rect[0], self._text_rect[1]), 2)

            self._hide_button.draw()
            self._pause_button.draw()
            self._next_button.draw()
            self._mute_unmute_button.draw()
