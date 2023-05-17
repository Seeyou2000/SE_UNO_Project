import pygame

from engine.events.event import Event
from engine.focus import Focusable
from engine.gameobjectcontainer import GameObjectContainer
from engine.layout import Layout, LayoutAnchor
from engine.text import Text


class Checkbox(GameObjectContainer, Focusable):
    def __init__(
        self, rect: pygame.Rect, font: pygame.font.Font, color: pygame.Color
    ) -> None:
        super().__init__()

        self.rect = rect.copy()
        self.font = font
        self.color = color
        self.layout = Layout(self.rect)
        self.is_checked = False
        self.on("click", self.toggle_checked)
        self.check = Text("V", pygame.Vector2(0, 0), self.font, self.color)
        self.layout.add(self.check, LayoutAnchor.CENTER, pygame.Vector2(0, 0))
        self.toggle_v()
        self.layout.update(0)

    def render(self, surface: pygame.Surface) -> None:
        if self.is_checked:
            pygame.draw.rect(
                surface,
                pygame.Color("#ffffff"),
                self.absolute_rect,
                border_radius=8,
            )
        else:
            pygame.draw.rect(
                surface,
                pygame.Color("#ffffff"),
                self.absolute_rect,
                border_radius=8,
            )
        super().render(surface)

    def toggle_v(self) -> None:
        if self.is_checked:
            if not self.has_child(self.check):
                self.add_child(self.check)
        else:
            if self.has_child(self.check):
                self.remove_child(self.check)

    def toggle_checked(self, event: Event) -> None:
        if self.is_checked:
            self.is_checked = False
        else:
            self.is_checked = True
        self.toggle_v()
