import pygame

from engine.events.event import Event
from engine.focus import Focusable, FocusController
from engine.gameobject import GameObject


class TextInput(GameObject, Focusable):
    font: pygame.font.Font
    color: pygame.Color
    _rendered_text: pygame.Surface
    _max_length: int

    def __init__(
        self,
        text: str,
        rect: pygame.Rect,
        font: pygame.font.Font,
        color: pygame.Color,
        max_length: int,
        focus_controller: FocusController,
    ) -> None:
        super().__init__()
        self.text = text
        self.font = font
        self.color = color
        self.rect = rect.copy()
        self._max_length = max_length
        self.controller = focus_controller
        self.set_text(text)
        self.on("keydown", self.handle_keydown)
        self.on("textinput", self.handle_textinput)
        self.on("click", lambda _: self.controller.focus_target(self))
        self.on("focus", self.start_editing)
        self.on("unfocus", self.stop_editing)

    def render(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface,
            pygame.Color("#fff1e7"),
            self.absolute_rect,
            border_radius=8,
        )

        text_rect = self._rendered_text.get_rect(center=self.absolute_rect.center)
        text_rect.left = self.absolute_rect.left + 20
        surface.blit(self._rendered_text, text_rect)

        if self.has_focus:
            focus_ring_rect = self.absolute_rect.copy()
            pygame.draw.rect(
                surface,
                pygame.Color("#FF9549"),
                focus_ring_rect,
                width=2,
                border_radius=8,
            )
        else:
            border_rect = self.absolute_rect.copy()
            pygame.draw.rect(
                surface,
                pygame.Color("#ffe8d7"),
                border_rect,
                width=2,
                border_radius=8,
            )

    def set_text(self, text: str) -> None:
        self.text = text
        if len(self.text) > self._max_length:
            self.text = self.text[: self._max_length]
        self._rendered_text = self.font.render(self.text, True, self.color)

    def set_color(self, color: pygame.Color) -> None:
        self.color = color
        self.set_text(self.text)

    def start_editing(self, event: Event) -> None:
        pygame.key.start_text_input()

    def stop_editing(self, event: Event) -> None:
        pygame.key.stop_text_input()

    def handle_keydown(self, event: Event) -> None:
        if not self.has_focus:
            return
        key: int = event.data["key"]

        match key:
            case pygame.K_BACKSPACE:
                self.set_text(self.text[:-1])
            case pygame.K_ESCAPE:
                self.unfocus()

    def handle_textinput(self, event: Event) -> None:
        if not self.has_focus:
            return

        self.set_text(self.text + event.data["text"])
