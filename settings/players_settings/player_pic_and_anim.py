from settings.players_settings.player_settings import PLAYER_SIZE

PLAYER_SIZE = PLAYER_SIZE * 2

IDLE_IMAGES = ('sprites/player/idle/idle_0.png', 'sprites/player/idle/idle_1.png',
               'sprites/player/idle/idle_2.png', 'sprites/player/idle/idle_3.png')
IDLE_TIMES = (1.5, 0.2, 0.2, 0.2)

RAGE_IMAGES = ('sprites/player/rage/rage_0.png', 'sprites/player/rage/rage_1.png',
               'sprites/player/rage/rage_2.png', 'sprites/player/rage/rage_3.png',
               'sprites/player/rage/rage_4.png', 'sprites/player/rage/rage_5.png',)
RAGE_TIMES = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1,)

DYING_IMAGES = ('sprites/player/to_death/to_death_0.png', 'sprites/player/to_death/to_death_1.png',
                'sprites/player/to_death/to_death_2.png', 'sprites/player/to_death/to_death_3.png',
                'sprites/player/to_death/to_death_4.png')
DYING_TIMES = (0.2, 0.2, 0.2, 0.2, 0.5)

DEAD_IMAGES = ('sprites/player/dead/dead_0.png', 'sprites/player/dead/dead_1.png',
               'sprites/player/dead/dead_2.png',)
DEAD_TIMES = (0.2, 0.2, 0.2,)

BODY_IMAGE = 'sprites/player/player_image.png'
CIRCLE_IMAGE = 'sprites/player/player_circle.png'

ANIM_RAGE_K = 'rage'
ANIM_IDLE_K = 'idle'
ANIM_DYING_K = 'dying'
ANIM_DEAD_K = 'dead'
