import pygame
import abc

from engine.event import EventEmitter

class GameObject(EventEmitter, abc.ABC):
    rect: pygame.Rect

    def __init__(self):
        super().__init__()

    def update(self):
        pass

    def render(self, surface: pygame.Surface):
        pass