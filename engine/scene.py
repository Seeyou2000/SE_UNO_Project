from __future__ import annotations

from typing import TYPE_CHECKING

from engine.gameobjectcontainer import GameObjectContainer
from engine.layout import Layout

if TYPE_CHECKING:
    from engine.world import World


class Scene(GameObjectContainer):
    def __init__(self, world: World) -> None:
        super().__init__()
        self.world = world
        self.layout = Layout(world.get_rect())
        self.on("resize", lambda _: self.layout.rect.update(self.world.get_rect()))

    def update(self, dt: float) -> None:
        super().update(dt)
        self.layout.update(dt)


class SceneDirector:
    _current_scene: Scene

    def __init__(self) -> None:
        self._current_scene = None

    def change_scene(self, scene: Scene) -> None:
        self._current_scene = scene

    def get_current(self) -> None:
        return self._current_scene
