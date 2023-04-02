import abc

import pygame

from engine.event import Event, EventEmitter


class GameObject(EventEmitter, abc.ABC):
    rect: pygame.Rect
    _is_hovered: bool
    _is_pressed: bool

    def __init__(self) -> None:
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)
        self._is_hovered = False
        self._is_pressed = False

        self.on("global_mouse_down", self.handle_global_mouse_down)
        self.on("global_mouse_up", self.handle_global_mouse_up)
        self.on("global_mouse_move", self.handle_global_mouse_move)
        self.on("mouse_out", self.handle_mouse_out)

    def update(self) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        pass

    def handle_global_mouse_down(self, event: Event) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.emit("mouse_down", event)
            event.stop_propagation()
            self._is_pressed = True

    def handle_global_mouse_up(self, event: Event) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()) and self._is_pressed:
            self.emit("click", event)
            event.stop_propagation()
        self._is_pressed = False

    def handle_global_mouse_move(self, event: Event) -> None:
        if event.target is self:
            return
        if "pos" in event.data:
            self._is_hovered = self.rect.collidepoint(event.data.get("pos"))
        if self._is_hovered:
            out_event = Event(None)
            out_event.target = self
            self.parent.emit("mouse_out", out_event, False)

            self.emit("hover", event)
            event.stop_propagation()

    def handle_mouse_out(self, event: Event) -> None:
        self._is_hovered = False
