import pygame

from engine.gameobject import GameObject


class LayoutAnchor:
    TOP_LEFT = pygame.Vector2(0, 0)
    MIDDLE_LEFT = pygame.Vector2(0, 0.5)
    BOTTOM_LEFT = pygame.Vector2(0, 1)

    TOP_CENTER = pygame.Vector2(0.5, 0)
    CENTER = pygame.Vector2(0.5, 0.5)
    BOTTOM_CENTER = pygame.Vector2(0.5, 1)

    TOP_RIGHT = pygame.Vector2(1, 0)
    MIDDLE_RIGHT = pygame.Vector2(1, 0.5)
    BOTTOM_RIGHT = pygame.Vector2(1, 1)


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
        if child in self._children:
            del self._children[child]

    def get_constraint(self, child: GameObject) -> LayoutConstraint | None:
        if child in self._children:
            return self._children[child]
        else:
            return None

    def update_constraint(
        self,
        child: GameObject,
        anchor: pygame.Vector2 | None = None,
        margin: pygame.Vector2 | None = None,
    ) -> None:
        if child not in self._children:
            return
        if anchor is not None:
            self._children[child].anchor = anchor
        if margin is not None:
            self._children[child].margin = margin

    def update(self, dt: float) -> None:
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
