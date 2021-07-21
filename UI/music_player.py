from obj_properties.rect_form import Rectangle
from settings.screen_size import X_SCALE, Y_SCALE
from settings.window_settings import MAIN_SCREEN
from common_things.sound_loader import GLOBAL_MUSIC_PLAYER
from common_things.global_mouse import GLOBAL_MOUSE
from UI.UI_base.animation import Animation
from UI.UI_base.button_UI import Button
from UI.UI_base.progress_bar_UI import Progress_Bar
from UI.UI_base.text_UI import Text
from pygame import SRCALPHA, Surface


class MusicPlayer(Rectangle):

    def __init__(self, x, y,
                 size_x=None, size_y=None,
                 background_color=(0, 0, 0, 120),  # r, g, b, t
                 transparent=0, ):

        size_x = int(size_x * X_SCALE)
        size_y = int(size_y * Y_SCALE)
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self._player = GLOBAL_MUSIC_PLAYER
        self._surface = self.get_surface()

        self._current_song = self._player.current_song
        self._text = Text(text=self._current_song, screen=self._surface)
        # --------- BACKGROUND ------------------
        self._background_t = transparent
        self._background_color = background_color

    def update(self):
        c_song = self._player.current_song
        if self._current_song != c_song:
            self._surface.fill(self._background_color)
            self._text = Text(text=c_song, screen=self._surface)
            self._current_song = c_song

        if self.collide_point(GLOBAL_MOUSE.pos):
          pass

    def get_surface(self, size=None, transparent=None, back_color=None):
        flags = 0
        transparent = transparent if transparent else self._background_t
        color = back_color if back_color else self._background_color
        size = size if size else (self.size_x, self.size_y)
        if transparent:
            flags = SRCALPHA

        surface = Surface(size, flags, 16)
        if color:
            surface.fill(color)

        surface.convert_alpha()

        return surface

    def draw(self):
        MAIN_SCREEN.blit(self._surface, (self.x0, self.y0))
