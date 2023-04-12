import sys

import pygame
import tween

from engine.event import Event
from engine.scene import SceneDirector
from game.settings.settings import Settings


class World:
    screen: pygame.Surface
    director: SceneDirector
    clock: pygame.time.Clock
    target_fps: float
    settings: Settings

    def __init__(self, size: tuple[float, float], target_fps: float = 60) -> None:
        pygame.init()
        self.director = SceneDirector()
        self.set_size(size)
        self.clock = pygame.time.Clock()
        self.target_fps = target_fps
        self.settings = Settings()
        self.settings.on("change", self.handle_settings_change)

    def set_size(self, size: tuple[float, float]) -> None:
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        current_scene = self.director.get_current()
        if current_scene is not None:
            current_scene.emit("resize", Event(None))

    def get_rect(self) -> pygame.Rect:
        return self.screen.get_rect()

    def loop(self) -> None:
        while True:
            self.update()
            self.render()

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
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                case pygame.MOUSEBUTTONDOWN:
                    self.director.get_current().emit(
                        "global_mouse_down", Event(event.dict)
                    )
                case pygame.MOUSEBUTTONUP:
                    self.director.get_current().emit(
                        "global_mouse_up", Event(event.dict)
                    )
                case pygame.MOUSEMOTION:
                    self.director.get_current().emit(
                        "global_mouse_move", Event(event.dict)
                    )
                case pygame.WINDOWRESIZED:
                    event_width = event.dict["x"]
                    event_height = event.dict["y"]
                    clipped_width = max(1280, event_width)
                    clipped_height = max(720, event_height)
                    self.set_size((clipped_width, clipped_height))

    def handle_settings_change(self, _: Event) -> None:
        self.set_size(self.settings.window_size)
