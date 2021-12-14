from abc import abstractmethod
from visual.visual_effects_controller import VisualEffectsController
from settings.global_parameters import its_client_instance


class PictureLazyLoadMixin:
    CLIENT = its_client_instance()
    EFFECTS_CON = VisualEffectsController
    LOADED = 0
    DRAW_METHODS_LOADED = 0

    PICTURE_PATH = None
    PICTURE = None
    MAIN_SCREEN = None

    ROTATE = None
    DRAW_LINE = None
    DRAW_LINES = None
    DRAW_CIRCLE = None
    DRAW_POLYGON = None
    DRAW_RECT = None

    def __init__(self, custom_load=None):
        self._lazy_load_picture = custom_load if custom_load else self._lazy_load_picture
        self.draw = self._draw if self._picture else self._lazy_load
        if PictureLazyLoadMixin.CLIENT or PictureLazyLoadMixin.LOADED:
            self._lazy_load()

    def _lazy_load_picture(self):
        from common_things.img_loader import load_image, load_animation

        self.load_draw_methods()

        if self.PICTURE_PATH:
            self._picture = load_image(self.PICTURE_PATH, size=self.size)
            self.set_screen_picture_methods(load_image=load_image,
                                            load_animation=load_animation,
                                            picture=self._picture,
                                            )

    def _lazy_load(self):
        self._lazy_load_picture()
        self.additional_lazy_load()
        self.draw = self._draw
        self.draw()

    @classmethod
    def load_draw_methods(cls):
        if not cls.DRAW_METHODS_LOADED:
            from settings.window_settings import MAIN_SCREEN
            from pygame.transform import rotate
            from pygame.draw import circle, line, lines, polygon, rect

            cls.MAIN_SCREEN = MAIN_SCREEN

            cls.ROTATE = rotate
            cls.DRAW_LINE = line
            cls.DRAW_LINES = lines
            cls.DRAW_CIRCLE = circle
            cls.DRAW_POLYGON = polygon
            cls.DRAW_RECT = rect
            cls.DRAW_METHODS_LOADED = 1

    @classmethod
    def set_screen_picture_methods(cls, load_image, load_animation, picture, ):
        cls.LOAD_IMAGE = load_image
        cls.LOAD_ANIMATION = load_animation

        cls.PICTURE = picture

        cls.LOADED = 1

    @abstractmethod
    def additional_lazy_load(self):
        raise NotImplementedError()

    def _draw(self):
        raise NotImplementedError()

    @property
    def int_position(self):
        return int(self._position[0]), int(self._position[1])
