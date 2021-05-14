from pygame import display, Surface, SRCALPHA
from pygame.locals import *
import ctypes

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
SCREEN_W, SCREEN_H = screensize
HALF_SCREEN_W, HALF_SCREEN_H = SCREEN_W//2, SCREEN_H//2

# SCREEN_W, SCREEN_H = display.get_window_size()

flags = FULLSCREEN | DOUBLEBUF | HWACCEL

MAIN_SCREEN = display.set_mode((SCREEN_W, SCREEN_H), flags, 32)
MAIN_SCREEN.set_alpha(None)  # main screen of all game
MAIN_SCREEN_RECT = MAIN_SCREEN.get_rect()

MAIN_T_SCREEN = Surface(screensize, flags, 32)
MAIN_T_SCREEN.fill((0, 0, 0, 125))
MAIN_T_SCREEN.convert_alpha()