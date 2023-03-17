from __future__ import annotations
from engine.gameobjectcontainer import GameObjectContainer
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from engine.world import World

class Scene(GameObjectContainer):
    @classmethod
    @property
    def name(cls):
        return cls.__name__
        
    def __init__(self, world: World):
        super().__init__()
        self.world = world

class SceneDirector():
    _current_scene: Scene

    def change_scene(self, scene: Scene):
        self._current_scene = scene

    def get_current(self):
        try:
            return self._current_scene
        except AttributeError:
            print("먼저 change_scene을 호출하세요.")
