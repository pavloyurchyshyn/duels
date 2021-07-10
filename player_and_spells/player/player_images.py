from settings.players_settings.player_pic_and_anim import PLAYER_SIZE, IDLE_IMAGES,IDLE_TIMES, RAGE_IMAGES, RAGE_TIMES
from settings.colors import PLAYERS_COLORS

from common_things.img_loader import recolor_picture, load_image, load_animation


class PLayerImages:
    # ANIMATIONS =  {'body': load_image('sprites/player/player_image.png',
    #                        size=size,
    #                        redraw_color=body_color),
    #
    #     'idle_animation': load_animation(IDLE_IMAGES, IDLE_TIMES,
    #                                      size=size,
    #                                      redraw_color=face_color),
    #
    #     'other_animation': animation,}

    def __init__(self, size=None):
        self.size = size if size else PLAYER_SIZE
        self.raw_animations = {
            'idle': load_animation(IDLE_TIMES, IDLE_TIMES, size=self.size)

        }

    def change_color(self, color: str or tuple or dict = 'blue', size=None):
        if type(color) is str:
            body_color, face_color = PLAYERS_COLORS.get(color, 'blue').values()
        elif type(color) in (list, tuple):
            body_color, face_color = color
        elif type(color) is dict:
            body_color, face_color = color['body'], color['face']
