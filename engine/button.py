from typing import Any, Callable
import pygame
from engine.gameobject import GameObject
from engine.world import World

class Button(GameObject):
    font: pygame.font.Font

    on_click: Callable[[], None]
    
    _is_hovered: bool
    _rendered_text: pygame.Surface

    def __init__(self, text: str, rect: pygame.Rect, font: pygame.font.Font, on_click: Callable[[Any], None] | None = None):
        self.rect = rect
        self.font = font
        self.on_click = on_click
        self._is_hovered = False
        
        self.set_text(text)
        if self.on_click is not None:
            World.events.on('click', self.handle_click)

    def update(self):
        self._is_hovered = self.rect.collidepoint(pygame.mouse.get_pos())

    def render(self, surface: pygame.Surface):
        if self._is_hovered:
            pygame.draw.rect(surface, pygame.Color('red'), self.rect)
        else:
            pygame.draw.rect(surface, pygame.Color('white'), self.rect)
        
        surface.blit(self._rendered_text, self._rendered_text.get_rect(center=self.rect.center))

    def set_text(self, text: str):
        self._rendered_text = self.font.render(text, True, pygame.Color('black'))

    def handle_click(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.on_click(event)