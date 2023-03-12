import pygame
import abc

class GameObject(abc.ABC):
    rect: pygame.Rect

    def __init__(self):
        pass

    def update(self):
        pass

    def render(self, surface: pygame.Surface):
        pass