import pygame
import sys
from engine.event import EventEmiiter
from engine.scene import SceneDirector

class World():
    events: EventEmiiter = EventEmiiter()

    screen: pygame.Surface
    director: SceneDirector
    clock: pygame.time.Clock
    target_fps: float

    def __init__(self, size: tuple[float, float], target_fps: float = 60):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.director = SceneDirector()
        self.clock = pygame.time.Clock()
        self.target_fps = target_fps

    def loop(self):
        while True:
            self.update()
            self.render()

    def update(self):
        self.handle_event()
        self.director.get_current().update()
        self.clock.tick(self.target_fps)

    def render(self):
        self.screen.fill(pygame.Color('black'))
        self.director.get_current().render(self.screen)
        pygame.display.flip()

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                World.events.emit('click', event)
                