# import os
# from settings.common_settings import SETTINGS_PATH

KEYS_CONFIG_FILE = 'keyboard_settings.json'  # os.path.join(SETTINGS_PATH, 'keyboard_settings.json')

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
SPELL_3_C = 'spell_3'

WEAPON_1_C = 'weapon_1'
WEAPON_2_C = 'weapon_2'
WEAPON_3_C = 'weapon_3'

SELF_DAMAGE = 'self_damage'
SELF_REVISE = 'self_revise'
TEST_MESSAGE = 'test_message'

DEFAULT_GAME_KEYS = {
    'w': UP_C,
    'a': LEFT_C,
    'd': RIGHT_C,
    's': DOWN_C,

    '1': WEAPON_1_C,
    '2': WEAPON_2_C,
    #'3': WEAPON_3_C,

    'q': SPELL_1_C,  # q
    'e': SPELL_2_C,  # e
    'space': SPELL_3_C,  # space

    'left shift': SPRINT_C,
    'p': SELF_DAMAGE,
    'o': TEST_MESSAGE,
    'l': SELF_REVISE,
}
