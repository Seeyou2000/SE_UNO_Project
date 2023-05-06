import pygame

from engine.events.event import Event


class MouseEvent(Event):
    position: pygame.Vector2

    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(None)
        self.position = position
