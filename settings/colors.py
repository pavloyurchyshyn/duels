from pygame import Color

EMPTY = Color(0, 0, 0, 0)
HALF_EMPTY = Color(0, 0, 0, 150)
HALF_EMPTY_L = Color(0, 0, 0, 50)

BLUE = [0, 0, 255]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
DARK_GREEN = [0, 55, 0]
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GREY = [169, 169, 169]
GREY_WHITE = [190, 190, 190]
GREY_DARK = [130, 130, 130]
GREY_DARK_2 = [70, 70, 70]
GREY_DARK_3 = [20, 20, 20]
GREY_GREEN = [160, 255, 160]
GREY_BLUE = [130, 130, 225]
GREY_RED = [255, 130, 130]
UMBRA = [115, 74, 18]
ORANGE = [255, 150, 100]
WHITE_BLUE = [0, 255, 255]
YELLOW = [255, 255, 0]

GOLD = [255, 223, 0]
SILVER = [192, 192, 192]

BULLET_COLOR = [155, 125, 0]

COLORS_DICT = {
    'blue': BLUE,
    'red': RED,
    'green': GREEN,
    'white': WHITE,
    'black': BLACK,
    'grey': GREY_DARK,
    'grey2': GREY_DARK_2,
    'grey3': GREY_DARK_3,
    'yellow': YELLOW

}
simple_colors = COLORS_DICT

BLOOD_COLOR = (75, 0, 0)

PLAYERS_COLORS = {
    'blue': {'body': (181, 244, 253, 255),
             'face': (112, 170, 241)},

    'red': {'body': (237, 121, 126, 255),
            'face': (185, 65, 70, 255)},

    'purple': {'body': (157, 98, 230, 255),
               'face': (125, 45, 223, 255)},

    'green': {'body': (62, 210, 111, 255),
              'face': (27, 114, 55, 255)}
}
