import asyncio
import sys

import pygame
import tween

from engine.events.event import Event
from engine.scene import SceneDirector
from game.achievements import Achievements
from game.audio_player import AudioPlayer
from game.settings.settings import Settings
from game.storyclearstatus import StoryClearStatus
from network.client.client import clientio

AUDIO_PLAYER: AudioPlayer = AudioPlayer()


class World:
    screen: pygame.Surface
    director: SceneDirector
    clock: pygame.time.Clock
    target_fps: float
    settings: Settings
    achievements: Achievements
    story_clear_status: StoryClearStatus

    def __init__(self, size: tuple[float, float], target_fps: float = 60) -> None:
        pygame.init()
        self.director = SceneDirector()
        self.set_size(size)
        self.clock = pygame.time.Clock()
        self.target_fps = target_fps
        self.settings = Settings()
        self.settings.on("change", self.handle_settings_change)

        global AUDIO_PLAYER
        AUDIO_PLAYER.play_bg_music()
        self.settings.on("change", AUDIO_PLAYER.handle_settings_change)

        self.audio_player = AUDIO_PLAYER
        self.achievements = Achievements()
        self.story_clear_status = StoryClearStatus()

        pygame.scrap.init()
        pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)

    def set_size(self, size: tuple[float, float]) -> None:
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        current_scene = self.director.get_current()
        if current_scene is not None:
            current_scene.emit("resize", Event(None))

    def get_rect(self) -> pygame.Rect:
        return self.screen.get_rect()

    async def loop(self, _: any) -> None:
        while True:
            self.update()
            self.render()
            await asyncio.sleep(0)

    def update(self) -> None:
        self.handle_event()
        dt = self.clock.tick(self.target_fps) / 1000.0
        self.director.get_current().update(dt)
        tween.update(dt)

    def render(self) -> None:
        self.screen.fill(pygame.Color("#FFF6EF"))
        self.director.get_current().render(self.screen)
        pygame.display.flip()

    def handle_event(self) -> None:
        current_scene = self.director.get_current()
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.exit()
                case pygame.MOUSEBUTTONDOWN:
                    current_scene.event_system.handle_mouse_down(event)
                case pygame.MOUSEBUTTONUP:
                    current_scene.event_system.handle_mouse_up(event)
                case pygame.MOUSEMOTION:
                    current_scene.event_system.handle_mouse_move(event)
                case pygame.KEYDOWN:
                    current_scene.emit("keydown", Event(event.dict))
                case pygame.TEXTEDITING:
                    current_scene.emit("textediting", Event(event.dict))
                case pygame.TEXTINPUT:
                    current_scene.emit("textinput", Event(event.dict))
                case pygame.WINDOWRESIZED:
                    event_width = event.dict["x"]
                    event_height = event.dict["y"]
                    clipped_width = max(1280, event_width)
                    clipped_height = max(720, event_height)
                    self.set_size((clipped_width, clipped_height))

    def handle_settings_change(self, _: Event) -> None:
        self.set_size(self.settings.window_size)

    def exit(self) -> None:
        clientio.disconnect()
        pygame.quit()
        sys.exit()
