import pygame

from engine.event import Event
from game.settings.settings import Settings


class AudioPlayer:
    def __init__(self, settings: Settings) -> None:
        self.bgm_volume = 1.0
        self.effect_volume = 1.0
        self.volume = 1.0
        pygame.mixer.init()
        # Load background music
        self.bg_music = pygame.mixer.Sound("resources/audio/Uno.mp3")

        # Load sound effect
        self.sound_effect = pygame.mixer.Sound("resources/audio/effectSound.wav")
        self.bg_music_playing = (
            False  # Add a flag to check if the background music is playing
        )

        settings.on("change", self.handle_settings_change)

    def play_bg_music(self):
        # Play background music on loop
        if (
            not self.bg_music_playing
        ):  # Check if the background music is already playing
            self.bg_music.play(-1)
            self.bg_music_playing = True
            self.bg_music.set_volume(self.bgm_volume)

    def stop_bg_music(self):
        # Stop background music
        if self.bg_music_playing:
            self.bg_music.stop()
            self.bg_music_playing = False

    def play_sound_effect(self):
        # self.sound_effect.play()
        self.sound_effect.play(volume=self.effect_volume)

    def play_card_drawn_sound_effect(self):
        # Play sound effect when a card is drawn
        self.sound_effect.play(volume=self.effect_volume)

    def set_volume(self, volume: float):
        self.volume = volume
        self.bg_music.set_volume(self.volume * self.bgm_volume)
        self.sound_effect.set_volume(self.volume * self.effect_volume)

    def set_bgm_volume(self, volume: float):
        self.bgm_volume = volume
        self.bg_music.set_volume(self.volume * self.bgm_volume)

    def set_effect_volume(self, volume: float):
        self.effect_volume = volume
        self.sound_effect.set_volume(self.volume * self.effect_volume)

    def handle_settings_change(self, event: Event):
        settings: Settings = event.target
        self.set_bgm_volume(settings.bgm_volume / 100.0)
        self.set_effect_volume(settings.effect_volume / 100.0)
        self.set_volume(settings.master_volume / 100.0)
