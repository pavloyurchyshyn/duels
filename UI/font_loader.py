from pygame import font
from settings.screen_size import X_SCALE


def custom_font_size(size: int, font_name='Arial'):
    return font.SysFont(font_name, size)


DEFAULT_FONT_SIZE = int(25 * X_SCALE)
DEFAULT_FONT = font.SysFont('Arial', DEFAULT_FONT_SIZE)
