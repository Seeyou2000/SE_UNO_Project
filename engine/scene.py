from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from engine.event import Event
from engine.focus import FocusController, FocusMoveDirection
from engine.gameobjectcontainer import GameObjectContainer
from engine.layout import Layout

if TYPE_CHECKING:
    from engine.world import World


class Scene(GameObjectContainer):
    def __init__(self, world: World) -> None:
        super().__init__()
        self.world = world
        self.layout = Layout(world.get_rect())
        self.focus_controller = FocusController()

        self.on("keydown", self.handle_focus_keydown)
        self.on("resize", lambda _: self.layout.rect.update(self.world.get_rect()))

    def update(self, dt: float) -> None:
        self.layout.update(dt)
        super().update(dt)

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


class SceneDirector:
    _current_scene: Scene

    def __init__(self) -> None:
        self._current_scene = None

    def change_scene(self, scene: Scene) -> None:
        self._current_scene = scene

    def get_current(self) -> Scene:
        return self._current_scene
