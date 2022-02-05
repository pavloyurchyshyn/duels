KEYS_CONFIG_FILE = 'keyboard_config.json'

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

DEFAULT_COMMAND_KEY = {
    UP_C: 'w',
    LEFT_C: 'a',
    RIGHT_C: 'd',
    DOWN_C: 's',

    WEAPON_1_C: '1',
    WEAPON_2_C: '2',
    # WEAPON_3_C: '3',

    SPELL_1_C: 'q',
    SPELL_2_C: 'e',
    SPELL_3_C: 'space',

    SPRINT_C: 'left shift',
    SELF_DAMAGE: 'p',
    TEST_MESSAGE: 'o',
    SELF_REVISE: 'l',
}

TEXT_TO_RAW = {
    ' ': 'space',
    SPELL_3_C: 'space',

    SPRINT_C: 'left shift',
}