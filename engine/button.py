from dataclasses import dataclass
from typing import Self

import pygame

from engine.events.emitter import EventHandler
from engine.events.event import Event
from engine.focus import Focusable
from engine.fsm import FlowMachine, FlowNode
from engine.gameobject import GameObject


@dataclass
class ButtonSurfaces:
    normal: pygame.Surface
    hover: pygame.Surface
    pressed: pygame.Surface


class NormalState(FlowNode):
    pass


class HoverState(FlowNode):
    pass


class PressedState(FlowNode):
    pass


class DisabledState(FlowNode):
    pass


class BaseButton(GameObject, Focusable):
    font: pygame.font.Font
    on_click: EventHandler | None

    surfaces: ButtonSurfaces
    state_machine: FlowMachine

    def __init__(
        self: Self,
        rect: pygame.Rect,
        surfaces: ButtonSurfaces,
        on_click: EventHandler | None = None,
    ) -> None:
        super().__init__()

        self.rect = rect
        self.surfaces = surfaces
        self.state_machine = FlowMachine()
        self.state_machine.transition_to(NormalState())

        self.on(
            "mouse_down", lambda _: self.state_machine.transition_to(PressedState())
        )
        self.on("mouse_up", lambda _: self.state_machine.transition_to(NormalState()))
        self.on("mouse_enter", lambda _: self.state_machine.transition_to(HoverState()))
        self.on(
            "mouse_leave", lambda _: self.state_machine.transition_to(NormalState())
        )

        if on_click is not None:
            self.on("click", on_click)

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)

        button_surface = None
        match self.state_machine.current_node:
            case NormalState():
                button_surface = self.surfaces.normal
            case HoverState():
                button_surface = self.surfaces.hover
            case PressedState():
                button_surface = self.surfaces.pressed

        surface.blit(
            button_surface, button_surface.get_rect(center=self.absolute_rect.center)
        )


class Button(BaseButton):
    def __init__(
        self,
        text: str,
        rect: pygame.Rect,
        font: pygame.font.Font,
        on_click: EventHandler | None = None,
    ) -> None:
        border_radius = 10
        drawing_rect = rect.inflate(-4, -4)
        drawing_rect.topleft = (2, 2)

        super().__init__(
            rect,
            create_default_button_surfaces(rect, drawing_rect, border_radius),
            on_click,
        )

        focus_ring_rect = rect.copy()
        focus_ring_rect.topleft = (0, 0)
        self.focus_ring_surface = pygame.Surface(focus_ring_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            self.focus_ring_surface,
            pygame.Color("#FF9549"),
            focus_ring_rect,
            width=2,
            border_radius=border_radius + 4,
        )

        self.font = font
        self.set_text(text)

        self.on("keydown", self.handle_keydown)

    def set_text(self, text: str) -> None:
        self.text = text
        self._rendered_text = self.font.render(text, True, pygame.Color("#451e11"))

    def render(self, surface: pygame.Surface) -> None:
        if not self.is_visible:
            return
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


def create_default_button_surfaces(
    rect: pygame.Rect, drawing_rect: pygame.Rect, border_radius: int
) -> ButtonSurfaces:
    normal_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(
        normal_surface,
        pygame.Color("#fff1e7"),
        drawing_rect,
        border_radius=border_radius,
    )

    hover_surface = normal_surface.copy()
    pygame.draw.rect(
        hover_surface,
        pygame.Color("#ffe8d7"),
        drawing_rect,
        border_radius=border_radius,
    )

    pressed_surface = normal_surface.copy()
    pygame.draw.rect(
        pressed_surface,
        pygame.Color("#ffdcc3"),
        drawing_rect,
        border_radius=border_radius,
    )

    return ButtonSurfaces(normal_surface, hover_surface, pressed_surface)


class SpriteButton(BaseButton):
    def __init__(
        self: Self, surfaces: ButtonSurfaces, on_click: EventHandler | None = None
    ) -> None:
        super().__init__(surfaces.normal.get_rect(), surfaces, on_click)
