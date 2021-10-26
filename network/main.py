from os import environ
import sys

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame as pg

pg.init()
from settings.window_settings import MAIN_SCREEN as main_screen

from settings.colors import WHITE
from settings.common_settings import DEFAULT_FONT as font
from settings.common_settings import VERSION
import time
pg.display.set_caption(f'Boss Fight V{VERSION}')


def update_fps():
    fps = int(clock.get_fps())
    fps_text = font.render(str(fps), 1, WHITE, (0, 0, 0))

    main_screen.blit(fps_text, (0, 0))


MAX_FPS = 0
MIN_FPS = 400
AVG_FPS = 0
AVG_FPS_i = 0


def get_max_fps(MAX_FPS):
    fps = int(clock.get_fps())
    if fps > MAX_FPS:
        MAX_FPS = fps

    fps_text = font.render(str(MAX_FPS), 1, WHITE, (0, 0, 0))

    main_screen.blit(fps_text, (0, 20))
    return MAX_FPS


def get_min_fps(MIN_FPS):
    fps = int(clock.get_fps())
    if fps < MIN_FPS:
        MIN_FPS = fps

    fps_text = font.render(str(MIN_FPS), 1, WHITE, (0, 0, 0))

    main_screen.blit(fps_text, (0, 50))
    return MIN_FPS


def avg(fps):
    fps_text = font.render(str(fps), 1, WHITE, background=True)

    main_screen.blit(fps_text, (0, 70))


clock = pg.time.Clock()
from player_and_spells.player.player import Player
from common_things.camera import Camera
from player_and_spells.player.simple_player import SimplePlayer as SPlayer
from network.network import Network

net = Network()
camera = Camera(100, 100)
player = Player(100, 100, camera=camera)
player2 = SPlayer(x=100, y=100)


if __name__ == "__main__":
    MIN_FPS = 400

    time_2 = time_1 = time.time()
    while True:
        main_screen.fill((0, 0, 0))
        if MIN_FPS < 50:
            MIN_FPS = 400

        # for y in range(0, SCREEN_H, WALL_CELL_SIZE):
        #     for x in range(0, SCREEN_W, WALL_CELL_SIZE):
        #         pg.draw.circle(main_screen, (255, 255, 155), (x + camera.camera[0], y + camera.camera[1]), 2)

        player.update()

        data = net.send(player.net_data)
        try:
            # data = pickle.loads(data)
            data = data.split(',')
            data = {'pos': data[0:2],
                    'angle': data[2],
                    # 'time': data[3]
                    }
            print(data)
        except:
            player2.update(time_2-time_1, {})
        else:
            player2.update(time_2-time_1, data)

        player2.draw(*camera.camera)
        player.draw()

        update_fps()

        MAX_FPS = get_max_fps(MAX_FPS)
        MIN_FPS = get_min_fps(MIN_FPS)

        dt = clock.tick()

        for eve in pg.event.get():
            if eve.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif eve.type == pg.K_ESCAPE:
                pg.quit()
                sys.exit()

        time_1 = time_2
        time_2 = time.time()
        pg.display.update()
