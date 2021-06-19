from settings.init_pygame import *

from pygame.time import Clock
from pygame import event as EVENT
from pygame import key as KEY
from pygame import quit as PY_QUIT
from pygame import QUIT, K_ESCAPE, MOUSEBUTTONDOWN
from pygame import display, draw, Surface, constants, mouse

from settings.colors import WHITE
from settings.common_settings import DEFAULT_FONT, VERSION
from settings.window_settings import MAIN_SCREEN, MAIN_SCREEN_RECT, SCREEN_H, SCREEN_W  # main screen of all game

from common_things.global_clock import GLOBAL_CLOCK
from common_things.global_mouse import GLOBAL_MOUSE
from common_things.global_keyboard import GLOBAL_KEYBOARD

from time import time
from sys import exit as SYS_EXIT

display.set_caption(f'Boss Fight V{VERSION}')

clock = Clock()  # main clock of game | FPS limit


def update_fps():
    fps_text = DEFAULT_FONT.render(str(int(clock.get_fps())), 1, WHITE, (0, 0, 0))

    MAIN_SCREEN.blit(fps_text, (0, 0))


# surface = Surface((200, 100), constants.SRCALPHA, 32)
# surface.fill((0, 0, 0, 50))
#
# surface.convert_alpha()

el_pos = list(mouse.get_pos())


def TEST_ELEMENT_DRAW(*args):
    G_Clock = GLOBAL_CLOCK
    G_Mouse = GLOBAL_MOUSE

    while 1:
        MAIN_SCREEN.fill((110, 110, 110))
        dt = clock.tick(60) / 1000

        G_Clock.update(dt)
        G_Mouse.update()
        GLOBAL_KEYBOARD.update()

        events = EVENT.get()
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    G_Mouse.scroll_top = 1
                elif event.button == 5:
                    G_Mouse.scroll_bot = -1

        l, m, r = G_Mouse.pressed
        xy = G_Mouse.pos

        for element in args:
            if hasattr(element, 'click') and l:
                element.click(xy)
            element.update()
            element.draw()

        dx, dy = G_Mouse.rel
        el_pos[0] += dx
        el_pos[1] += dy
        draw.circle(MAIN_SCREEN, (200, 200, 200), el_pos, 5)
        update_fps()
        keys = KEY.get_pressed()

        if keys[K_ESCAPE]:
            PY_QUIT()
            SYS_EXIT()

        display.update(MAIN_SCREEN_RECT)

