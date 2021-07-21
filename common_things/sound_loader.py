from pygame.mixer import Sound
from pygame.mixer import music as Music

import os
import random
from settings.common_settings import SOUNDS_FOLDER, COMMON_GAME_SETTINGS_JSON_PATH
from settings.default_common_settings import DEFAULT_MUSIC_VOLUME, MUSIC_MUTED, MUSIC_VOLUME
from common_things.save_and_load_json_config import load_json_config, save_json_config

FOLDER_WITH_BACK_MUSIC = os.path.join(SOUNDS_FOLDER, 'back_music')


class MusicPlayer:
    MIN_VOLUME = 0.0
    VOL_STEP = 0.1
    MAX_VOLUME = 1.0 + VOL_STEP

    FADE = 2000

    def __init__(self):
        self.music_set = None
        self.load_back_music_list()

        self.played_list = set()

        settings = load_json_config(COMMON_GAME_SETTINGS_JSON_PATH)

        self._current_song = None
        self._current_song_path = None

        self._volume_lvl = settings.get(MUSIC_VOLUME, DEFAULT_MUSIC_VOLUME)  # sound lvl from 0.0 to 1.0

        self._muted = settings.get(MUSIC_MUTED, 0)
        self._paused = 0

        Music.set_volume(self._volume_lvl)
        self.save_settings()

    def update(self):
        if not Music.get_busy() and not self._muted:
            self.add_second_song()
            self.play_back_music()

    def load_back_music_list(self):
        music_list = filter(lambda file: file.endswith('.mp3') or file.endswith('.wav'),
                            os.listdir(FOLDER_WITH_BACK_MUSIC))
        music_list = map(lambda music: os.path.abspath(os.path.join(FOLDER_WITH_BACK_MUSIC, music)), music_list)
        music_list = set(music_list)

        self.music_set = music_list

    def add_second_song(self):
        if not self.music_set:
            self.music_set = self.played_list.copy()
            self.played_list.clear()

        if not self.music_set:
            self._current_song_path = None
            return

        second_comp = self.music_set.pop()
        self.played_list.add(second_comp)
        self._current_song = os.path.basename(second_comp)
        self._current_song_path = second_comp

    def save_settings(self):
        config = load_json_config(COMMON_GAME_SETTINGS_JSON_PATH)
        config[MUSIC_VOLUME] = self._volume_lvl
        config[MUSIC_MUTED] = self._muted
        save_json_config(config, COMMON_GAME_SETTINGS_JSON_PATH)

    def play_back_music(self):
        if self._current_song_path and not self._muted:
            Music.load(self._current_song_path)
            Music.play(fade_ms=MusicPlayer.FADE)

    def pause_back_music(self):
        Music.pause()
        self._paused = 1

    def resume_back_music(self):
        Music.unpause()
        self._paused = 0

    def stop_back_music(self):
        Music.stop()

    def add_volume(self):
        self._muted = 0
        if self._paused:
            self.resume_back_music()

        self._volume_lvl += self.VOL_STEP
        if self._volume_lvl > self.MAX_VOLUME:
            self._volume_lvl = self.MAX_VOLUME

        Music.set_volume(self._volume_lvl)
        self.save_settings()

    def minus_volume(self):
        self._volume_lvl -= self.VOL_STEP
        if self._volume_lvl < self.MIN_VOLUME or self._volume_lvl < self.VOL_STEP:
            self._volume_lvl = self.MIN_VOLUME

        Music.set_volume(self._volume_lvl)
        self.save_settings()

    def mute(self):
        self._muted = 1
        self.pause_back_music()
        self.save_settings()

    def unmute(self):
        self._muted = 0
        self.resume_back_music()
        self.save_settings()

    @property
    def current_song(self):
        return self._current_song
    @staticmethod
    def load_sound(path):
        return Sound(os.path.join(SOUNDS_FOLDER, path))

    @property
    def volume(self):
        return self._volume_lvl

    @property
    def volume_stages(self):
        return (self.MAX_VOLUME - self.MIN_VOLUME) // self.VOL_STEP + 1

    @property
    def volume_stage(self):
        return int((self.MAX_VOLUME - self.MIN_VOLUME) // self.VOL_STEP * self._volume_lvl)

    @property
    def muted(self):
        return self._muted


GLOBAL_MUSIC_PLAYER = MusicPlayer()
