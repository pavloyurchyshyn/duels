from game_tests.window_for_tests import *

from obj_properties.rect_form import Rectangle
from obj_properties.circle_form import Circle
from obj_properties.line import Line

from settings.global_parameters import test_draw_status_is_on, SET_CLIENT_INSTANCE
from pygame.draw import circle as draw_circle
from pygame.draw import line as draw_line
from math import radians

G_Clock = GLOBAL_CLOCK
G_Mouse = GLOBAL_MOUSE

circle = Circle(500, 500, 50)
rect = Rectangle(100, 100, 100)
line = Line([60, 60], length=220, angle=radians(45))
sec_line = Line([300, 310], length=150, angle=radians(45))
third_line = Line([300, 300], length=150, angle=0)
f_line = Line([300, 320], length=150, angle=radians(90))

obj_list = [circle, rect, line]
obj_index = 0

SET_CLIENT_INSTANCE(1)

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
    dx, dy = G_Mouse.rel

    draw.circle(MAIN_SCREEN, (200, 200, 200), G_Mouse.pos, 5)
    update_fps()
    keys = KEY.get_pressed()

    for x, y in rect.dots:
        draw_circle(MAIN_SCREEN, (0, 255, 0), (x, y), 1)

    for x, y in circle.dots:
        draw_circle(MAIN_SCREEN, (255, 255, 0), (x, y), 1)


    if l:
        line._change_position(G_Mouse.pos)

    if r:
        # from common_things.common_functions import get_angle_between_dots

        line._change_position(xy1=G_Mouse.pos)
        # print(get_angle_between_dots(line.dots[1], line.dots[0]), get_angle_between_dots(line.dots[0], line.dots[1]))

        # sec_line._change_position(G_Mouse.pos, angle=get_angle_between_dots(*line.dots), length=50)

    draw_line(MAIN_SCREEN, (255, 0, 0), *line.dots, 1)

    draw_line(MAIN_SCREEN, (0, 255, 255), *sec_line.dots, 1)

    draw_line(MAIN_SCREEN, (0, 255, 55), *third_line.dots, 1)
    draw_line(MAIN_SCREEN, (255, 0, 0), *f_line.dots, 1)

    # if line.collide_line(sec_line):
    #     print(2)
    # if line.collide_line(third_line):
    #     print(3)
    if rect.collide(line):
        print('rect')
    if line.collide_circle(circle._center, circle._size):
        print('circle')

    if line.collide_line(f_line):
        print(1)
        # draw_circle(MAIN_SCREEN, (255, 255, 0), line.collide_line(f_line), 5)
    if line.collide_line(sec_line):
        print(2)

    if line.collide_line(third_line):
        print(3)

    for ll in (line, sec_line, third_line, f_line):
        draw_circle(MAIN_SCREEN, (0, 255, 0), ll.first_dot, 3)
        draw_circle(MAIN_SCREEN, (0, 0, 255), ll.second_dot, 3)
        if ll.collide_point(G_Mouse.pos):
            draw_circle(MAIN_SCREEN, (255, 0, 0), G_Mouse.pos, 5)

    if keys[K_ESCAPE]:
        PY_QUIT()
        SYS_EXIT()

    display.update(MAIN_SCREEN_RECT)
