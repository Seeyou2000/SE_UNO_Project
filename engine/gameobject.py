import abc

import pygame

from engine.event import Event, EventEmitter


class GameObject(EventEmitter, abc.ABC):
    rect: pygame.Rect
    parent: "GameObject"
    absolute_rect: pygame.Rect
    _is_hovered: bool
    _is_pressed: bool

    def __init__(self) -> None:
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.absolute_rect = self.rect.copy()

        self._is_hovered = False
        self._is_pressed = False

        self.on("global_mouse_down", self.handle_global_mouse_down)
        self.on("global_mouse_up", self.handle_global_mouse_up)
        self.on("global_mouse_move", self.handle_global_mouse_move)
        self.on("front_object_entered", self.handle_front_object_entered)

    @property
    def is_hovered(self) -> bool:
        return self._is_hovered

    def update(self, dt: float) -> None:
        if self.parent is not None:
            self.absolute_rect = self.rect.move(self.parent.rect.topleft)
        else:
            self.absolute_rect = self.rect.copy()

    def render(self, surface: pygame.Surface) -> None:
        pass

    def handle_global_mouse_down(self, event: Event) -> None:
        if self.absolute_rect.collidepoint(pygame.mouse.get_pos()):
            self.emit("mouse_down", event)
            event.stop_propagation()
            self._is_pressed = True

    def handle_global_mouse_up(self, event: Event) -> None:
        if self.absolute_rect.collidepoint(pygame.mouse.get_pos()) and self._is_pressed:
            self._is_pressed = False
            self.emit("click", event)
            event.stop_propagation()

    def handle_global_mouse_move(self, event: Event) -> None:
        # 매 프레임 실행된다.
        if event.target is self:
            return
        is_first_enter = False
        is_first_exit = False
        if "pos" in event.data:
            is_mouse_collided = self.absolute_rect.collidepoint(event.data.get("pos"))
            is_first_enter = (not self._is_hovered) and is_mouse_collided
            is_first_exit = self._is_hovered and (not is_mouse_collided)
            self._is_hovered = is_mouse_collided
        if is_first_enter:
            self.emit("mouse_enter", Event(event.data))

            out_event = Event(None)
            out_event.target = self

            root = self.parent
            while root.parent is not None:
                root = root.parent
            root.emit("front_object_entered", out_event, False)

        if is_first_exit:
            self.emit("mouse_out", Event(None))

        if self._is_hovered:
            self.emit("hover", event)
            event.stop_propagation()

    def handle_front_object_entered(self, event: Event) -> None:
        if event.target is self:
            return
        if not self._is_hovered:
            return

        event.stop_propagation()

        self._is_hovered = False
        self.emit("mouse_out", Event(None))
