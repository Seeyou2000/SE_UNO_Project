import abc
import pygame
from engine.event import Event

from engine.gameobject import GameObject

class GameObjectContainer(GameObject, abc.ABC):
    _children: list[GameObject]

    def __init__(self):
        super().__init__()
        self._children = []

    def update(self):
        for child in self._children:
            child.update()

    def render(self, surface: pygame.Surface):
        for child in self._children:
            child.render(surface)

    def add_child(self, child: GameObject):
        self._children.append(child)
        child.parent = self
    
    def add_children(self, children: list[GameObject]):
        for child in children:
            self.add_child(child)

    def remove_child(self, child: GameObject):
        self._children.remove(child)
        child.parent = None
    
    def emit(self, event_name: str, event: Event):
        super().emit(event_name, event)
        for child in reversed(self._children):
            if event.target is child:
                continue
            if event.is_propagation_stopped:
                break
            child.emit(event_name, event)