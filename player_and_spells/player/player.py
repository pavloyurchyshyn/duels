# from obj_properties.physical_objects import PhysicalObj, SimplePhysicalCircleObj
from obj_properties.circle_form import Circle
from settings.player_settings import *

from pygame.constants import *
from pygame import mouse, key, transform
from pygame.draw import circle, line

from UI.UI_base.animation import Animation
from math import atan2, cos, sin, degrees, dist

from settings.colors import BLOOD_COLOR
from settings.window_settings import MAIN_SCREEN

# global things
from UI.camera import GLOBAL_CAMERA
from world_arena.world import GLOBAL_WORLD
from settings.global_parameters import GLOBAL_SETTINGS
import time


class Player(Circle):  # , PhysicalObj):
    MAIN_SCREEN = MAIN_SCREEN
    # BULLETS_CON = BULLETS_CONTROLLER  # check for collide with bullets
    # PARTICLES_CON = PARTICLES_CONTROLLER
    PLAYER_HP = PLAYER_HP
    PLAYER_SPEED = PLAYER_SPEED
    PLAYER_SPRINT_SPEED = PLAYER_SPRINT_SPEED
    PLAYER_GLIDE_K = PLAYER_GLIDE_K
    PLAYER_PUSH_FORCE = PLAYER_PUSH_FORCE
    BLOOD_COLOR = BLOOD_COLOR

    def __init__(self, x, y,
                 size=PLAYER_SIZE, mass=PLAYER_MASS,
                 n_a=PLAYER_GLIDE_K, **kwargs):
        super().__init__(x, y, size)
        # PhysicalObj.__init__(self, mass)

        self.WORLD = kwargs.get('world', GLOBAL_WORLD)
        self.CURRENT_CELL = self.WORLD.current_cell
        # self.item_con = ITEM_CONTROLLER

        self.hands_radius = PLAYER_HANDS_SIZE + PLAYER_SIZE

        self._angle = 0

        self.image = PLAYER_PIC
        # =======================
        self._full_hp = kwargs.get('hp', Player.PLAYER_HP)
        self._hp = self._full_hp

        # self.hp_bar = Loader(stage=self.hp,
        #                      stages_num=self._full_hp,
        #                      bar_pos=(30, 40),
        #                      bar_x_size=200,
        #                      bar_y_size=20,
        #                      text_pos=(30, 27),
        #                      text=str(self._hp),
        #                      bar_inner_color=PLAYER_HP_BAR_COLOR,
        #
        #                      )
        # =======================

        self.camera = kwargs.get('camera', GLOBAL_CAMERA)

        self.speed = kwargs.get('speed', Player.PLAYER_SPEED)
        self.sprint_speed = kwargs.get('sprint_speed', Player.PLAYER_SPRINT_SPEED)

        self.global_settings = GLOBAL_SETTINGS
        # ============= inventory ========

        self._inventory = {
            1: kwargs.get('weapon_1', None),
            2: kwargs.get('weapon_2', None),
            3: kwargs.get('weapon_3', None),
        }

        self.inv_obj_in_hands = None  # like hands
        self.picked_from_inv = None  # key of last taken obj from inventory

        self._backpack = kwargs.get('backpack', [])
        # =======================================
        self.cursor(mouse.get_pos())

        # self._messages = Messages(self.camera, (x + 50, y))

        self.hands = None
        self.hands_endpoint = [0, 0]
        self.hands_force = Player.PLAYER_PUSH_FORCE

        # self.spell = FireBallSkill(arena=self.arena,
                                   # item_con=self.item_con)

        self.particles = []

        # self._blood_drops = BloodDrops(x=x, y=y, arena=self.arena)

        # circle(self.arena.floor_surface, (255, 255, 255), self._center, 100)
        self.face_anim = Animation(self._center, idle_frames=IDLE_ANIMATION, **OTHER_ANIMATIONS)

        self._time = 0.000000001
        self._d_time = 0.00000001

    def update(self, time_d):

        self._time += time_d
        self._d_time = time_d

        mouse_buttons = mouse.get_pressed()
        m_pos = mouse.get_pos()
        keys = key.get_pressed()
        self._velocity.zero()
        self.step(keys)

        self.cursor(m_pos)

        self.__get_from_inventory(keys)

        if self.hands and self.hands not in self.inventory.values():
            if keys[K_g]:
                self.hands.zero_force()
                self.hands = None

            else:
                if self.hands_radius + self.hands_radius < dist(self._center, self.hands._center):
                    self.hands.zero_force()
                    self.hands = None

                elif not self.hands.alive:
                    self.hands.zero_force()
                    self.hands = None

                else:
                    feedback = self.hands.change_position(xy=self.hands_endpoint, angle=self._angle)
                    self.hands._make_dots()
                    if feedback == 'drop':
                        self.hands.zero_force()
                        self.hands = None

                if mouse_buttons[0]:
                    self.hands.zero_force()

                    self.hands.change_position(xy=self.hands_endpoint)
                    self.hands._make_dots()
                    self.hands = None

                if mouse_buttons[2]:
                    self.hands.zero_force()
                    self.hands.push(self._center, self.hands_force)
                    self.hands = None

        if keys[K_f]:
            self._grab_item(m_pos)

        if keys[K_q]:
            self.use_Q_spell()

        elif mouse_buttons[0]:
            if self.hands and self.hands in self.inventory.values():
                if self.hands.range:
                    self.hands.shoot(*self.hands_endpoint, self._angle)

        if keys[K_p]:
            self.damage(5)

        if keys[K_r]:
            if self.hands and self.hands in self.inventory.values():
                if self.hands.range:
                    self.hands.reload()

        if keys[K_e]:
            self._interact(m_pos)

        if keys[K_t]:
            pass
            # self._messages.add_message('TEST MESSAGE')

        # self._messages.update(self._d_time, position=self._center)
        self.face_anim.update(self._d_time, self._center, self._angle)
        self.__pause(keys)
        self.__update_inventory(time_d)
        self.camera.update(self.position)

        # self.spell.update(d_time=time_d)
        # self._blood_drops.update(time_d, *self._center)

    def _interact(self, m_pos):
        pos = m_pos if dist(self._center, m_pos) <= self.hands_radius else self.hands_endpoint

        self.arena.interact(interact_pos=pos)

    def __get_from_inventory(self, keys):
        for i, k in enumerate((K_1, K_2, K_3)):
            if keys[k]:
                if self.hands and self.hands in self.inventory.values():
                    if self.hands != self.inventory[i + 1] and self.hands.range:
                        self.hands.stop_reload()

                self.hands = self.inventory[i + 1]
                break

    def __update_inventory(self, time_d):
        for weapon, dot in zip(self.inventory.values(), [self._dots[5], self._dots[7], self._dots[9]]):
            if weapon:
                if weapon == self.hands:
                    weapon.update(*self.hands_endpoint, self._angle, time_d=time_d)
                else:
                    weapon.update(*dot, -self._angle, time_d=time_d)

    def __pause(self, keys):
        if (keys[K_ESCAPE] or keys[K_LALT]) and time.time() > self.global_settings['next_pause']:
            self.global_settings['PAUSE'] = True
            self.global_settings['next_pause'] = time.time() + self.global_settings['pause_delay']

    def use_Q_spell(self):
        # self.spell.use(*self.hands_endpoint, angle=self._angle)
        self.face_anim.change_animation('rage')

    def cursor(self, m_pos: tuple):
        x1, y1 = m_pos
        xc, yc = self._center
        xc += self.camera.camera[0]
        yc += self.camera.camera[1]

        d_x = 0.00001 if x1 - xc == 0 else x1 - xc
        d_y = 0.00001 if y1 - yc == 0 else y1 - yc

        angle = atan2(d_y, d_x)

        x2 = self._center[0] + cos(angle) * self.hands_radius
        y2 = self._center[1] + sin(angle) * self.hands_radius

        self.hands_endpoint = [x2, y2]

        self._angle = angle

    def step(self, keys):
        self._use_self_force()

        x_step = 0
        if keys[K_d]:
            x_step += self.speed
        if keys[K_a]:
            x_step -= self.speed

        y_step = 0
        if keys[K_w]:
            y_step -= self.speed
        if keys[K_s]:
            y_step += self.speed

        if x_step != 0 or y_step != 0:
            if keys[K_LSHIFT]:
                x_step *= self.sprint_speed
                y_step *= self.sprint_speed

            x, y = self._center
            x_add = 0 if x_step == 0 else (x_step / abs(x_step)) * self._size
            y_add = 0 if y_step == 0 else (y_step / abs(y_step)) * self._size
            new_x, new_y = x + x_step * self._d_time, y + y_step * self._d_time

            if not self.arena.can_go(new_x + x_add, new_y + y_add):
                self._make_dots_with_angle(self._angle)
                return
            self._push_another_items()
            self._change_position((new_x, new_y))

            # items = self.item_con.items.copy()
            # while items:
            #     item = items.pop()
            #
            #     if self.collide_dots(item):
            #         try:
            #             item.push(self._center, self._size*self._t_delay)  # # # # # # # #
            #         except AttributeError as a:
            #             print(a, 'can`t be pushed')
            #             pass

        else:
            self._make_dots_with_angle(self._angle)

    def draw(self) -> None:
        # self._messages.draw()
        dx, dy = self.camera.camera

        x0, y0 = self._center

        line(Player.MAIN_SCREEN, (255, 255, 255),
             (x0 + dx, y0 + dy),
             (self.hands_endpoint[0] + dx, self.hands_endpoint[1] + dy))

        circle(Player.MAIN_SCREEN, (255, 255, 255), (self.hands_endpoint[0] + dx, self.hands_endpoint[1] + dy), 3)

        img_copy = transform.rotate(self.image, -degrees(self._angle))

        Player.MAIN_SCREEN.blit(img_copy, (x0 - img_copy.get_width() // 2 + dx, y0 - img_copy.get_height() // 2 + dy))

        # if self.hands:
        #     self.hands.draw(window, dx, dy)

        if self.global_settings['test_draw']:
            for dot in self._dots:
                circle(Player.MAIN_SCREEN, (0, 255, 255), (dot[0] + dx, dot[1] + dy), 1)

        for weapon in self.inventory.values():
            if weapon:
                weapon.draw(dx, dy)

        self.face_anim.draw(dx, dy)
        self.hp_bar.draw()

    def _grab_item(self, m_pos):
        dot = m_pos if dist(self._center, m_pos) <= self.hands_radius else self.hands_endpoint

        for item in self.item_con.items:
            if item in self.inventory.values():
                continue

            if item.collide_point(dot):
                if item.can_be_collected():
                    if None in self.inventory.values():
                        for key in self.inventory.keys():
                            if self.inventory[key] is None:
                                self.inventory[key] = item
                                break

                else:
                    if self.hands and self.hands in self.inventory.values():
                        if self.hands.range and self.hands.reloading:
                            self.hands.stop_reload()

                    self.hands = item
                    break


    def update_cell(self):
        self.CURRENT_CELL = self.WORLD.current_cell


    @property
    def position(self):
        return self._center

    @position.setter
    def position(self, pos):
        self._change_position(pos)

    @property
    def backpack(self):
        return self._backpack

    @backpack.setter
    def backpack(self, item):
        self._backpack.append(item)

    @property
    def inventory(self):
        return self._inventory

    @inventory.setter
    def inventory(self, inventory):
        self._inventory = inventory

    @property
    def full_hp(self):
        return self._full_hp

    @full_hp.setter
    def full_hp(self, hp):
        self._full_hp = hp

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        self.hp_bar.update(text=self._hp, current_stage=self._hp, stages_num=self._full_hp)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value

    def damage(self, damage):
        self._hp -= damage
        self.hp_bar.update(text=self._hp, current_stage=self._hp, stages_num=self._full_hp)

    @property
    def alive(self):
        return self._hp > 0

    @property
    def dead(self):
        return self._hp <= 0
