from obj_properties.img_lazy_load import LoadPictureMethodLazyLoad, PygameMethodsLazyLoad, ScreenLazyLoad
from common_things.save_and_load_json_config import get_param_from_cgs
from common_things.camera import GLOBAL_CAMERA
from settings.network_settings.network_constants import PLAYER_SKIN
from settings.global_parameters import its_client_instance


class PlayerLazyLoad(LoadPictureMethodLazyLoad, PygameMethodsLazyLoad, ScreenLazyLoad):
    PLAYERS_SKINS = {}
    PlayerImagesManager = None
    CIRCLE_ROT_SPEED = 0.01

    def __init__(self, player_skin=None, *args, **kwargs):
        if its_client_instance():
            from settings.colors import PLAYERS_COLORS

            super().__init__()
            PygameMethodsLazyLoad.__init__(self)
            ScreenLazyLoad.__init__(self)

            self.turn_off_camera = kwargs.get('turn_off_camera', False)
            self.color = player_skin if player_skin else get_param_from_cgs(PLAYER_SKIN, def_value='blue')

            self.under_player_circle = kwargs.get('under_circle_color')

            self._draw_health_points = kwargs.get('draw_health_points', True)

            self.image = None
            self.face_anim = None

            self._load_methods()

            self.images_manager = PlayerLazyLoad.PlayerImagesManager(size=self._size * 2)

            if type(self.color) in (list, tuple):
                self.color = {'body': self.color[0],
                              'face': self.color[1]}
            elif type(self.color) is str:
                self.color = PLAYERS_COLORS[self.color]

            color_key = (self._size, tuple(self.color['body']), tuple(self.color['face']))
            if color_key not in PlayerLazyLoad.PLAYERS_SKINS:
                PlayerLazyLoad.PLAYERS_SKINS[color_key] = self.get_skin()

            pictures = PlayerLazyLoad.PLAYERS_SKINS[color_key]
            self.image = pictures['body']
            self.face_anim = self.ANIMATION(self.position,
                                            idle_frames=pictures['idle_animation'],
                                            **pictures['other_animation'])

            self.under_player_circle = self.ROTATE_ANIMATION(self._center, self.images_manager.get_circle()) \
                if self.under_player_circle else None

            self.additional_lazy_load()

            self.camera = kwargs.get('camera', GLOBAL_CAMERA)

    def get_skin(self):
        return self.images_manager.get_new_skin(self.color)

    # def _pictures_lazy_load(self):
    #     from settings.window_settings import MAIN_SCREEN
    #     from player.player_images import PlayerImagesManager
    #     from UI.UI_base.animation import Animation, RotateAnimation
    #     from UI.UI_base.text_UI import Text
    #     from pygame.transform import scale, smoothscale
    #
    #     BasePlayer.SCALE = scale
    #     BasePlayer.SMOOTH_SCALE = smoothscale
    #
    #     self.MAIN_SCREEN = MAIN_SCREEN
    #
    #     self.images_manager = PlayerImagesManager(size=self._size * 2 if self._size == PLAYER_SIZE else self._size)
    #     pictures = self.images_manager.get_new_skin(self.color)
    #     self.image = pictures['body']
    #     self.face_anim = Animation(self._center,
    #                                idle_frames=pictures['idle_animation'],
    #                                **pictures['other_animation'])
    #
    #     self.high_images_manager = PlayerImagesManager(original_size=1)
    #     high_pic = self.high_images_manager.get_new_skin(self.color)
    #     self.high_image = high_pic['body']
    #     self.high_face_anim = Animation(self._center,
    #                                     idle_frames=high_pic['idle_animation'],
    #                                     **high_pic['other_animation'])
    #
    #     self.health_points_text = Text(int(self._health_points), MAIN_SCREEN, x=self._center[0],
    #                                    y=self._center[1] + self._size,
    #                                    auto_draw=False)
    #     self._additional_lazy_load()
    #     self.draw = self._draw

    def update_color(self, body_color=None, face_color=None):
        self.color = {'body': body_color, 'face': face_color}
        color_key = (self._size, tuple(body_color), tuple(face_color))

        if color_key in PlayerLazyLoad.PLAYERS_SKINS:
            pictures = PlayerLazyLoad.PLAYERS_SKINS[color_key]
        else:
            PlayerLazyLoad.PLAYERS_SKINS[color_key] = self.get_skin()
            pictures = PlayerLazyLoad.PLAYERS_SKINS[color_key]

        self.image = pictures['body']
        self.face_anim = self.ANIMATION(self._center,
                                        idle_frames=pictures['idle_animation'],
                                        **pictures['other_animation'])

    def _load_methods(self):
        if PlayerLazyLoad.PlayerImagesManager is None:
            from player.player_images import PlayerImagesManager
            PlayerLazyLoad.PlayerImagesManager = PlayerImagesManager

    def additional_lazy_load(self):
        pass

    def draw(self):
        raise NotImplementedError('Have to implement draw method in inheritance class')

    @property
    def int_position(self):
        return int(self._position[0]), int(self._position[1])
