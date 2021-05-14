from settings.arena_settings import STANDARD_ARENA_CELL_SIZE, STANDARD_ARENA_BORDER_SIZE, \
    ELEMENT_SIZE, SUB_CELL_SIZE
from pygame import Rect, draw
import time
from obj_properties.rect_form import Rectangle

rects = []
start = time.time()

for x in range(0, STANDARD_ARENA_CELL_SIZE, ELEMENT_SIZE):
    for y in range(0, STANDARD_ARENA_CELL_SIZE, ELEMENT_SIZE):
        rects.append(Rect((x, y), (ELEMENT_SIZE, ELEMENT_SIZE)))

print(time.time() - start)

rects = []
start = time.time()

for x in range(0, STANDARD_ARENA_CELL_SIZE, ELEMENT_SIZE):
    for y in range(0, STANDARD_ARENA_CELL_SIZE, ELEMENT_SIZE):
        rects.append(Rectangle(x, y, ELEMENT_SIZE, ELEMENT_SIZE))

print(time.time() - start)



num = 200000
start = time.time()
a = Rect((0, 0), (100, 100))
b = Rect((0, 0), (100, 100))

res = [a.colliderect(b) for _ in range(num)]

print(time.time() - start)

start = time.time()
a = Rectangle(0, 0, 100, 100)
b = Rectangle(0, 0, 100, 100)

res = [a.collide_dots(b) for _ in range(num)]

print(time.time() - start)