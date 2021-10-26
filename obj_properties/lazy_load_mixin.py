class PictureLazyLoadMixin:
    PICTURE_PATH = None
    PICTURE = None
    MAIN_SCREEN = None
    ROTATE = None

    def __init__(self):
        self.draw = self._draw if self._picture else self._lazy_load

    def _lazy_load_picture(self):
        from common_things.img_loader import load_image, load_animation
        from settings.window_settings import MAIN_SCREEN
        from pygame.transform import rotate

        self._main_screen = MAIN_SCREEN

        self._picture = load_image(self.PICTURE_PATH, size=self.size)
        self._picture_rotate = rotate
        self.set_screen_picture_rotate(main_screen=MAIN_SCREEN,
                                       picture=self._picture,
                                       rotate=self._picture_rotate)

    def _lazy_load(self):
        self._lazy_load_picture()
        self.draw = self._draw
        self.draw()

    @classmethod
    def set_screen_picture_rotate(cls, main_screen, picture, rotate):
        cls.PICTURE = picture
        cls.MAIN_SCREEN = main_screen
        cls.ROTATE = rotate

    def _draw(self):
        raise NotImplementedError()

    @property
    def int_position(self):
        return int(self._position[0]), int(self._position[1])