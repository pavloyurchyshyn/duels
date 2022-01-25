from settings.screen_size import X_SCALE, Y_SCALE
from settings.window_settings import MAIN_SCREEN, HALF_SCREEN_W
from UI.font_loader import DEFAULT_FONT


class ScoresText:
    def __init__(self, scores: dict, position: tuple = (HALF_SCREEN_W, 0)):
        x, y = position
        self._scores = scores
        self._teams = tuple(self._scores.keys())
        self._screen = MAIN_SCREEN

        self._text_img = None
        self._text_font = DEFAULT_FONT
        self._text_pos = [x*X_SCALE, y*Y_SCALE]

        self.update_text()

    def update_text(self):
        self._teams = tuple(self._scores.keys())

        text = ''
        direction = 1
        for team in self._teams:
            if direction:
                text = f'{text} {team} {self._scores[team]} :'
                direction = 0
            else:
                text = f'{text} {team} {self._scores[team]} '
                if self._teams.index(team) != len(self._teams) - 1:
                    text = text + ':'
                direction = 1

        self._text_img = self._text_font.render(text, 1, (255, 255, 255))
        self._text_pos[0] = HALF_SCREEN_W - self._text_img.get_width()//2

    def draw(self):
        self._screen.blit(self._text_img, self._text_pos)


