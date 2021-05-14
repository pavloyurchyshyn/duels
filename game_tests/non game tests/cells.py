from settings.init_pygame import *

from pygame.time import Clock
from pygame import event as EVENT
from pygame import key as KEY
from pygame import quit as PY_QUIT
from pygame import QUIT, K_ESCAPE, MOUSEBUTTONDOWN
from pygame import display, draw, Surface, constants, mouse, key

from settings.colors import WHITE
from settings.common_settings import DEFAULT_FONT, VERSION
from settings.window_settings import MAIN_SCREEN, MAIN_SCREEN_RECT, SCREEN_H, SCREEN_W  # main screen of all game

from common_things.global_clock import GLOBAL_CLOCK
from common_things.global_mouse import GLOBAL_MOUSE
from UI.camera import Camera
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

from settings.arena_settings import STANDARD_ARENA_CELL_SIZE, STANDARD_ARENA_BORDER_SIZE, \
    ELEMENT_SIZE, SUB_CELL_SIZE
from pygame import Rect, draw, transform, image, error, Surface

PLAYER_SIZE = 45

try:
    PLAYER_PIC = image.load('../../sprites/player/player_image.png').convert_alpha()
    # PLAYER_PIC = image.load('sprites/player/player_jojo.png').convert_alpha()
    PLAYER_PIC = transform.smoothscale(PLAYER_PIC, (int(PLAYER_SIZE), int(PLAYER_SIZE))).convert_alpha()
except error:
    print('No file sprites/player_image.png')
    exit()

from math import sin, cos, radians

BBB = []


def build_house(surf, pos, angle=0):
    global BBB
    x, y = pos
    values = ((-90, 100), (90, 600), (90, 400), (90, 600), (90, 140))

    i = 0
    for ang, l in values:
        angle += ang

        for l_step in range(0, l, ELEMENT_SIZE):
            new_x = x + cos(radians(angle)) * l_step
            new_y = y + sin(radians(angle)) * l_step

            new_x = (new_x // ELEMENT_SIZE) * ELEMENT_SIZE
            new_y = (new_y // ELEMENT_SIZE) * ELEMENT_SIZE

            r = Rect((new_x, new_y), (ELEMENT_SIZE, ELEMENT_SIZE))
            BBB.append((new_x, new_y))

            draw.rect(surf, (0, 0, 155), r)

        text = DEFAULT_FONT.render(str(i + 1), 1, (0, 255, 0))
        surf.blit(text, (x, y))
        i += 1
        x = int(x + cos(radians(angle)) * l)
        y = int(y + sin(radians(angle)) * l)

    x, y = pos
    r = Rect((x, y), (ELEMENT_SIZE, ELEMENT_SIZE))
    draw.rect(surf, (255, 2, 0), r, 5)


from pygame import SRCALPHA

flags = SRCALPHA


def TEST_ELEMENT_DRAW(*args):
    G_Clock = GLOBAL_CLOCK
    G_Mouse = GLOBAL_MOUSE

    new_surf = Surface((STANDARD_ARENA_CELL_SIZE, STANDARD_ARENA_CELL_SIZE))

    i = 0
    for x in range(0, STANDARD_ARENA_CELL_SIZE, ELEMENT_SIZE):
        for y in range(0, STANDARD_ARENA_CELL_SIZE, ELEMENT_SIZE):
            r = Rect((x, y), (ELEMENT_SIZE, ELEMENT_SIZE))
            draw.rect(new_surf, (55, 55, 55), r, 5)
            i += 1
    print(i)

    build_house(new_surf, (1, 500), 0)
    build_house(new_surf, (701, 700), 25)
    build_house(new_surf, (1401, 1000), 45)
    new_surf.convert_alpha()
    # new_surf.convert()
    MAIN_SCREEN.blit(new_surf, (0, 0))

    player_pos = [100, 100]

    CAMERA = Camera(*player_pos)

    mouse.set_cursor()
    while 1:
        CAMERA.update(player_pos)
        camera = CAMERA.camera

        # MAIN_SCREEN.fill((110, 110, 110))
        MAIN_SCREEN.blit(new_surf, (0 + camera[0], 0 + camera[1]))

        MAIN_SCREEN.blit(PLAYER_PIC, (player_pos[0] + camera[0], player_pos[1] + camera[1]))

        dt = clock.tick() / 1000

        G_Clock.update(dt)
        G_Mouse.update()

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

        if keys[constants.K_w]:
            player_pos[1] -= 5
        elif keys[constants.K_s]:
            player_pos[1] += 5
        if keys[constants.K_a]:
            player_pos[0] -= 5
        elif keys[constants.K_d]:
            player_pos[0] += 5

        if keys[K_ESCAPE]:
            PY_QUIT()
            SYS_EXIT()

        display.update(MAIN_SCREEN_RECT)


if __name__ == '__main__':
    TEST_ELEMENT_DRAW()
