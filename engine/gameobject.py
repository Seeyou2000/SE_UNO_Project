import abc

import pygame

from engine.event import EventEmitter


class GameObject(EventEmitter, abc.ABC):
    rect: pygame.Rect

    def __init__(self) -> None:
        super().__init__()

    def update(self) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        pass
