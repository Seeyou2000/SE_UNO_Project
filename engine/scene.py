from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from engine.events.emitter import EventEmitter
from engine.events.event import Event
from engine.events.system import EventSystem
from engine.focus import FocusController, FocusMoveDirection
from engine.gameobject import GameObject
from engine.gameobjectcontainer import GameObjectContainer
from engine.layout import Layout

if TYPE_CHECKING:
    from engine.world import World


class Scene(GameObjectContainer):
    def __init__(self, world: World) -> None:
        super().__init__()
        self.world = world
        self.rect = self.world.get_rect()
        self.layout = Layout(world.get_rect())
        self.focus_controller = FocusController()
        self.event_system = EventSystem(self)

        self.on("keydown", self.handle_focus_keydown)
        self.on("textinput", self.handle_textinput)
        self.on("textediting", self.handle_textediting)
        self.on("resize", self.handle_screen_resize)

    def update(self, dt: float) -> None:
        self.layout.update(dt)
        super().update(dt)

    def open_modal(self, modal: GameObject) -> None:
        self.add_child(modal)
        self.off("keydown", self.handle_focus_keydown)
        if self.focus_controller.current_focus is not None: 
            self.focus_controller.current_focus.unfocus()

    def close_modal(self, modal: GameObject) -> None:
        self.remove_child(modal)
        self.on("keydown", self.handle_focus_keydown)

    def handle_focus_keydown(self, event: Event) -> None:
        pressed_key: int = event.data["key"]

        match pressed_key:
            case pygame.K_UP:
                self.focus_controller.move_focus(FocusMoveDirection.UP)
            case pygame.K_DOWN:
                self.focus_controller.move_focus(FocusMoveDirection.DOWN)
            case pygame.K_LEFT:
                self.focus_controller.move_focus(FocusMoveDirection.LEFT)
            case pygame.K_RIGHT:
                self.focus_controller.move_focus(FocusMoveDirection.RIGHT)

        if isinstance(self.focus_controller.current_focus, EventEmitter):
            self.focus_controller.current_focus.emit("keydown", event)

    def handle_textinput(self, event: Event) -> None:
        if isinstance(self.focus_controller.current_focus, EventEmitter):
            self.focus_controller.current_focus.emit("textinput", event)

    def handle_textediting(self, event: Event) -> None:
        if isinstance(self.focus_controller.current_focus, EventEmitter):
            self.focus_controller.current_focus.emit("textediting", event)

    def handle_screen_resize(self, event: Event) -> None:
        self.rect = self.world.get_rect()
        self.layout.rect.update(self.world.get_rect())


class SceneDirector:
    _current_scene: Scene

    def __init__(self) -> None:
        self._current_scene = None

    def change_scene(self, scene: Scene) -> None:
        self._current_scene = scene

    def get_current(self) -> Scene:
        return self._current_scene
