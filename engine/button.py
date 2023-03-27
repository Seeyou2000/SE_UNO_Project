from typing import Self

import pygame

from engine.event import Event, EventHandler
from engine.gameobject import GameObject


class Button(GameObject):
    font: pygame.font.Font

    on_click: EventHandler | None

    _is_hovered: bool
    _rendered_text: pygame.Surface

    def __init__(
        self: Self,
        text: str,
        rect: pygame.Rect,
        font: pygame.font.Font,
        on_click: EventHandler | None = None,
    ) -> None:
        super().__init__()

        self.rect = rect
        self.font = font
        self.on_click = on_click
        self._is_hovered = False

        self.set_text(text)
        self.on("mouse_down", self.handle_mouse_down)
        self.on("mouse_move", self.handle_mouse_move)
        self.on("mouse_out", self.handle_mouse_out)

    def render(self, surface: pygame.Surface) -> None:
        if self._is_hovered:
            pygame.draw.rect(surface, pygame.Color("red"), self.rect)
        else:
            pygame.draw.rect(surface, pygame.Color("yellow"), self.rect)

        surface.blit(
            self._rendered_text, self._rendered_text.get_rect(center=self.rect.center)
        )

    def set_text(self, text: str) -> None:
        self._rendered_text = self.font.render(text, True, pygame.Color("black"))

    def handle_mouse_down(self, event: Event) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.on_click is None:
                return
            self.on_click(event)
            event.stop_propagation()

    def handle_mouse_move(self, event: Event) -> None:
        if event.target is self:
            return
        if "pos" in event.data:
            self._is_hovered = self.rect.collidepoint(event.data.get("pos"))
        if self._is_hovered:
            e = Event(None)
            e.target = self
            self.parent.emit("mouse_out", e)
            event.stop_propagation()

    def handle_mouse_out(self, event: Event) -> None:
        self._is_hovered = False
