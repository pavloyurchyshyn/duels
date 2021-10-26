from settings.players_settings.player_pic_and_anim import *
from settings.colors import PLAYERS_COLORS
# from settings.screen_size import GAME_SCALE

from common_things.img_loader import recolor_picture, load_image, load_animation


class PlayerImagesManager:
    def __init__(self, size=None):
        self.size = size if size else PLAYER_SIZE
        self.size = int(self.size)# * GAME_SCALE)
        self.pic_size = (self.size, self.size)

        self.raw_body = load_image(BODY_IMAGE, size=self.pic_size)
        self.raw_animations = {
            ANIM_IDLE_K: load_animation(IDLE_IMAGES, IDLE_TIMES, size=self.pic_size),
            ANIM_RAGE_K: load_animation(RAGE_IMAGES, RAGE_TIMES, size=self.pic_size),
            ANIM_DEAD_K: load_animation(DEAD_IMAGES, DEAD_TIMES, size=self.pic_size),
            ANIM_DYING_K: load_animation(DYING_IMAGES, DYING_TIMES, size=self.pic_size)
        }
        self.raw_animations[ANIM_RAGE_K]['end'] = ANIM_IDLE_K
        self.raw_animations[ANIM_DYING_K]['end'] = ANIM_DEAD_K
        self.raw_animations[ANIM_DEAD_K]['end'] = ANIM_DEAD_K
        self.under_player_circle = load_image(CIRCLE_IMAGE, size=(self.size + 4, self.size + 4))

    def get_new_skin(self, colors: str or tuple or dict = 'blue'):
        if type(colors) is str:
            body_color, face_color = PLAYERS_COLORS.get(colors, 'blue').values()
        elif type(colors) in (list, tuple):
            body_color, face_color = colors
        elif type(colors) is dict:
            body_color, face_color = colors['body'], colors['face']

        return {
            'body': recolor_picture(self.raw_body.copy(), body_color),
            'idle_animation': self.recolor_animation(ANIM_IDLE_K, face_color),
            'other_animation': {
                ANIM_RAGE_K: self.recolor_animation(ANIM_RAGE_K, face_color),
                ANIM_DEAD_K: self.recolor_animation(ANIM_DEAD_K, face_color),
                ANIM_DYING_K: self.recolor_animation(ANIM_DYING_K, face_color)
            }
        }

    def recolor_animation(self, animation_k, color):
        animation = self.raw_animations[animation_k]
        new_animation = {}

        for frame_num in animation:

            if frame_num == 'end':
                new_animation['end'] = animation['end']
            else:
                frame = animation[frame_num]['frame'].copy()
                new_animation[frame_num] = {'frame': recolor_picture(frame, color),
                                            'cd': animation[frame_num]['cd']}
        return new_animation

    def get_circle(self, color=(255, 110, 110)):
        return recolor_picture(self.under_player_circle.copy(), color)


NORMAL_PLAYER_IMGS = PlayerImagesManager()
