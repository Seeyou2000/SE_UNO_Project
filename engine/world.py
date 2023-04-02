import sys

import pygame

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

    def set_size(self, size: tuple[float, float]) -> None:
        self.screen = pygame.display.set_mode(size)

    def get_rect(self) -> pygame.Rect:
        return self.screen.get_rect()

    def loop(self) -> None:
        while True:
            self.update()
            self.render()

    def update(self) -> None:
        self.handle_event()
        self.director.get_current().update()
        self.clock.tick(self.target_fps)

    def render(self) -> None:
        self.screen.fill(pygame.Color("white"))
        self.director.get_current().render(self.screen)
        pygame.display.flip()

    def handle_event(self) -> None:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                case pygame.MOUSEBUTTONDOWN:
                    self.director.get_current().emit("mouse_down", Event(event.dict))
                case pygame.MOUSEMOTION:
                    self.director.get_current().emit("mouse_move", Event(event.dict))
