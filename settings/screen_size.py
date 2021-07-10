import ctypes

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
SCREEN_W, SCREEN_H = screensize
HALF_SCREEN_W, HALF_SCREEN_H = SCREEN_W//2, SCREEN_H//2