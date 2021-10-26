from obj_properties.circle_form import Circle
from settings.players_settings.player_settings import *
from settings.global_parameters import GLOBAL_SETTINGS
from abc import abstractmethod
from settings.default_keys import UP_C, LEFT_C, RIGHT_C, DOWN_C, SPRINT_C, WEAPON_1_C, WEAPON_2_C, WEAPON_3_C
from math import atan2, cos, sin
from world_arena.base.arena_cell_obj import ArenaCellObject
from common_things.common_objects_lists_dicts import BULLETS_LIST, PLAYERS_LIST
from settings.effects import *
from settings.colors import BLOOD_COLOR
from common_things.camera import GLOBAL_CAMERA
from common_things.save_and_load_json_config import get_param_from_cgs
from settings.network_settings.network_constants import PLAYER_SKIN


class BasePlayer(Circle):
    PLAYER_HP = PLAYER_HEALTH_POINTS
    PLAYER_SPEED = PLAYER_SPEED
    PLAYER_SPRINT_SPEED = PLAYER_SPRINT_SPEED
    PLAYER_GLIDE_K = PLAYER_GLIDE_K
    PLAYER_HANDS_SIZE = PLAYER_HANDS_SIZE
    BLOOD_COLOR = BLOOD_COLOR

    MAIN_SCREEN = None
    CIRCLE_ROT_SPEED = 0.01

    def __init__(self, x, y,
                 arena: ArenaCellObject,
                 team=None,
                 player_skin=None,
                 size=PLAYER_SIZE,
                 **kwargs):
        super().__init__(x, y, size, dots_angle=True)
        self._arena: ArenaCellObject = arena
        self.team = team
        self._angle = 0.0
        self.global_settings = GLOBAL_SETTINGS

        self._full_health_points = kwargs.get('health_points', BasePlayer.PLAYER_HP)
        self._health_points = self._full_health_points

        self.speed = kwargs.get('speed', BasePlayer.PLAYER_SPEED)
        self.sprint_speed = kwargs.get('sprint_speed', BasePlayer.PLAYER_SPRINT_SPEED)

        self.spawn_position = kwargs.get(SPAWN_POSITION, (x, y))

        self._time = 0.000000001
        self._d_time = 0.00000001

        self._inventory = {
            1: kwargs.get(WEAPON_1_C, None),
            2: kwargs.get(WEAPON_2_C, None),
            3: kwargs.get(WEAPON_3_C, None),
        }
        self._damaged = 0
        self.hands_radius = PLAYER_HANDS_SIZE
        self._hands_endpoint = [0, 0]

        self.bullets_list = BULLETS_LIST
        self.effects: dict = {}
        self.active_effects = {}
        PLAYERS_LIST.append(self)

        self.camera = kwargs.get('camera', GLOBAL_CAMERA)
        self.turn_off_camera = kwargs.get('turn_off_camera', False)
        self.color = player_skin if player_skin else get_param_from_cgs(PLAYER_SKIN, def_value='blue')
        self.image = None
        self.face_anim = None
        self.under_player_circle = kwargs.get('under_player_circle_color')
        self._draw_health_points = kwargs.get('draw_health_points', True)

        if kwargs.get('load_images'):
            self._pictures_lazy_load()

        else:
            self.draw = self._pictures_lazy_load

    def _pictures_lazy_load(self):
        from settings.window_settings import MAIN_SCREEN
        from player_and_spells.player.player_images import PlayerImagesManager
        from UI.UI_base.animation import Animation, RotateAnimation
        from UI.UI_base.text_UI import Text

        self.MAIN_SCREEN = MAIN_SCREEN
        self.images_manager = PlayerImagesManager(size=self._size *2 if self._size == PLAYER_SIZE else self._size)
        pictures = self.images_manager.get_new_skin(self.color)
        self.image = pictures['body']
        self.face_anim = Animation(self._center,
                                   idle_frames=pictures['idle_animation'],
                                   **pictures['other_animation'])
        self.under_player_circle = RotateAnimation(self._center,
                                                   self.images_manager.get_circle()) if self.under_player_circle else None

        self.health_points_text = Text(int(self._health_points), MAIN_SCREEN, x=self._center[0],
                                       y=self._center[1] + self._size,
                                       auto_draw=False)
        self._additional_lazy_load()
        self.draw = self._draw

    def update_color(self, body_color=None, face_color=None):
        from UI.UI_base.animation import Animation
        pictures = self.images_manager.get_new_skin((body_color, face_color))
        self.image = pictures['body']
        self.face_anim = Animation(self._center,
                                   idle_frames=pictures['idle_animation'],
                                   **pictures['other_animation'])

    def _additional_lazy_load(self):
        pass

    def _draw(self):
        raise NotImplementedError('Draw has to be implemented in subclasses')

    def check_for_bullets_damage(self):
        for bullet in self.bullets_list:
            if bullet.alive and self.collide_point(bullet.position):
                self.damage(bullet.damage)
                bullet.kill()

    def update_hands_endpoints(self):
        self._hands_endpoint[0] = self._center[0] + cos(self._angle) * self.PLAYER_HANDS_SIZE
        self._hands_endpoint[1] = self._center[1] + sin(self._angle) * self.PLAYER_HANDS_SIZE

    def make_step(self, commands) -> bool:
        """
        :param commands: tuple or list of commands
        :return: True if position changed
        """
        if ROOT in self.active_effects or STUN in self.active_effects:
            return False

        step_speed = self.sprint_speed if SPRINT_C in commands else self.speed
        step_speed = step_speed * self._d_time
        if SLOW in self.active_effects:
            step_speed *= self.active_effects[SLOW]

        x_step = 0
        if RIGHT_C in commands:
            x_step += step_speed
        if LEFT_C in commands:
            x_step -= step_speed

        y_step = 0
        if UP_C in commands:
            y_step -= step_speed
        if DOWN_C in commands:
            y_step += step_speed

        if x_step != 0 or y_step != 0:
            x, y = self._center
            new_x, new_y = x + x_step, y + y_step
            self._change_position((new_x, new_y))
            return True

        return False

    def rotate_to_cursor(self, mouse_pos: tuple, camera_x_position=0, camera_y_position=0) -> bool:
        """
        :return: True if angle changed
        """
        if ROTATING_BLOCK in self.active_effects or STUN in self.active_effects:
            return False

        x_mouse_position, y_mouse_position = mouse_pos
        x_center_position, y_center_position = self._center

        x_center_position += camera_x_position
        y_center_position += camera_y_position

        d_x = 0.00001 if x_mouse_position - x_center_position == 0 else x_mouse_position - x_center_position
        d_y = 0.00001 if y_mouse_position - y_center_position == 0 else y_mouse_position - y_center_position

        old_angle = self._angle
        self._angle = atan2(d_y, d_x)

        return self._angle != old_angle

    def add_effects(self, effects):
        for name, effect in effects:
            self.add_effect(name, effect)

    def add_effect(self, name, effect: dict):
        if name in self.effects:
            if self.effects[name][DURATION] < effect[DURATION]:
                self.effects[name] = effect
        else:
            self.effects[name] = effect

    def update_effects(self, d_time):
        self.active_effects.clear()

        for effect_name, effect_values in self.effects.copy():
            self.update_effect(effect_name, effect_values, d_time)

    def update_effect(self, name, effect, d_time):
        if effect[PERIOD_TYPE] == SOLID_EFFECT:
            effect[DURATION] -= d_time
            if effect[DURATION] < 0:
                self.effects.pop(name)
            else:
                self.damage(effect.get(DAMAGE, 0))

                for effect_type in (SLOW,):
                    if effect_type in effect:
                        self.active_effects[effect_type] -= effect[effect_type]
                        if self.active_effects[effect_type] < 0:
                            self.active_effects[effect_type] = 0
                    else:
                        self.active_effects[effect_type] = 1 - effect[effect_type]

                for effect_type in (ROOT, ROTATING_BLOCK, BLOCK):
                    self.active_effects[effect_type] = 1

        elif effect[PERIOD_TYPE] == PERIODIC_EFFECT:
            raise NotImplementedError('Need to create this method')

    def revise(self):
        self._health_points = self._full_health_points

    def damage(self, damage):
        self._health_points -= damage
        self._damaged += damage

    @property
    def damaged(self):
        d = self._damaged
        self._damaged = 0
        return d

    @abstractmethod
    def update(self, commands=(), mouse_buttons=(0, 0, 0), mouse_pos=None):
        raise NotImplementedError

    @property
    def position(self):
        return self._center

    @position.setter
    def position(self, pos):
        if pos:
            self._change_position(pos)

    @property
    def full_health_points(self):
        return self._full_health_points

    @full_health_points.setter
    def full_health_points(self, hp):
        self._full_health_points = hp

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        if value:
            self._angle = value

    @property
    def alive(self):
        return self._health_points > 0

    @property
    def dead(self):
        return self._health_points <= 0

    @property
    def health_points(self):
        return self._health_points

    @health_points.setter
    def health_points(self, health_points):
        self._health_points = health_points

    def __del__(self):
        PLAYERS_LIST.remove(self)
