from common_things.singletone import Singleton
from settings.window_settings import MAIN_SCREEN
from common_things.global_clock import GLOBAL_CLOCK
from common_things.global_keyboard import GLOBAL_KEYBOARD
from settings.default_keys import *
from pygame.draw import lines
from pygame import constants
from math import dist
from common_things.stages import Stages


class UI_controller(metaclass=Singleton):
    def __init__(self, ):
        self.tree = {}
        self.reversed_tree = {}
        self.focused_element = None
        self.current_menu = None

        self.enter_default_focus = {}

        self.color = [255, 255, 255, 255]
        self.color_step = -1

        self.next_step = 1
        self.step_delay = 0.1

        self.next_enter = 1

        self.get_current_stage = Stages().get_current_stage
        self.current_stage_is_menu = Stages().current_stage_is_menu

    def update(self):
        if self.next_enter < 0:
            self.next_enter += GLOBAL_CLOCK.d_time

        if self.current_stage_is_menu() and self.get_current_stage() in self.tree:
            if self.next_step < 0:
                self.next_step += GLOBAL_CLOCK.d_time

            self.current_menu = self.get_current_stage()
            if self.focused_element is None:
                self.focused_element = self.enter_default_focus.get(self.current_menu)

                if not self.focused_element or not self.focused_element.is_active:
                    self.focused_element = self.get_left_top_element()

            if self.focused_element:
                self.update_color()
                self.move()

                if GLOBAL_KEYBOARD.ENTER and self.next_enter >= 0:
                    self.next_enter = -0.5
                    self.focused_element.click(xy=self.focused_element.center)

        else:
            self.drop_focused()

    def move(self):
        if self.next_step > 0:
            self.next_step = -self.step_delay

            foc_el = self.focused_element
            pressed_keys = GLOBAL_KEYBOARD.pressed
            commands = GLOBAL_KEYBOARD.commands

            x = y = 0
            if pressed_keys[constants.K_UP] or UP_C in commands:
                y -= 1
            elif pressed_keys[constants.K_DOWN] or DOWN_C in commands:
                y += 1

            if pressed_keys[constants.K_LEFT] or LEFT_C in commands:
                x -= 1
            elif pressed_keys[constants.K_RIGHT] or RIGHT_C in commands:
                x += 1

            if x:
                new = self.__make_x_step(foc_el, x)
                if new:
                    self.focused_element = new
            elif y:
                new = self.__make_y_step(foc_el, y)
                if new:
                    self.focused_element = new

    def __make_y_step(self, obj, y_step):
        x0, y0 = obj.center
        new_item = None
        for item in self.tree[self.current_menu].values():
            if item != obj and item.is_active and item.is_visible:
                x1, y1 = item.center
                if y_step < 0:
                    if y0 - y1 < 0:
                        continue

                    if new_item:
                        new_item = item if dist(obj.center, item.center) < dist(obj.center,
                                                                                new_item.center) else new_item
                    else:
                        new_item = item

                else:
                    if y0 - y1 > 0:
                        continue

                    if new_item:
                        new_item = item if dist(obj.center, item.center) < dist(obj.center,
                                                                                new_item.center) else new_item
                    else:
                        new_item = item

        return new_item

    def __make_x_step(self, obj, x_step):
        x0, y0 = obj.center
        new_item = None
        for item in self.tree[self.current_menu].values():
            if item != obj and item.is_active and item.is_visible:
                x1, y1 = item.center
                if x_step < 0:
                    if x0 - x1 < 0:
                        continue

                    if new_item:
                        new_item = item if dist(obj.center, item.center) < dist(obj.center,
                                                                                new_item.center) else new_item
                    else:
                        new_item = item

                else:
                    if x0 - x1 > 0:
                        continue

                    if new_item:
                        new_item = item if dist(obj.center, item.center) < dist(obj.center,
                                                                                new_item.center) else new_item
                    else:
                        new_item = item

        return new_item

    def update_color(self):
        self.color[-1] += self.color_step * GLOBAL_CLOCK.d_time
        if self.color[-1] > 255:
            self.color_step = -1
            self.color[-1] = 255

        elif self.color[-1] < 0:
            self.color_step = 1
            self.color[-1] = 0

    def draw(self):
        if self.focused_element:
            x0, y0 = self.focused_element.left_top
            x1 = x0 + self.focused_element.width + 3
            y1 = y0 + self.focused_element.height + 3
            x0 -= 4
            y0 -= 4
            lines(MAIN_SCREEN, self.color, 1, ((x0, y0), (x1, y0), (x1, y1), (x0, y1)), 3)

    def add_button_to_menu(self, menu, button):
        if button.id:
            if button.id in self.tree[menu.name]:
                raise Exception(f"Button already exists in {menu.name}")
            elif self.tree[menu.name]:
                self.tree[menu.name][button.id] = button
            else:
                self.tree[menu.name] = {button.id: button}

    def add_menu(self, menu, *elements, enter_focus=None):
        self.tree[menu.name] = {button.id: button for button in elements if button.id}

        if enter_focus:
            self.enter_default_focus[menu.name] = enter_focus

    def drop_focused(self):
        self.focused_element = None
        self.current_menu = None

    def get_left_top_element(self):
        elements = self.tree[self.current_menu]
        y = 9999
        x = 9999
        left_top_el = None
        for element in elements.values():
            if element.is_active:
                x1, y1 = element.center
                if x1 < x or y1 < y:
                    x, y = x1, y1
                    left_top_el = element

        return left_top_el


UI_TREE = UI_controller()
