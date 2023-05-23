import abc
from enum import Enum
from typing import cast

import pygame

from engine.events.emitter import EventEmitter
from engine.events.event import Event
from engine.gameobject import GameObject


class FocusMoveDirection(Enum):
    """
    포커스를 움직일 수 있는 방향과 그 정규 벡터
    """

    RIGHT = pygame.Vector2(1, 0)
    DOWN = pygame.Vector2(0, 1)
    LEFT = pygame.Vector2(-1, 0)
    UP = pygame.Vector2(0, -1)


class Focusable(EventEmitter, abc.ABC):
    has_focus: bool
    rect: pygame.Rect
    controller: "FocusController"

    def __init__(self) -> None:
        super().__init__()
        self.has_focus = False
        self.controller = None
        self.on("keydown", self.emit_click)

    def focus(self) -> None:
        self.has_focus = True
        self.emit("focus", Event(None))

    def unfocus(self) -> None:
        self.has_focus = False
        self.emit("unfocus", Event(None))

    def emit_click(self, event: Event) -> None:
        if event.data["key"] == pygame.K_RETURN and self.has_focus:
            self.emit("click", Event(None))


FocusSiblings = dict[FocusMoveDirection, Focusable]


class FocusController:
    _targets: dict[Focusable, FocusSiblings | None]
    current_focus: Focusable

    def __init__(self) -> None:
        self._targets = {}
        self.current_focus = None

    def add(self, target: Focusable) -> None:
        self._targets[target] = {}
        target.controller = self

    def remove(self, target: Focusable) -> None:
        targets = list(self._targets.keys())
        self.current_focus = targets[targets.index(target) - 1]
        del self._targets[target]
        target.controller = None

    def has(self, target: Focusable) -> bool:
        return target in self._targets

    def set_siblings(self, target: Focusable, siblings: FocusSiblings) -> None:
        """
        방향별 sibling을 직접 지정하고 싶을 때 사용합니다. 지정하지 않으면 포커스를 옮길 때 자동으로 거리 기반으로 찾습니다.
        참조: find_sibling()
        """
        self._targets[target] = siblings

    def focus_target(self, target: Focusable) -> None:
        if target not in self._targets:
            return

        if target is not None:
            before = self.current_focus
            if before is not None:
                before.unfocus()
            target.focus()
            self.current_focus = target

    def move_focus(self, direction: FocusMoveDirection) -> None:
        before = self.current_focus
        after: Focusable | None
        if before is None:
            if len(self._targets) == 0:
                return
            after = next(iter(self._targets.keys()))
        else:
            after = self.find_sibling(self.current_focus, direction)

        if after is None:
            return
        self.focus_target(after)

    def find_sibling(
        self, target: Focusable, direction: FocusMoveDirection
    ) -> Focusable | None:
        if target not in self._targets:
            return

        if direction in self._targets[target]:
            candidate = self._targets[target][direction]
            if not cast(GameObject, candidate).is_visible:
                return self._targets[target][direction]

        closest = self.find_in_direction_vector(target, direction.value, farthest=False)
        if closest is not None:
            return closest

        # 해당 방향성이 있는 곳에서 찾지 못했다면 방향이 반대이고 가장 멀리 있는 타겟으로 가기(루프)
        return self.find_in_direction_vector(
            target, direction.value * -1, farthest=True
        )

    def find_in_direction_vector(
        self, target: Focusable, direction_vector: pygame.Vector2, farthest: bool
    ) -> Focusable | None:
        distance_sorted = sorted(
            filter(
                lambda t: (t is not target) and (t.is_visible), self._targets.keys()
            ),
            key=lambda other: pygame.Vector2(
                other.absolute_rect.center
            ).distance_squared_to(target.absolute_rect.center),
            reverse=farthest,
        )

        # print("dist", distance_sorted)

        angle_filtered = [
            other
            for other in distance_sorted
            if is_on_direction_vector(target, other, direction_vector)
        ]

        # print("angle", angle_filtered)

        if len(angle_filtered) > 0:
            return angle_filtered[0]

        return None


def get_angle(
    target: Focusable, other: Focusable, direction_vector: pygame.Vector2
) -> float:
    target_center = pygame.Vector2(target.absolute_rect.center)
    other_center = pygame.Vector2(other.absolute_rect.center)
    diff = other_center - target_center

    angle = diff.angle_to(direction_vector)
    # -360이 뜨는 경우가 있어 보정
    if angle < -359:
        angle += 360

    return angle


def is_on_direction_vector(
    target: Focusable, other: Focusable, direction_vector: pygame.Vector2
) -> None:
    angle = get_angle(target, other, direction_vector)

    # +45나 -45 안이면 해당 방향에 있는 것으로 간주
    return abs(angle) < 45
