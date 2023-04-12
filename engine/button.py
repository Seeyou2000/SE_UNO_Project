from typing import Self

import pygame
from attr import dataclass

from engine.event import EventHandler
from engine.gameobject import GameObject


@dataclass
class ButtonSurfaces:
    normal: pygame.Surface
    hover: pygame.Surface
    pressed: pygame.Surface


class BaseButton(GameObject):
    font: pygame.font.Font
    on_click: EventHandler | None

    surfaces: ButtonSurfaces

    def __init__(
        self: Self,
        rect: pygame.Rect,
        surfaces: ButtonSurfaces,
        on_click: EventHandler | None = None,
    ) -> None:
        super().__init__()

        self.rect = rect
        self.surfaces = surfaces

        if on_click is not None:
            self.on("click", on_click)

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)

        button_surface = self.surfaces.normal
        if self._is_pressed:
            button_surface = self.surfaces.pressed
        elif self._is_hovered:
            button_surface = self.surfaces.hover

        surface.blit(button_surface, self.absolute_rect)


class Button(BaseButton):
    def __init__(
        self: Self,
        text: str,
        rect: pygame.Rect,
        font: pygame.font.Font,
        on_click: EventHandler | None = None,
    ) -> None:
        normal_surface = pygame.Surface(rect.size)
        normal_surface.fill(pygame.Color("#fff1e7"))

        hover_surface = normal_surface.copy()
        hover_surface.fill(pygame.Color("#ffe8d7"))

        pressed_surface = normal_surface.copy()
        pressed_surface.fill(pygame.Color("#ffdcc3"))
        super().__init__(
            rect,
            ButtonSurfaces(normal_surface, hover_surface, pressed_surface),
            on_click,
        )

        self.font = font
        self.set_text(text)

    def set_text(self, text: str) -> None:
        self._rendered_text = self.font.render(text, True, pygame.Color("#451e11"))

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)
        surface.blit(
            self._rendered_text,
            self._rendered_text.get_rect(center=self.absolute_rect.center),
        )


class SpriteButton(BaseButton):
    def __init__(
        self: Self, surfaces: ButtonSurfaces, on_click: EventHandler | None = None
    ) -> None:
        super().__init__(surfaces.normal.get_rect(), surfaces, on_click)
