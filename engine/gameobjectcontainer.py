import abc
from collections.abc import Iterator
from operator import attrgetter

import pygame

from engine.gameobject import GameObject


class GameObjectContainer(GameObject, abc.ABC):
    _children: list[GameObject]

    def __init__(self) -> None:
        super().__init__()
        self._children = []

    def update(self, dt: float) -> None:
        super().update(dt)
        for child in self._children:
            child.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        if not self.is_visible:
            return
        super().render(surface)
        self._children.sort(key=attrgetter("order"))
        for child in self._children:
            child.render(surface)

    def add_child(self, child: GameObject) -> None:
        self._children.append(child)
        child.set_parent(self)
        child.update_absolute_rect()

    def add_children(self, children: list[GameObject]) -> None:
        for child in children:
            self.add_child(child)

    def remove_child(self, child: GameObject) -> None:
        self._children.remove(child)
        child.set_parent(None)

    def has_child(self, child: GameObject) -> None:
        return child in self._children

    def len_children(self) -> int:
        return len(self._children)

    def reversed_child_iterator(self) -> Iterator[GameObject]:
        return reversed(self._children)

    def set_order(self, child: GameObject, order: int) -> None:
        if not self.has_child(child):
            return
        self._children.remove(child)
        self._children.insert(order, child)
