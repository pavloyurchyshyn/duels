from visual.visual_effects_controller import VisualEffectsController
from settings.global_parameters import its_client_instance
from common_things.loggers import LOGGER


class ScreenLazyLoad:
    CLIENT_INSTANCE = 0
    EFFECTS_CON = VisualEffectsController
    MAIN_SCREEN = None

    def __init__(self):
        if its_client_instance() and ScreenLazyLoad.MAIN_SCREEN is None:
            self.load_screen()

    @staticmethod
    def load_screen():
        from settings.window_settings import MAIN_SCREEN
        ScreenLazyLoad.MAIN_SCREEN = MAIN_SCREEN
        LOGGER.info('Main screen loaded')
        ScreenLazyLoad.CLIENT_INSTANCE = 1

class LoadPictureMethodLazyLoad:
    LOAD_IMAGE = None
    LOAD_ANIMATION = None
    ANIMATION = None
    ROTATE_ANIMATION = None

    def __init__(self):
        if its_client_instance() and LoadPictureMethodLazyLoad.LOAD_IMAGE is None:
            super(LoadPictureMethodLazyLoad, self).__init__()
            self.load_img_loader()

    @staticmethod
    def load_img_loader():
        from common_things.img_loader import load_image, load_animation
        from UI.UI_base.animation import Animation, RotateAnimation

        LoadPictureMethodLazyLoad.LOAD_IMAGE = load_image
        LoadPictureMethodLazyLoad.LOAD_ANIMATION = load_animation
        LoadPictureMethodLazyLoad.ANIMATION = Animation
        LoadPictureMethodLazyLoad.ROTATE_ANIMATION = RotateAnimation
        LOGGER.info('Load images methods loaded')


class PygameMethodsLazyLoad:
    methods_loaded = 0

    DRAW_LINE = None
    DRAW_LINES = None
    DRAW_CIRCLE = None
    DRAW_POLYGON = None
    DRAW_RECT = None

    def __init__(self):
        if PygameMethodsLazyLoad.methods_loaded == 0 and its_client_instance():
            super(PygameMethodsLazyLoad, self).__init__()
            self.load_draw_methods()
            PygameMethodsLazyLoad.methods_loaded = 1
            LOGGER.info('Pygame methods loaded')

    @staticmethod
    def load_draw_methods():
        from pygame.draw import circle, line, lines, polygon, rect
        from pygame.transform import rotate, smoothscale, scale

        PygameMethodsLazyLoad.DRAW_LINE = line
        PygameMethodsLazyLoad.DRAW_LINES = lines
        PygameMethodsLazyLoad.DRAW_CIRCLE = circle
        PygameMethodsLazyLoad.DRAW_POLYGON = polygon
        PygameMethodsLazyLoad.DRAW_RECT = rect

        PygameMethodsLazyLoad.ROTATE = rotate
        PygameMethodsLazyLoad.SCALE = scale
        PygameMethodsLazyLoad.SMOOTH_SCALE = smoothscale


class OnePictureLazyLoad(LoadPictureMethodLazyLoad, PygameMethodsLazyLoad, ScreenLazyLoad):
    PICTURE_PATH = None
    PICTURE = None

    def __init__(self, size=None, angle=None, smooth_scale=0):
        if self.PICTURE is None and its_client_instance():
            super().__init__()
            PygameMethodsLazyLoad.__init__(self)
            ScreenLazyLoad.__init__(self)
            self.load_picture(size, angle, smooth_scale)
            self.additional_lazy_load()

    @classmethod
    def load_picture(cls, size, angle, smooth_scale):
        if cls.PICTURE_PATH:
            cls.PICTURE = cls.LOAD_IMAGE(cls.PICTURE_PATH, size,
                                         angle=angle,
                                         smooth_scale=smooth_scale)

            LOGGER.info(f'One picture loaded: {cls.PICTURE_PATH}')

    def additional_lazy_load(self):
        pass

