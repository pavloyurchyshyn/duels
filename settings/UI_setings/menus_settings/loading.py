from settings.colors import PLAYERS_COLORS
from settings.players_settings.player_settings import PLAYER_SIZE
from settings.common_settings import COMMON_GAME_SETTINGS_JSON_PATH as CGSJP
from common_things.save_and_load_json_config import get_parameter_from_json_config
from player.simple_player import SimplePlayer
from settings.screen_size import HALF_SCREEN_H, HALF_SCREEN_W

__player_color = get_parameter_from_json_config('player_skin', CGSJP, def_value=PLAYERS_COLORS['blue'])
PLAYER_PIC = SimplePlayer(HALF_SCREEN_W, HALF_SCREEN_H,
                          turn_off_camera=True,
                          size=PLAYER_SIZE * 5,
                          add_self_to_list=0,
                          player_color=__player_color, follow_mouse=1,
                          draw_health_points=False, arena=None)
