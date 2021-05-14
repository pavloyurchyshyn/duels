from game_tests.window_for_tests import *

from player_and_spells.player.player import Player

from world_arena.base.arena_cell import ArenaCell
from world_arena.world import World

WORLD = World([ArenaCell(), ], 0, 0, 500, 500)
WORLD.set_current_position((0, 0))


def TEST_CELL():
    G_Clock = GLOBAL_CLOCK
    G_Mouse = GLOBAL_MOUSE
    CELL = ArenaCell()

    while 1:
        MAIN_SCREEN.fill((110, 110, 110))
        dt = clock.tick(60) / 1000

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

        if keys[K_ESCAPE]:
            PY_QUIT()
            SYS_EXIT()

        display.update(MAIN_SCREEN_RECT)
