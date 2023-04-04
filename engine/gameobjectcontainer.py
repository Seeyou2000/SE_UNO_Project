import abc

import pygame

from engine.event import Event
from engine.gameobject import GameObject


class GameObjectContainer(GameObject, abc.ABC):
    _children: list[GameObject]

    def __init__(self) -> None:
        super().__init__()
        self._children = []

    def update(self, dt: float) -> None:
        for child in self._children:
            child.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        for child in self._children:
            child.render(surface)

    def add_child(self, child: GameObject) -> None:
        self._children.append(child)
        child.parent = self

    def add_children(self, children: list[GameObject]) -> None:
        for child in children:
            self.add_child(child)

    def remove_child(self, child: GameObject) -> None:
        self._children.remove(child)
        child.parent = None

    def emit(self, event_name: str, event: Event, is_target_self: bool = True) -> None:
        super().emit(event_name, event, is_target_self)
        # 마우스 이벤트라면 위에서 이벤트를 감지했다면 앞에 깔려있는 오브젝트에 전파를 하지 않아도 된다
        # _children의 뒤에 있을 수록 나중에 렌더링되므로 순회를 역순으로 한다
        for child in reversed(self._children):
            if event.target is child:
                continue
            if event.is_propagation_stopped:
                break
            child.emit(event_name, event, False)
