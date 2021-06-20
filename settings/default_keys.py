from pygame.constants import *
import os
from settings.common_settings import SETTINGS_PATH

KEYS_CONFIG_FILE = os.path.join(SETTINGS_PATH, 'keyboard_settings.json')


UP_C = 'up'
DOWN_C = 'down'
LEFT_C = 'left'
RIGHT_C = 'right'

SPRINT_C = 'sprint'
INTERACT_C = 'interact'
RELOAD_C = 'reload'
DROP_C = 'drop'
GRAB_C = 'grab'
SPELL_1_C = 'spell_1'
SPELL_2_C = 'spell_2'

WEAPON_1_C = 'weapon_1'
WEAPON_2_C = 'weapon_2'
WEAPON_3_C = 'weapon_3'

SELF_DAMAGE = 'self_damage'
TEST_MESSAGE = 'test_message'

DEFAULT_GAME_KEYS = {
    UP_C: K_w,
    LEFT_C: K_a,
    RIGHT_C: K_d,
    DOWN_C: K_s,

    RELOAD_C: K_r,

    WEAPON_1_C: K_1,
    WEAPON_2_C: K_2,
    WEAPON_3_C: K_3,

    SPELL_1_C: K_q,

    GRAB_C: K_f,
    DROP_C: K_g,
    INTERACT_C: K_e,

    SPRINT_C: K_LSHIFT,
    SELF_DAMAGE: K_p,
    TEST_MESSAGE: K_o,
}
