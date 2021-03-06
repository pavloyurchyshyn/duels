from settings.players_settings.player_pic_and_anim import *
from settings.colors import PLAYERS_COLORS
from pygame.transform import smoothscale
from common_things.img_loader import recolor_picture, load_image, load_animation


class PlayerImagesManager:
    def __init__(self, size=None, original_size=0, circle_size=None, angle=90):

        self.size = size
        if size:
            self.size = int(self.size)
            self.pic_size = (self.size, self.size) if size else size
            self.circle_size = circle_size if circle_size else (int(self.size * 1.1), int(self.size * 1.1))

        if original_size or size is None:
            self.size = self.pic_size = self.circle_size = None

        self.raw_body = load_image(BODY_IMAGE, size=None, angle=angle)
        self.raw_animations = {
            ANIM_IDLE_K: load_animation(IDLE_IMAGES, IDLE_TIMES, size=None, angle=angle),
            ANIM_RAGE_K: load_animation(RAGE_IMAGES, RAGE_TIMES, size=None, angle=angle),
            ANIM_DEAD_K: load_animation(DEAD_IMAGES, DEAD_TIMES, size=None, angle=angle),
            ANIM_DYING_K: load_animation(DYING_IMAGES, DYING_TIMES, size=None, angle=angle)
        }

        self.raw_animations[ANIM_RAGE_K]['end'] = ANIM_IDLE_K
        self.raw_animations[ANIM_DYING_K]['end'] = ANIM_DEAD_K
        self.raw_animations[ANIM_DEAD_K]['end'] = ANIM_DEAD_K
        self.under_player_circle = load_image(CIRCLE_IMAGE, size=self.circle_size)

    def get_new_skin(self, colors: str or tuple or dict = 'blue'):
        if type(colors) is str:
            body_color, face_color = PLAYERS_COLORS.get(colors, 'blue').values()
        elif type(colors) in (list, tuple):
            body_color, face_color = colors
        elif type(colors) is dict:
            body_color, face_color = colors['body'], colors['face']

        return {
            'body': recolor_picture(smoothscale(self.raw_body.copy(), self.pic_size), body_color),
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
                new_animation[frame_num] = {'frame': smoothscale(recolor_picture(frame, color), self.pic_size),
                                            'cd': animation[frame_num]['cd']}
        return new_animation

    def get_circle(self, color=(255, 110, 110)):
        return recolor_picture(self.under_player_circle.copy(), color)


NORMAL_PLAYER_IMGS = PlayerImagesManager()
