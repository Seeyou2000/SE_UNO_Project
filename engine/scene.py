from __future__ import annotations

from typing import TYPE_CHECKING

from engine.gameobjectcontainer import GameObjectContainer

if TYPE_CHECKING:
    from engine.world import World


class Scene(GameObjectContainer):
    def __init__(self, world: World) -> None:
        super().__init__()
        self.world = world


class SceneDirector:
    _current_scene: Scene

    def __init__(self) -> None:
        self._current_scene = None

    def change_scene(self, scene: Scene) -> None:
        self._current_scene = scene

    def get_current(self) -> None:
        return self._current_scene
