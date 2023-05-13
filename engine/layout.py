from collections.abc import Callable
from enum import Enum
from typing import Self

import pygame

from engine.gameobject import GameObject
from engine.gameobjectcontainer import GameObjectContainer


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


class LinearLayoutDirection(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class LinearLayout(GameObjectContainer):
    direction: LinearLayoutDirection
    gap: int

    def __init__(
        self,
        pos: pygame.Vector2,
        direction: LinearLayoutDirection,
        gap: int,
        elements: list[GameObject | Self],
        margin: int = 0,
    ) -> None:
        super().__init__()
        self.rect = pygame.Rect(pos.x, pos.y, 0, 0)
        self.direction = direction
        self.gap = gap
        self.margin = margin
        self.add_children(elements)
        self.update(0)

    def update(self, dt: float) -> None:
        super().update(dt)
        next_pos = self.margin
        max_sub_axis_size = 0
        for child in self._children:
            if self.direction == LinearLayoutDirection.HORIZONTAL:
                child.rect.x = next_pos
                next_pos = self.margin + child.rect.right + self.gap
                max_sub_axis_size = max(max_sub_axis_size, child.rect.height)
            else:
                child.rect.y = next_pos
                next_pos = self.margin + child.rect.bottom + self.gap
                max_sub_axis_size = max(max_sub_axis_size, child.rect.width)

        if self.direction == LinearLayoutDirection.HORIZONTAL:
            self.rect.width = (
                self._children[-1].rect.right if len(self._children) > 0 else 0
            ) + self.margin
            self.rect.height = max_sub_axis_size
        else:
            self.rect.width = max_sub_axis_size
            self.rect.height = (
                self._children[-1].rect.bottom if len(self._children) > 0 else 0
            ) + self.margin


class Horizontal(LinearLayout):
    def __init__(
        self, pos: pygame.Vector2, gap: int, elements: list[GameObject | Self]
    ) -> None:
        super().__init__(pos, LinearLayoutDirection.HORIZONTAL, gap, elements)


class Vertical(LinearLayout):
    def __init__(
        self, pos: pygame.Vector2, gap: int, elements: list[GameObject | Self]
    ) -> None:
        super().__init__(pos, LinearLayoutDirection.VERTICAL, gap, elements)


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
