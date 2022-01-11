from obj_properties.circle_form import Circle
from obj_properties.physic_body import PhysicalObj
from player.player_effects import *
from player.base.player_constants import *
from abc import abstractmethod

from math import atan2, cos, sin, radians
from world_arena.base.arena_cell_obj import ArenaCellObject

from common_things.common_objects_lists_dicts import BULLETS_LIST, PLAYERS_LIST, SPELLS_LIST
from common_things.loggers import LOGGER

from settings.players_settings.player_settings import *
from settings.global_parameters import GLOBAL_SETTINGS
from settings.default_keys import UP_C, LEFT_C, RIGHT_C, DOWN_C, SPRINT_C, \
    WEAPON_1_C, WEAPON_2_C, SPELL_1_C, SPELL_2_C, SPELL_3_C

rad_180 = radians(180)


class BasePlayer(Circle, PhysicalObj):
    PLAYER_HP = PLAYER_HEALTH_POINTS
    PLAYER_SPEED = PLAYER_SPEED
    PLAYER_SPRINT_SPEED = PLAYER_SPRINT_SPEED
    PLAYER_GLIDE_K = PLAYER_GLIDE_K
    PLAYER_HANDS_SIZE = PLAYER_HANDS_SIZE

    def __init__(self, x, y,
                 arena: ArenaCellObject,
                 team='POLYGON',
                 size=PLAYER_SIZE,
                 add_self_to_list=1,
                 **kwargs):
        super().__init__(x, y, size, dots_angle=True)
        PhysicalObj.__init__(self, f_coef=3)
        self._arena: ArenaCellObject = arena
        self.global_settings = GLOBAL_SETTINGS

        self.team = team

        self._full_health_points = kwargs.get('health_points', BasePlayer.PLAYER_HP)
        self._health_points = self._full_health_points

        self._angle = 0.0
        self.speed = kwargs.get('speed', BasePlayer.PLAYER_SPEED)
        self.sprint_speed = kwargs.get('sprint_speed', BasePlayer.PLAYER_SPRINT_SPEED)

        self.spawn_position = kwargs.get(SPAWN_POSITION, (x, y))

        self._time = 0.000000001
        self._d_time = 0.00000001

        self.spells = {
            SPELL_1_C: kwargs.get(SPELL_1_C),
            SPELL_2_C: kwargs.get(SPELL_2_C),
            SPELL_3_C: kwargs.get(SPELL_3_C),
        }
        self._build_spells()

        self._weapon = {
            WEAPON_1_C: kwargs.get(WEAPON_1_C, None),
            WEAPON_2_C: kwargs.get(WEAPON_2_C, None),
        }
        self._build_weapon()

        self._active_weapon = self._weapon[WEAPON_1_C]

        self.hands_radius = PLAYER_HANDS_SIZE
        self._hands_endpoint = [0, 0]

        self.bullets_list = BULLETS_LIST
        self.spells_list = SPELLS_LIST
        self.effects: dict = {}
        self.active_effects = {}

        self._statisic = {}

        self._damaged = 0

        self._switch_cd = kwargs.get('switch_cd', -0.5)
        self._next_switch = 1

        if add_self_to_list:
            PLAYERS_LIST.append(self)

    def _build_weapon(self):
        for key, weapon in self._weapon.items():
            if weapon:
                self._weapon[key] = weapon(*self.position, owner=self)

    def _build_spells(self):
        for key, spell in self.spells.items():
            if spell:
                self.spells[key] = spell(owner=self)

    def use_weapon(self):
        if self._active_weapon:
            self._active_weapon.use()

    def alt_use_weapon(self):
        if self._active_weapon:
            self._active_weapon.alt_use()

    def check_for_weapon_switch(self, commands):
        if self._next_switch >= 0.0:
            for key in self._weapon:
                if key in commands:
                    self._active_weapon = self._weapon[key]
                    self._next_switch = self._switch_cd
        elif self._next_switch < 0.0:
            self._next_switch += self._d_time

    def update_weapon(self):
        for weapon in self._weapon.values():
            if weapon:
                if weapon == self._active_weapon:
                    weapon.update(angle=self._angle, position=self._hands_endpoint)
                else:
                    weapon.update(angle=self._angle + rad_180, position=self._dots[7])

    def use_spells(self, commands):
        for key, spell in self.spells.items():
            if key in commands and spell:
                spell.use()

    def update_spells(self):
        for spell in self.spells.values():
            if spell:
                spell.update()

    def draw(self):
        raise NotImplementedError('Draw has to be implemented in subclasses')

    # def check_for_bullets_interaction(self):
    #     for bullet in self.bullets_list:
    #         if bullet.alive and self.collide_point(bullet.position):
    #             bullet.interact_with_object(self)
    #
    # def check_for_spells_interaction(self):
    #     for spell in self.spells_list:
    #         if spell.alive and self.collide(spell):
    #             spell.interact_with_object(self)

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

    def rotate_to_cursor(self, mouse_pos: tuple) -> bool:
        """
        :return: True if angle changed
        """
        if ROTATING_BLOCK in self.active_effects or STUN in self.active_effects:
            return False

        x_mouse_position, y_mouse_position = mouse_pos
        x_center_position, y_center_position = self._center

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
        d, self._damaged = self._damaged, 0
        return d

    @abstractmethod
    def update(*args, **kwargs):
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
        try:
            if self in PLAYERS_LIST:
                PLAYERS_LIST.remove(self)
        except ValueError as e:
            LOGGER.warning(f"Player not in list: {e}")
            # print('error')

