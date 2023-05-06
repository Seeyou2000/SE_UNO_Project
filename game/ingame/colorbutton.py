import pygame

from engine.button import ButtonSurfaces, SpriteButton
from engine.events.emitter import EventHandler
from game.gameplay.cardentitiy import get_card_color
from game.settings.settings import Settings
from game.surfaceutil import darken, lighten


class ColorButton(SpriteButton):
    def __init__(
        self, rect: pygame.Rect, color: str, settings: Settings, on_click: EventHandler
    ) -> None:
        surface_rect = pygame.Rect(0, 0, rect.width, rect.height)
        surface = pygame.Surface(surface_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            surface, pygame.Color("#FFF6EF"), surface_rect, border_radius=20
        )
        pygame.draw.rect(
            surface,
            get_card_color(color, settings.is_colorblind),
            surface_rect.inflate(-8, -8),
            border_radius=16,
        )

        super().__init__(
            ButtonSurfaces(surface, lighten(surface, 30), darken(surface, 30)), on_click
        )
        self.rect = rect
