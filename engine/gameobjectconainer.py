import abc
import pygame

from engine.gameobject import GameObject

class GameObjectContainer(abc.ABC):
    children: list[GameObject]

    def __init__(self):
        super().__init__()
        self.children = []

    def update(self):
        for child in self.children:
            child.update()

    def render(self, surface: pygame.Surface):
        for child in self.children:
            child.render(surface)