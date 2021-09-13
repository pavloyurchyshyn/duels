class PictureLazyLoadMixin:
    DEFAULT_PICTURE_PATH = None
    PICTURE = None
    MAIN_SCREEN = None
    ROTATE = None

    def _lazy_load_picture(self):
        from common_things.img_loader import load_image
        from settings.window_settings import MAIN_SCREEN
        from pygame.transform import rotate

        self._main_screen = MAIN_SCREEN

        self._picture = load_image(self.DEFAULT_PICTURE_PATH, size=self.size)
        self._picture_rotate = rotate
        self.set_screen_picture_rotate(main_screen=MAIN_SCREEN,
                                       picture=self._picture,
                                       rotate=self._picture_rotate)
    @classmethod
    def set_screen_picture_rotate(cls, main_screen, picture, rotate):
        cls.PICTURE = picture
        cls.MAIN_SCREEN = main_screen
        cls.ROTATE = rotate
