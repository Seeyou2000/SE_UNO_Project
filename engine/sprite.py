import pygame

from engine.gameobject import GameObject

class Sprite(GameObject):
    image: pygame.Surface

    def __init__(self, surface: pygame.Surface):
        super().__init__()
        self.image = surface
        self.rect = surface.get_rect()

    def render(self, surface: pygame.Surface):
        super().render(surface)
        surface.blit(self.image, self.rect)
    