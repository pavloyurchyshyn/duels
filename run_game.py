from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# from pygame import mixer

# mixer.pre_init(44100, 16, 2, 4096)

from settings.init_pygame import *  # do not remove its ok

import datetime
import os

from pygame.time import Clock
from pygame import event as EVENT
from pygame import MOUSEBUTTONDOWN

EVENT.set_allowed([MOUSEBUTTONDOWN, ])

from pygame import display, draw, Surface, constants

from settings.colors import WHITE
from settings.global_parameters import GLOBAL_SETTINGS
from settings.common_settings import VERSION, FPS
from settings.window_settings import MAIN_SCREEN, MAIN_SCREEN_RECT, SCREEN_H, SCREEN_W, \
    MAIN_SCREEN_DEF_COLOR, MAIN_T_SCREEN  # main screen of all game
from settings.game_stages import ROUND_S, CURRENT_STAGE, START_ROUND_S, MULTIPLAYER_CLIENT_ROUND_S, \
    MULTIPLAYER_CLIENT_ROUND_PAUSE_S

from common_things.font_loader import DEFAULT_FONT
from common_things.global_clock import GLOBAL_CLOCK, ROUND_CLOCK
from common_things.global_mouse import GLOBAL_MOUSE
from common_things.global_keyboard import GLOBAL_KEYBOARD
from common_things.loggers import LOGGER

from settings.screen_size import SCREEN_H, SCREEN_W, Y_SCALE, X_SCALE

from game_body import GameBody
from time import time

display.set_caption(f'Boss Fight V{VERSION}')

clock = Clock()  # main clock of game | FPS limit


def update_fps():
    fps_text = DEFAULT_FONT.render(str(int(clock.get_fps())), 1, WHITE, (0, 0, 0))
    MAIN_SCREEN.blit(fps_text, (0, 0))


surface = Surface((200, 100), constants.SRCALPHA, 32)
surface.fill((0, 0, 0, 50))

surface.convert_alpha()


display.update(MAIN_SCREEN_RECT)


def update_scree():
    display.update(MAIN_SCREEN_RECT)


if __name__ == "__main__":
    G_Clock = GLOBAL_CLOCK
    R_Clock = ROUND_CLOCK
    G_Mouse = GLOBAL_MOUSE
    G_Keyboard = GLOBAL_KEYBOARD

    GAME_BODY = GameBody()
    start = time()
    while 1:
        events = EVENT.get()
        finish = time()

        clock.tick(FPS)
        dt = finish - start
        start = finish
        # update time
        G_Clock.update(dt)
        if GLOBAL_SETTINGS[CURRENT_STAGE] in {ROUND_S}:  # solo game or leave it for animation?
            R_Clock.update(dt)

        # update mouse and keyboard
        G_Mouse.update()
        G_Keyboard.update()

        # scroll up and scroll down update
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    G_Mouse.scroll_top = 1
                elif event.button == 5:
                    G_Mouse.scroll_bot = -1

        GAME_BODY.game_loop()

        draw.circle(MAIN_SCREEN, (255, 0, 0), (SCREEN_W // 2, SCREEN_H // 2), 5)

        update_fps()
        G_Mouse.draw()
        display.update(MAIN_SCREEN_RECT)
