import pygame

from engine.gameobject import GameObject


class LayoutConstraint:
    def __init__(self, anchor: pygame.Vector2, margin: pygame.Vector2) -> None:
        self.anchor = anchor
        self.margin = margin


class Layout:
    _children: dict[GameObject, LayoutConstraint]
    rect: pygame.Rect

    def __init__(self, rect: pygame.Rect) -> None:
        self._children = {}
        self.rect = rect

    def add(
        self, child: GameObject, anchor: pygame.Vector2, margin: pygame.Vector2
    ) -> None:
        self._children[child] = LayoutConstraint(anchor, margin)

    def remove(self, child: GameObject) -> None:
        del self._children[child]

    def update(self) -> None:
        for child, constraint in self._children.items():
            anchor = constraint.anchor
            margin = constraint.margin
            width = self.rect.bottomright[0] * anchor.x + margin.x
            height = self.rect.bottomright[1] * anchor.y + margin.y
            if anchor.x < 0.5:
                child.rect.left = width
            elif anchor.x > 0.5:
                child.rect.right = width
            else:
                child.rect.centerx = width
            if anchor.y < 0.5:
                child.rect.top = height
            elif anchor.y > 0.5:
                child.rect.bottom = height
            else:
                child.rect.centery = height
