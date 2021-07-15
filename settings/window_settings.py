from pygame import display, Surface, SRCALPHA
from pygame.locals import *
from settings.screen_size import *

# SCREEN_W, SCREEN_H = display.get_window_size()
flags = 0  # DOUBLEBUF | HWACCEL | FULLSCREEN
MAIN_SCREEN_DEF_COLOR = (0, 0, 0)

MAIN_SCREEN = display.set_mode((SCREEN_W, SCREEN_H), flags, 16)
# MAIN_SCREEN.set_alpha(None)  # main screen of all game
MAIN_SCREEN_RECT = MAIN_SCREEN.get_rect()

MAIN_T_SCREEN = Surface(screensize, flags, 32)
MAIN_T_SCREEN.fill((0, 0, 0, 125))
MAIN_T_SCREEN.convert_alpha()
