import pygame
from engine.gameobject import GameObject

class Text(GameObject):
    font: pygame.font.Font
    _rendered_text: pygame.Surface
    position: pygame.Vector2
    color: pygame.Color
    
    def __init__(self, text: str, position: pygame.Vector2, font: pygame.font.Font, color: pygame.Color):
        super().__init__()
        self.text = text
        self.position = position
        self.font = font
        self.color = color
        self.set_text(text)

    def render(self, surface: pygame.Surface):
        surface.blit(self._rendered_text, self.position)

    def set_text(self, text: str):
        self._rendered_text = self.font.render(text, True, self.color)