
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
    UP_C: 119,
    LEFT_C: 97,
    RIGHT_C: 100,
    DOWN_C: 115,

    RELOAD_C: 114,

    WEAPON_1_C: 49,
    WEAPON_2_C: 50,
    WEAPON_3_C: 51,

    SPELL_1_C: 113,

    GRAB_C: 102,
    DROP_C: 103,
    INTERACT_C: 101,

    SPRINT_C: 1073742049,
    SELF_DAMAGE: 112,
    TEST_MESSAGE: 111,
}
