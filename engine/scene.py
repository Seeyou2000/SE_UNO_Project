from __future__ import annotations
from engine.gameobjectconainer import GameObjectContainer
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
    _scenes: dict[str, Scene]
    _current_scene: Scene

    def __init__(self):
        self._scenes = {}

    def add(self, scene: Scene, as_current: bool = False):
        self._scenes[type(scene).name] = scene
        if as_current:
            self.change_scene(type(scene))

    def change_scene(self, scene_type: type[Scene]):
        if scene_type.name in self._scenes:
            self._current_scene = self._scenes[scene_type.name]
            print(f'Scene 전환: {self._current_scene.name}')
        else:
            print(f'먼저 add를 호출하세요: {scene_type.name}')

    def get_current(self):
        try:
            return self._current_scene
        except AttributeError:
            print("먼저 change_scene을 호출하세요.")
    