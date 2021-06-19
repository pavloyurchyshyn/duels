from settings.init_pygame import *  # do not remove its ok

from pygame.time import Clock
from pygame import event as EVENT
from pygame import MOUSEBUTTONDOWN
from pygame import display, draw, Surface, constants

from settings.colors import WHITE
from settings.global_parameters import GLOBAL_SETTINGS
from settings.common_settings import DEFAULT_FONT, VERSION
from settings.window_settings import MAIN_SCREEN, MAIN_SCREEN_RECT, SCREEN_H, SCREEN_W  # main screen of all game
from settings.game_stages import ROUND_S, CURRENT_STAGE, START_ROUND_S

from common_things.global_clock import GLOBAL_CLOCK, ROUND_CLOCK
from common_things.global_mouse import GLOBAL_MOUSE
from common_things.global_keyboard import GLOBAL_KEYBOARD

from game_body import GameBody

display.set_caption(f'Boss Fight V{VERSION}')

clock = Clock()  # main clock of game | FPS limit


def update_fps():
    fps_text = DEFAULT_FONT.render(str(int(clock.get_fps())), 1, WHITE, (0, 0, 0))
    MAIN_SCREEN.blit(fps_text, (0, 0))


surface = Surface((200, 100), constants.SRCALPHA, 32)
surface.fill((0, 0, 0, 50))

surface.convert_alpha()

if __name__ == "__main__":
    for y in range(0, SCREEN_H, 50):
        for x in range(0, SCREEN_W, 50):
            draw.circle(MAIN_SCREEN, (255, 255, 155), (x, y), 2)

    G_Clock = GLOBAL_CLOCK
    R_Clock = ROUND_CLOCK
    G_Mouse = GLOBAL_MOUSE
    G_Keyboard = GLOBAL_KEYBOARD

    GAME_BODY = GameBody()

    while 1:
        events = EVENT.get()

        dt = clock.tick() / 1000  # milliseconds to seconds

        # update time
        G_Clock.update(dt)
        if GLOBAL_SETTINGS[CURRENT_STAGE] == ROUND_S:
            R_Clock.update(dt)

        # update mouse and keyboard
        G_Mouse.update()
        G_Keyboard.update()

        MAIN_SCREEN.fill((0, 0, 0))

        # scroll up and scroll down update
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    G_Mouse.scroll_top = 1
                elif event.button == 5:
                    G_Mouse.scroll_bot = -1

        # MAIN_SCREEN.blit(surface, (50, 50))

        GAME_BODY.game_loop()

        update_fps()
        G_Mouse.draw()

        # for y in range(0, SCREEN_H, 50):
        #     for x in range(0, SCREEN_W, 50):
        #         draw.circle(MAIN_SCREEN, (255, 255, 155), (x, y), 2)

        display.update(MAIN_SCREEN_RECT)
        # display.update()
