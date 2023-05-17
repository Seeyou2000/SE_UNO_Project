import pygame

from engine.events.event import Event
from engine.focus import Focusable
from engine.gameobjectcontainer import GameObjectContainer
from engine.text import Text


class Checkbox(GameObjectContainer, Focusable):
    def __init__(
        self, rect: pygame.Rect, font: pygame.font.Font
    ) -> None:
        super().__init__()

        self.rect = rect.copy()
        self.font = font
        self.is_checked = False

        self.check = Text("V", pygame.Vector2(0, 0), self.font, pygame.Color("white"))
        self.add_child(self.check)
        self.check.rect.center = pygame.Rect(0, 0, rect.width, rect.height).center
        self.toggle_v()

        self.on("click", self.toggle_checked)

    def render(self, surface: pygame.Surface) -> None:
        if not self.is_visible:
            return
        if self.is_checked:
            pygame.draw.rect(
                surface,
                pygame.Color("#ff8114"),
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
        pygame.draw.rect(
            surface,
            pygame.Color("#ffe1c7"),
            self.absolute_rect,
            border_radius=8,
            width=2
        )
        super().render(surface)

    def toggle_v(self) -> None:
        self.check.is_visible = self.is_checked

    def toggle_checked(self, event: Event) -> None:
        if self.is_checked:
            self.is_checked = False
        else:
            self.is_checked = True
        self.toggle_v()
