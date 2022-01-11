import ctypes


DEFAULT_SCREEN_SIZE = 1920, 1080

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
SCREEN_W, SCREEN_H = screensize

SCREEN_W = 1870
SCREEN_H = 980
X_SCALE = SCREEN_W / DEFAULT_SCREEN_SIZE[0]
Y_SCALE = SCREEN_H / DEFAULT_SCREEN_SIZE[1]
GAME_SCALE = (X_SCALE + Y_SCALE)/2

HALF_SCREEN_W, HALF_SCREEN_H = SCREEN_W // 2, SCREEN_H // 2

# print("SCALE", X_SCALE, Y_SCALE)
