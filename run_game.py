from common_things.loggers import LOGGER
from common_things.save_and_load_json_config import get_cgs_config

LOGGER.info(f'Global parameters: {get_cgs_config()}')

import traceback
import sys

try:
    from settings.global_parameters import SET_CLIENT_INSTANCE

    SET_CLIENT_INSTANCE(1)

    from settings.init_pygame import *  # do not remove its ok

    from pygame.time import Clock
    from pygame import event as EVENT
    from pygame import MOUSEBUTTONDOWN

    EVENT.set_allowed([MOUSEBUTTONDOWN, ])

    from pygame import display, draw, Surface, constants

    from settings.colors import WHITE
    from settings.common_settings import VERSION, FPS
    from settings.window_settings import MAIN_SCREEN, MAIN_SCREEN_RECT
    from settings.game_stages_constants import ROUND_STAGE
    from settings.global_parameters import get_slow_motion_k, update_slow_motion, get_fps

    from UI.font_loader import DEFAULT_FONT

    from common_things.global_clock import GLOBAL_CLOCK, ROUND_CLOCK
    from common_things.global_mouse import GLOBAL_MOUSE
    from common_things.global_keyboard import GLOBAL_KEYBOARD
    from common_things.stages import Stages

    from settings.screen_size import SCREEN_H, SCREEN_W

    from game_body import GameBody
    from time import time

    display.set_caption(f'V{VERSION}')

    clock = Clock()  # main clock of game | FPS limit


    def update_fps(fps):
        fps_text = DEFAULT_FONT.render(str(int(fps)), 1, WHITE, (0, 0, 0))
        MAIN_SCREEN.blit(fps_text, (0, 0))


    def max_fps():
        data = {'i': 0, 'max': '0'}

        def calc(fps, dt):
            if data['i'] > 3:
                data['i'] = 0
                data['max'] = '0'
            data['i'] += dt
            if int(data['max']) < fps:
                data['max'] = str(int(fps))
            fps_text = DEFAULT_FONT.render(f"Max:{data['max']}", 1, WHITE, (0, 0, 0))
            MAIN_SCREEN.blit(fps_text, (0, 30))

        return calc


    def min_fps():
        data = {'i': 0, 'min': '999999'}

        def calc(fps, dt):
            if data['i'] > 3:
                data['i'] = 0
                data['min'] = '999999'
            data['i'] += dt
            if int(data['min']) > fps:
                data['min'] = str(int(fps))
            fps_text = DEFAULT_FONT.render(f"Min:{data['min']}", 1, WHITE, (0, 0, 0))
            MAIN_SCREEN.blit(fps_text, (0, 120))

        return calc


    def avg_fps():
        data = {'i': 0, 'avg': [], 'all_avg': []}

        def calc(fps, dt):
            if data['i'] > 5:
                data['i'] = 0
                data['avg'].clear()
            data['i'] += dt
            data['avg'].append(fps)
            data['all_avg'].append(fps)
            avg = sum(data['avg']) // len(data['avg'])
            fps_text = DEFAULT_FONT.render(f"AVG:{str(avg)}", 1, WHITE, (0, 0, 0))
            MAIN_SCREEN.blit(fps_text, (0, 60))

            avg = sum(data['all_avg']) // len(data['all_avg'])
            fps_text = DEFAULT_FONT.render(f"ALL AVG:{str(avg)}", 1, WHITE, (0, 0, 0))
            MAIN_SCREEN.blit(fps_text, (0, 90))

        return calc


    surface = Surface((200, 100), constants.SRCALPHA, 32)
    surface.fill((0, 0, 0, 50))

    surface.convert_alpha()

    display.update(MAIN_SCREEN_RECT)

    STAGES = Stages()
    if __name__ == "__main__":
        G_Clock = GLOBAL_CLOCK
        R_Clock = ROUND_CLOCK
        G_Mouse = GLOBAL_MOUSE
        G_Keyboard = GLOBAL_KEYBOARD

        GAME_BODY = GameBody()
        start = time()

        update_max_fps = max_fps()
        update_min_fps = min_fps()
        update_avg_fps = avg_fps()
        while 1:
            events = EVENT.get()
            finish = time()

            clock.tick(get_fps())
            dt = finish - start
            start = finish
            # update time
            G_Clock.update(dt)
            if STAGES.current_stage == ROUND_STAGE:  # solo game or leave it for animation?
                update_slow_motion(d_time=dt)
                R_Clock.update(dt * get_slow_motion_k())

            # update mouse and keyboard
            G_Mouse.update()
            G_Keyboard.update(events)

            # scroll up and scroll down update
            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 4:
                        G_Mouse.scroll_top = 1
                    elif event.button == 5:
                        G_Mouse.scroll_bot = -1

            GAME_BODY.game_loop()

            # draw.circle(MAIN_SCREEN, (255, 0, 0), (SCREEN_W // 2, SCREEN_H // 2), 5)

            fps = clock.get_fps()

            update_fps(fps)
            update_max_fps(fps, dt)
            update_avg_fps(fps, dt)
            update_min_fps(fps, dt)

            G_Mouse.draw()
            display.update(MAIN_SCREEN_RECT)
            # UPDATE_SCREEN = 1

except Exception as e:
    LOGGER.error('Final fail')
    LOGGER.error(e)
    LOGGER.error(traceback.format_exc())
    LOGGER.error(sys.exc_info()[2])
    # exit(1)
    raise e
