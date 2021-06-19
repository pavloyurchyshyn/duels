from pygame.mixer import Sound
from pygame.mixer import music as Music

import os
import random
from settings.global_parameters import SOUNDS_FOLDER
from settings.global_parameters import SETTINGS_PATH


FOLDER_WITH_BACK_MUSIC = os.path.join(SOUNDS_FOLDER, 'back_music')


def load_sound(path):
    return Sound(os.path.join(SOUNDS_FOLDER, path))


class MusicPlayer:
    MAX_VOLUME = 1.0
    MIN_VOLUME = 0.0
    VOL_STEP = 0.1

    FADE = 2000

    def __init__(self):
        self.music_set = None
        self.load_back_music_list()

        self.played_list = set()

        self._current_song = None
        self._current_song_path = None

        self._volume_lvl = 1.0  # sound lvl from 0.0 to 1.0
        Music.set_volume(self._volume_lvl)

    def update(self):
        if not Music.get_busy():
            self.add_second_song()
            self.play_back_music()

    def load_back_music_list(self):
        music_list = filter(lambda file: file.endswith('.mp3') or file.endswith('.wav'), os.listdir(FOLDER_WITH_BACK_MUSIC))
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

    def play_back_music(self):
        if self._current_song_path:
            Music.load(self._current_song_path)
            Music.play(fade_ms=MusicPlayer.FADE)

    def pause_back_music(self):
        Music.pause()

    def resume_back_music(self):
        Music.unpause()

    def stop_back_music(self):
        Music.stop()

    def add_volume(self):
        self._volume_lvl += self.VOL_STEP
        if self._volume_lvl > self.MAX_VOLUME:
            self._volume_lvl = self.MAX_VOLUME

    def minus_volume(self):
        self._volume_lvl -= self.VOL_STEP
        if self._volume_lvl < self.MIN_VOLUME:
            self._volume_lvl = self.MIN_VOLUME

    def __del__(self):
        pass
        # if Music.get_busy():
        #     Music.stop()

        #Music.unload()

GLOBAL_MUSIC_PLAYER = MusicPlayer()
