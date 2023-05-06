import pygame

from engine.events.event import Event
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
        self.effect_uno_clicked = pygame.mixer.Sound("resources/audio/uno_clicked.wav")
        self.effect_card_sliding = pygame.mixer.Sound(
            "resources/audio/card_sliding_sound.wav"
        )
        self.effect_card_playing = pygame.mixer.Sound(
            "resources/audio/card_playing_sound.wav"
        )
        self.bg_music_playing = (
            False  # Add a flag to check if the background music is playing
        )

        settings.on("change", self.handle_settings_change)

    def play_bg_music(self) -> None:
        # Play background music on loop
        if (
            not self.bg_music_playing
        ):  # Check if the background music is already playing
            self.bg_music.play(-1)
            self.bg_music_playing = True
            self.bg_music.set_volume(self.volume)

    def stop_bg_music(self) -> None:
        # Stop background music
        if self.bg_music_playing:
            self.bg_music.stop()
            self.bg_music_playing = False

    def play_effect_uno_clicked(self) -> None:
        self.effect_uno_clicked.play()

    def play_effect_card_sliding(self) -> None:
        self.effect_card_sliding.play()

    def play_effect_card_playing(self) -> None:
        self.effect_card_playing.play()

    def set_volume(self, volume: float) -> None:
        self.volume = volume
        self.set_bgm_volume(self.volume)
        self.set_effect_volume(self.volume)

    def set_bgm_volume(self, volume: float) -> None:
        self.bgm_volume = volume
        self.bg_music.set_volume(self.volume * self.bgm_volume)

    def set_effect_volume(self, volume: float) -> None:
        self.effect_volume = volume
        self.effect_uno_clicked.set_volume(self.volume * self.effect_volume)
        self.effect_card_sliding.set_volume(self.volume * self.effect_volume)
        self.effect_card_playing.set_volume(self.volume * self.effect_volume)

    def handle_settings_change(self, event: Event) -> None:
        settings: Settings = event.target
        self.set_volume(settings.master_volume / 100.0)
        self.set_bgm_volume(settings.bgm_volume / 100.0)
        self.set_effect_volume(settings.effect_volume / 100.0)
