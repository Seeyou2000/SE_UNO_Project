import pygame
import tween

from engine.button import BaseButton, ButtonSurfaces
from engine.events.emitter import EventHandler
from engine.events.event import Event
from engine.focus import Focusable
from game.font import FontType, get_font


class MenuButton(BaseButton, Focusable):
    def __init__(
        self,
        text: str,
        size: pygame.Vector2,
        on_click: EventHandler | None = None,
    ) -> None:
        rect = pygame.Rect(0, 0, size.x, size.y)
        normal_surface = pygame.Surface(rect.size, pygame.SRCALPHA)

        hover_surface = normal_surface.copy()
        pygame.draw.rect(
            hover_surface,
            pygame.Color("#ffe8d7"),
            rect.inflate(0, -70),
            border_radius=20,
        )

        pressed_surface = normal_surface.copy()
        pygame.draw.rect(
            pressed_surface,
            pygame.Color("#ffdcc3"),
            rect.inflate(0, -60),
            border_radius=20,
        )

        super().__init__(
            rect,
            ButtonSurfaces(normal_surface, hover_surface, pressed_surface),
            on_click,
        )

        self.font = get_font(FontType.UI_BOLD, 20)
        self.set_text(text)

        self.on("mouse_enter", self.handle_mouse_enter)
        self.on("mouse_leave", self.handle_mouse_leave)
        self.on("focus", self.handle_mouse_enter)
        self.on("unfocus", self.handle_mouse_leave)
        self.hover_alpha = 0

    def set_text(self, text: str) -> None:
        self._rendered_text = self.font.render(text, True, pygame.Color("#451e11"))

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)
        surface.blit(
            self._rendered_text,
            self._rendered_text.get_rect(center=self.absolute_rect.center),
        )

    def update(self, dt: float) -> None:
        super().update(dt)

    def handle_mouse_enter(self, event: Event) -> None:
        # self._override_surface = self.surfaces.hover
        t = tween.to(self, "hover_alpha", 255, 0.3)
        t.on_update(self.update_hover_alpha)

    def handle_mouse_leave(self, event: Event) -> None:
        # self._override_surface = None
        self.hover_alpha = 0

    def update_hover_alpha(self) -> None:
        self.surfaces.hover.set_alpha(self.hover_alpha)
