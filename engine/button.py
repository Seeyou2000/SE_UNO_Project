from typing import Self

import pygame
from attr import dataclass

from engine.event import Event, EventHandler
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
    _override_surface: pygame.Surface

    def __init__(
        self: Self,
        rect: pygame.Rect,
        surfaces: ButtonSurfaces,
        on_click: EventHandler | None = None,
    ) -> None:
        super().__init__()

        self.rect = rect
        self.surfaces = surfaces
        self._override_surface = None

        if on_click is not None:
            self.on("click", on_click)

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)

        button_surface = None
        if self._override_surface is not None:
            button_surface = self._override_surface
        else:
            button_surface = self.surfaces.normal
            if self._is_pressed:
                button_surface = self.surfaces.pressed
            elif self._is_hovered:
                button_surface = self.surfaces.hover

        surface.blit(
            button_surface, button_surface.get_rect(center=self.absolute_rect.center)
        )


class Button(BaseButton):
    has_focus: bool

    def __init__(
        self,
        text: str,
        rect: pygame.Rect,
        font: pygame.font.Font,
        on_click: EventHandler | None = None,
    ) -> None:
        self.has_focus = False
        border_radius = 10
        normal_rect = rect.inflate(-4, -4)
        normal_surface = pygame.Surface(normal_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            normal_surface,
            pygame.Color("#fff1e7"),
            normal_rect,
            border_radius=border_radius,
        )

        hover_surface = normal_surface.copy()
        pygame.draw.rect(
            hover_surface,
            pygame.Color("#ffe8d7"),
            normal_rect,
            border_radius=border_radius,
        )

        pressed_surface = normal_surface.copy()
        pygame.draw.rect(
            pressed_surface,
            pygame.Color("#ffdcc3"),
            normal_rect,
            border_radius=border_radius,
        )
        super().__init__(
            rect,
            ButtonSurfaces(normal_surface, hover_surface, pressed_surface),
            on_click,
        )

        focus_ring_rect = rect.copy()
        self.focus_ring_surface = pygame.Surface(focus_ring_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            self.focus_ring_surface,
            pygame.Color("#ffdcc3"),
            focus_ring_rect,
            width=2,
            border_radius=border_radius + 4,
        )

        self.font = font
        self.set_text(text)

        self.on("keydown", self.handle_keydown)

    def set_text(self, text: str) -> None:
        self._rendered_text = self.font.render(text, True, pygame.Color("#451e11"))

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)
        surface.blit(
            self._rendered_text,
            self._rendered_text.get_rect(center=self.absolute_rect.center),
        )
        if self.has_focus:
            surface.blit(
                self.focus_ring_surface,
                self.focus_ring_surface.get_rect(center=self.absolute_rect.center),
            )

    def handle_keydown(self, event: Event) -> None:
        pressed_key: int = event.data["key"]
        if self.has_focus and pressed_key == pygame.K_RETURN:
            self.emit("click", Event(None))


class SpriteButton(BaseButton):
    def __init__(
        self: Self, surfaces: ButtonSurfaces, on_click: EventHandler | None = None
    ) -> None:
        super().__init__(surfaces.normal.get_rect(), surfaces, on_click)
