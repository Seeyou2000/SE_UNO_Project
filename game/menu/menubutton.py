import pygame
import tween

from engine.button import BaseButton, ButtonSurfaces
from engine.events.emitter import EventHandler
from engine.events.event import Event
from engine.gameobjectcontainer import GameObjectContainer
from engine.text import Text
from game.font import FontType, get_font


class MenuButton(BaseButton, GameObjectContainer):
    normal_text_color = pygame.Color("#635648")
    hover_text_color = pygame.Color("black")

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

        self.menu_text = Text(
            text,
            pygame.Vector2(),
            get_font(FontType.UI_BOLD, 30),
            self.normal_text_color,
        )
        self.menu_text.rect.left = 20
        self.menu_text.rect.centery = rect.centery
        self.add_child(self.menu_text)

        self.on("mouse_enter", self.handle_mouse_enter)
        self.on("mouse_leave", self.handle_mouse_leave)
        self.on("focus", self.handle_mouse_enter)
        self.on("unfocus", self.handle_mouse_leave)
        self.hover_alpha = 0
        self.alpha_tween = None

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)
        GameObjectContainer.render(self, surface)

    def handle_mouse_enter(self, event: Event) -> None:
        # self._override_surface = self.surfaces.hover
        self.alpha_tween = tween.to(self, "hover_alpha", 255, 0.3)
        self.alpha_tween.on_update(self.update_hover_alpha)
        self.menu_text.set_color(self.hover_text_color)

    def handle_mouse_leave(self, event: Event) -> None:
        if self.alpha_tween is not None:
            self.alpha_tween.stop()
            self.alpha_tween = None
        self.hover_alpha = 0
        self.menu_text.set_color(self.normal_text_color)

    def update_hover_alpha(self) -> None:
        self.surfaces.hover.set_alpha(self.hover_alpha)
