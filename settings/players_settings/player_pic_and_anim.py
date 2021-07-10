from common_things.img_loader import load_image, load_animation
from settings.colors import PLAYERS_COLORS
from settings.players_settings.player_settings import PLAYER_SIZE

PLAYER_SIZE = PLAYER_SIZE * 2

IDLE_IMAGES = ['sprites/player/idle/idle_0.png', 'sprites/player/idle/idle_1.png',
                 'sprites/player/idle/idle_2.png', 'sprites/player/idle/idle_3.png']
IDLE_TIMES = [1.5, 0.2, 0.2, 0.2]

RAGE_IMAGES = ['sprites/player/rage/rage_0.png', 'sprites/player/rage/rage_1.png',
                 'sprites/player/rage/rage_2.png', 'sprites/player/rage/rage_3.png',
                 'sprites/player/rage/rage_4.png', 'sprites/player/rage/rage_5.png', ]
RAGE_TIMES = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, ]

ANIM_RAGE_K = 'rage'
ANIM_IDLE_K = 'idle'


# ---------------------------------------------------------------
def get_sprite_and_animations(color: str or tuple or dict = 'blue', size=None):
    if type(color) is str:
        body_color, face_color = PLAYERS_COLORS.get(color, 'blue').values()
    elif type(color) in (list, tuple):
        body_color, face_color = color
    elif type(color) is dict:
        body_color, face_color = color['body'], color['face']

    size = size if size else (PLAYER_SIZE, PLAYER_SIZE)

    animation = {
        ANIM_RAGE_K: load_animation(RAGE_IMAGES, RAGE_TIMES, size=size,
                                    redraw_color=face_color)
    }
    animation[ANIM_RAGE_K]['end'] = ANIM_IDLE_K

    return {
        'body': load_image('sprites/player/player_image.png',
                           size=size,
                           redraw_color=body_color),

        'idle_animation': load_animation(IDLE_IMAGES, IDLE_TIMES,
                                         size=size,
                                         redraw_color=face_color),

        'other_animation': animation,
        # 'scaled_body': load_image('sprites/player/player_image.png', size=(PLAYER_SIZE * SCALE, PLAYER_SIZE * SCALE))
    }
