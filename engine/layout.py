from collections.abc import Callable

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


def update_horizontal_linear_overlapping_layout(
    objects: list[GameObject],
    layout: Layout,
    dt: float,
    max_width: float,
    gap: float,
    offset_retriever: Callable[
        [GameObject, float], pygame.Vector2
    ] = lambda _, __: pygame.Vector2(),
) -> None:
    if len(objects) < 1:
        return
    width = objects[0].rect.width
    original_total_width = (width - gap) * (len(objects) - 1) + width
    clamped_total_width = min(original_total_width, max_width)
    for i, obj in enumerate(objects):
        # 일단 트윈 대신 감속 공식으로 애니메이션 구현
        constraint = layout.get_constraint(obj)
        if constraint is None:
            continue
        existing_margin = constraint.margin
        objects_len = len(objects)
        delta = obj.rect.width - gap
        x = (
            (i - objects_len / 2.0) * max_width / objects_len + gap
            if original_total_width > max_width
            else (i - 1 - objects_len / 2.0) * delta + obj.rect.width + gap / 2
        )
        target_pos = pygame.Vector2(x, 0) + offset_retriever(obj, clamped_total_width)
        layout.update_constraint(
            obj,
            margin=existing_margin + (target_pos - existing_margin) * dt * 10,
        )
