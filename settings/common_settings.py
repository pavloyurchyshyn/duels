from pygame import font
VERSION = '0.0.1'

FPS = 64


def custom_font_size(size: int):
    return font.SysFont('Arial', size)


DEFAULT_FONT_SIZE = 25
DEFAULT_FONT = font.SysFont('Arial', DEFAULT_FONT_SIZE)