from pygame.draw import rect as draw_rect
from pygame.draw import line as draw_line
from pygame.rect import Rect

from UI.UI_base.progress_bar_UI import ProgressBar
from UI.UI_base.animation import Animation

from common_things.sprites_functions import get_surface
from UI.font_loader import DEFAULT_FONT

from settings.UI_setings.player_bot_bar_settigns import BAR_X_SIZE, BAR_Y_SIZE
from settings.window_settings import MAIN_SCREEN
from settings.screen_size import X_SCALE, Y_SCALE, SCREEN_H, SCREEN_W

from player.base.base_player import BasePlayer
from player.base_visual.player_images import PlayerImagesManager


class PlayerBotBar:
    X_SIZE = BAR_X_SIZE * X_SCALE
    Y_SIZE = BAR_Y_SIZE * Y_SCALE
    X_POSITION = SCREEN_W // 2 - X_SIZE // 2
    Y_POSITION = SCREEN_H - Y_SIZE

    PORTRAIT_X_POS = X_POSITION
    PORTRAIT_Y_POS = Y_POSITION
    PORTRAIT_X_SIZE = int(70 * X_SCALE)
    PORTRAIT_X_SIZE_MID = PORTRAIT_X_SIZE // 2
    PORTRAIT_Y_SIZE = int(85 * Y_SCALE)
    PORTRAIT_Y_SIZE_MID = PORTRAIT_Y_SIZE // 2

    HP_BAR_X_SIZE = X_SIZE * 0.6 * X_SCALE
    HP_BAR_Y_SIZE = 10 * Y_SCALE
    HP_BAR_X_POS = X_POSITION + PORTRAIT_X_SIZE + HP_BAR_X_SIZE * 0.05
    HP_BAR_Y_POS = Y_POSITION + 10 * Y_SCALE

    WEAPON_ICON_START_X_POS = HP_BAR_X_POS
    WEAPON_ICON_START_Y_POS = HP_BAR_Y_POS + 20 * Y_SCALE
    WEAPON_ICON_Y_SIZE = WEAPON_ICON_X_SIZE = 70 * X_SCALE

    SPELL_ICON_START_Y_POS = HP_BAR_Y_POS + 20 * Y_SCALE
    SPELL_ICON_Y_SIZE = SPELL_ICON_X_SIZE = 50 * X_SCALE

    LOADED_SKINS = {}
    IMAGE_MANAGER = PlayerImagesManager(PORTRAIT_X_SIZE, angle=360)

    def __init__(self, player):
        self._player: BasePlayer = player
        self._surface = get_surface(self.X_SIZE, self.Y_SIZE, color=(100, 100, 200, 255), transparent=1)
        self._player_hp_bar = ProgressBar(stage=self._player.health_points,
                                          border_radius=10, out_border_radius=10,
                                          bar_x_size=self.HP_BAR_X_SIZE, bar_y_size=self.HP_BAR_Y_SIZE,
                                          stages_num=self._player.full_health_points, scale=0,
                                          bar_pos=(self.HP_BAR_X_POS, self.HP_BAR_Y_POS),
                                          )

        self.player_portrait_rect = (self.PORTRAIT_X_POS, self.PORTRAIT_Y_POS), (
            self.PORTRAIT_X_SIZE, self.PORTRAIT_Y_SIZE)

        self.spell_fade_surface = get_surface(self.SPELL_ICON_X_SIZE, self.SPELL_ICON_Y_SIZE,
                                              transparent=1, color=(50, 50, 50, 150))
        self.weapon_fade_surface = get_surface(self.WEAPON_ICON_X_SIZE, self.WEAPON_ICON_Y_SIZE,
                                               transparent=1, color=(50, 50, 50, 150))

        self.weapons = []
        self.spells = []
        self.current_skin = None
        self.follow_player(player)

        self.build()

    def follow_player(self, player):
        self._player = player
        color = (tuple(player._visual_part._body_color), tuple(player._visual_part._face_color))
        if color not in PlayerBotBar.LOADED_SKINS:
            skin = PlayerBotBar.IMAGE_MANAGER.get_new_skin(color)
            idle_anim, other_anim = skin['idle_animation'], skin['other_animation']
            skin['face'] = Animation((self.PORTRAIT_X_POS, self.PORTRAIT_Y_POS),
                                     idle_frames=idle_anim, **other_anim)
            PlayerBotBar.LOADED_SKINS[color] = skin

        skin = PlayerBotBar.LOADED_SKINS[color]
        self.current_skin = skin

    def build(self):
        self.weapons = []
        self.spells = []

        start_ = self.WEAPON_ICON_START_X_POS

        for weapon in self._player._weapon.values():
            if weapon:
                self.weapons.append({
                    'img': weapon.ICON,
                    'weapon': weapon,
                    'rect': Rect((start_, self.WEAPON_ICON_START_Y_POS),
                                 (self.WEAPON_ICON_X_SIZE + 1, self.WEAPON_ICON_Y_SIZE + 1))
                })
            start_ += int(self.WEAPON_ICON_X_SIZE * 1.1)

        self._separate_line = ((start_, int(self.WEAPON_ICON_START_Y_POS)),
                               (start_, int(self.WEAPON_ICON_START_Y_POS + self.WEAPON_ICON_Y_SIZE)))

        start_ = int(start_ + self.WEAPON_ICON_X_SIZE * 0.1)

        for spell in self._player.spells.values():
            if spell:
                self.spells.append({
                    'img': spell.ICON,
                    'spell': spell,
                    'rect': Rect((start_, self.SPELL_ICON_START_Y_POS),
                                 (self.SPELL_ICON_X_SIZE + 1, self.SPELL_ICON_Y_SIZE + 1))
                })

                start_ += int(self.SPELL_ICON_X_SIZE * 1.1)

    def update(self):
        hp = self._player.health_points
        self._player_hp_bar.update(current_stage=hp if hp > 0.0 else 0.0, stages_num=self._player.full_health_points)

    def _draw_icons(self):
        for weapon in self.weapons:
            MAIN_SCREEN.blit(weapon['img'], weapon['rect'].topleft)
            if weapon['weapon'].on_cooldown:
                MAIN_SCREEN.blit(self.weapon_fade_surface, weapon['rect'].topleft)

                text = DEFAULT_FONT.render(str(round(abs(weapon['weapon'].cooldown), 1)), 1, (255, 255, 255))
                x, y = weapon['rect'].center
                MAIN_SCREEN.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

            draw_rect(MAIN_SCREEN, (255, 255, 255), weapon['rect'], 5)

        draw_line(MAIN_SCREEN, (255, 255, 255), *self._separate_line, 2)

        for spell in self.spells:
            MAIN_SCREEN.blit(spell['img'], spell['rect'].topleft)

            if spell['spell'].on_cooldown:
                MAIN_SCREEN.blit(self.spell_fade_surface, spell['rect'].topleft)

                text = DEFAULT_FONT.render(str(round(abs(spell['spell'].cooldown), 1)), 1, (255, 255, 255))
                x, y = spell['rect'].center
                MAIN_SCREEN.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

            draw_rect(MAIN_SCREEN, (255, 255, 255), spell['rect'], 5)

    def draw(self):
        MAIN_SCREEN.blit(self.current_skin['body'], self.player_portrait_rect)
        face_frame = self.current_skin['face'].animations[self._player._visual_part.face_animation.current_anim][self._player._visual_part.face_animation.frame]['frame']
        MAIN_SCREEN.blit(face_frame, self.player_portrait_rect)

        draw_rect(MAIN_SCREEN, (255, 255, 255), self.player_portrait_rect, 2, 5)

        self._draw_icons()

        self._player_hp_bar.draw()
