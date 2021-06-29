from common_things.img_loader import load_image, load_animation
from settings.colors import PLAYERS_COLORS
from settings.players_settings.player_settings import PLAYER_SIZE

PLAYER_SIZE = PLAYER_SIZE * 2

__idle_images = ['sprites/player/idle/idle_0.png', 'sprites/player/idle/idle_1.png',
                 'sprites/player/idle/idle_2.png', 'sprites/player/idle/idle_3.png']
__idle_times = [1.5, 0.2, 0.2, 0.2]

__rage_images = ['sprites/player/rage/rage_0.png', 'sprites/player/rage/rage_1.png',
                 'sprites/player/rage/rage_2.png', 'sprites/player/rage/rage_3.png',
                 'sprites/player/rage/rage_4.png', 'sprites/player/rage/rage_5.png', ]
__rage_times = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, ]

ANIM_RAGE_K = 'rage'
ANIM_IDLE_K = 'idle'


# ---------------------------------------------------------------
def get_sprite_and_animations(color: str = 'blue'):
    body_color, face_color = PLAYERS_COLORS[color].values()

    animation = {
        ANIM_RAGE_K: load_animation(__rage_images, __rage_times, size=(PLAYER_SIZE, PLAYER_SIZE), redraw_color=face_color)
    }
    animation[ANIM_RAGE_K]['end'] = ANIM_IDLE_K

    return {
        'body': load_image('sprites/player/player_image.png',
                           size=(PLAYER_SIZE, PLAYER_SIZE),
                           redraw_color=body_color),

        'idle_animation': load_animation(__idle_images, __idle_times,
                                         size=(PLAYER_SIZE, PLAYER_SIZE),
                                         redraw_color=face_color),

        'other_animation': animation,
        # 'scaled_body': load_image('sprites/player/player_image.png', size=(PLAYER_SIZE * SCALE, PLAYER_SIZE * SCALE))
    }
