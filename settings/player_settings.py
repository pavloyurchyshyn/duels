from pygame import image, error, transform
from sys import exit
from common_things.img_loader import load_image
import os
PLAYER_HP_BAR_COLOR = (55, 155, 55)

PLAYER_SIZE = 45
PLAYER_HANDS_SIZE = 35
PLAYER_PUSH_FORCE = 20000
PLAYER_SPEED = 550
PLAYER_SPRINT_SPEED = 1.5

PLAYER_STAMINA = 125
PLAYER_STAMINA_LOSE = 5
PLAYER_STAMINA_RESTORE = 1

PLAYER_MASS = 10
PLAYER_GLIDE_K = 1

PLAYER_HP = 100
PLAYER_RAYS_NUM = 60
PLAYER_VISION_RANGE = 300

IDLE_ANIMATION = {}
OTHER_ANIMATIONS = {}

__idle_images = ['sprites/player/idle/idle_0.png', 'sprites/player/idle/idle_1.png',
                 'sprites/player/idle/idle_2.png', 'sprites/player/idle/idle_3.png']
__idle_times = [1.5, 0.2, 0.2, 0.2]

for i, path in enumerate(__idle_images):
    IDLE_ANIMATION[i] = {'frame': load_image(path, (PLAYER_SIZE, PLAYER_SIZE)),
                         'cd': __idle_times[i]}

__rage_images = ['sprites/player/rage/rage_0.png', 'sprites/player/rage/rage_1.png',
                 'sprites/player/rage/rage_2.png', 'sprites/player/rage/rage_3.png',
                 'sprites/player/rage/rage_4.png', 'sprites/player/rage/rage_5.png',
                 ]
__rage_times = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, ]

OTHER_ANIMATIONS['rage'] = {}
for i, path in enumerate(__rage_images):
    OTHER_ANIMATIONS['rage'][i] = {'frame': load_image(path, (PLAYER_SIZE, PLAYER_SIZE)),
                                   'cd': __rage_times[i]}
OTHER_ANIMATIONS['rage']['end'] = 'idle'

try:
    PLAYER_PIC = image.load('sprites/player/player_image.png').convert_alpha()
    # PLAYER_PIC = image.load('sprites/player/player_jojo.png').convert_alpha()
    PLAYER_PIC = transform.smoothscale(PLAYER_PIC, (PLAYER_SIZE, PLAYER_SIZE)).convert_alpha()
except error:
    print('No file sprites/player_image.png')
    exit()

PHRASE_LIFETIME = 5
PHRASES = {
    'full_inventory': {'My inventory  full', },
    'low_hp': {'Low HP', }
}

# ---------------------- FOR BATTLE PREPARE ----------------------
SCALED_IDLE_ANIMATION = {}
SCALE = 2
for i, path in enumerate(__idle_images):
    SCALED_IDLE_ANIMATION[i] = {'frame': load_image(path, (PLAYER_SIZE * SCALE, PLAYER_SIZE * SCALE)),
                                'cd': __idle_times[i]}

try:
    SCALED_PLAYER_PIC = image.load('sprites/player/player_image.png').convert_alpha()
    SCALED_PLAYER_PIC = transform.smoothscale(SCALED_PLAYER_PIC,
                                              (PLAYER_SIZE * SCALE, PLAYER_SIZE * SCALE)).convert_alpha()
except error:
    print('No file sprites/player_image.png')
    exit()

# ---------------------------------------------------------------
