import abc

import pygame

from engine.event import Event
from engine.gameobject import GameObject


class GameObjectContainer(GameObject, abc.ABC):
    _children: list[GameObject]

    def __init__(self) -> None:
        super().__init__()
        self._children = []

    def update(self) -> None:
        for child in self._children:
            child.update()

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

    def emit(self, event_name: str, event: Event) -> None:
        super().emit(event_name, event)
        for child in reversed(self._children):
            if event.target is child:
                continue
            if event.is_propagation_stopped:
                break
            child.emit(event_name, event)
