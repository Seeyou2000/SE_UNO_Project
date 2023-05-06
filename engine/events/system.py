from copy import copy
from dataclasses import dataclass

import pygame

from engine.events.event import Event, EventPhase
from engine.events.mouseevent import MouseEvent
from engine.gameobject import GameObject
from engine.gameobjectcontainer import GameObjectContainer


@dataclass
class GlobalMouseContext:
    over_targets: list[GameObject]
    press_targets: list[GameObject]

    @property
    def leaf_over_target(self) -> GameObject | None:
        return self.over_targets[-1] if len(self.over_targets) > 0 else None

    @property
    def leaf_press_target(self) -> GameObject | None:
        return self.press_targets[-1] if len(self.press_targets) > 0 else None


class EventSystem:
    root: GameObject
    mouse_context: GlobalMouseContext

    def __init__(self, root: GameObject) -> None:
        self.root = root
        self.mouse_context = GlobalMouseContext([], [])

    def dispatch(self, event_name: str, event: Event) -> None:
        event.is_propagation_stopped = False
        event.name = event_name
        self.propagate(event)

    def propagate(self, event: Event) -> None:
        if event.target is None:
            return

        event.phase = EventPhase.CAPTURE
        for current_target in event.target.propagation_path[:-1]:
            event.current_target = current_target
            current_target.emit(event.name, event)
            if event.is_propagation_stopped:
                return

        event.phase = EventPhase.TARGET
        event.target.emit(event.name, event)
        if event.is_propagation_stopped:
            return

        event.phase = EventPhase.BUBBLE
        for current_target in reversed(event.target.propagation_path):
            if current_target is event.target:
                continue
            event.current_target = current_target
            current_target.emit(event.name, event, capturing=False, bubbling=True)
            if event.is_propagation_stopped:
                return

    def create_mouse_event_with_target(self, py_event: pygame.event.Event) -> Event:
        position = pygame.Vector2(py_event.dict["pos"])
        event = self.create_mouse_event(py_event, self.hit_test(position))
        return event

    def create_mouse_event(
        self, py_event: pygame.event.Event, target: GameObject | None
    ) -> Event:
        position = pygame.Vector2(py_event.dict["pos"])
        event = MouseEvent(position)
        event.target = target
        return event

    def hit_test(self, position: pygame.Vector2) -> GameObject | None:
        result = self.hit_test_recursive(self.root, position)
        return None if result is None else result[0]

    def hit_test_recursive(
        self, current_target: GameObject, position: pygame.Vector2
    ) -> list[GameObject] | None:
        if self.decide_ignore(current_target):
            return None

        current = current_target
        if isinstance(current, GameObjectContainer) and current.len_children() > 0:
            for child in current.reversed_child_iterator():
                recursive_hit = self.hit_test_recursive(child, position)
                if recursive_hit is not None:
                    if len(recursive_hit) > 0:
                        recursive_hit.append(current)
                    return recursive_hit

        if current.absolute_rect.collidepoint(position):
            return [current]

        return None

    def decide_ignore(self, game_object: GameObject) -> bool:
        return not game_object.is_visible

    def handle_mouse_down(self, py_event: pygame.event.Event) -> None:
        event = self.create_mouse_event_with_target(py_event)

        if event.target is None:
            return

        self.mouse_context.press_targets = event.target.propagation_path
        self.dispatch("mouse_down", event)

    def handle_mouse_move(self, py_event: pygame.event.Event) -> None:
        move_event = self.create_mouse_event_with_target(py_event)

        if move_event.target is None:
            return

        self.dispatch("mouse_move", move_event)

        # 직전 이벤트가 존재했어야만 out과 leave를 발생시킬 수 있다
        if (
            self.mouse_context.leaf_over_target is not None
            and move_event.target is not self.mouse_context.leaf_over_target
        ):
            # mouse_out
            out_event = self.create_mouse_event(
                py_event, self.mouse_context.leaf_over_target
            )
            self.dispatch("mouse_out", out_event)

            # mouse_leave
            # leaf_over_target은 직전 move 이벤트의 target이므로,
            # 이번 이벤트의 propagation_path에 직전 move 이벤트의 target이 없다는 것은
            # 새로운 컨테이너에 마우스가 올라갔거나 부모-자식 관계 중 자식에서 마우스가 빠져나왔다는 이야기이다.
            if (
                self.mouse_context.leaf_over_target
                not in move_event.target.propagation_path
            ):
                leave_event = self.create_mouse_event(
                    py_event, self.mouse_context.leaf_over_target
                )
                leave_event.phase = EventPhase.TARGET

                # move_event의 propagation_path에 존재하면 이번 move 이벤트의 좌표에 그 객체의 영역이 포함되어있다는
                # 얘기이므로 leaf_over_target에서 부모를 하나씩 찾아가면서 move_event의 propagation_path에
                # 포함되어 있지 않으면 mouse_leave 이벤트를 발생시킨다.
                while (
                    leave_event.target is not None
                    and leave_event.target not in move_event.target.propagation_path
                ):
                    leave_event.current_target = leave_event.target
                    leave_event.current_target.emit("mouse_leave", leave_event)
                    leave_event.target = leave_event.target.parent

        # 직전 이벤트가 없었어도 over와 enter는 발생시킬 수 있다
        if self.mouse_context.leaf_over_target is not move_event.target:
            # mouse_over
            over_event = self.create_mouse_event_with_target(py_event)
            self.dispatch("mouse_over", over_event)

            # mouse_enter
            enter_event = copy(move_event)
            enter_event.phase = EventPhase.TARGET

            while (
                enter_event.target is not None
                and enter_event.target is not self.mouse_context.leaf_over_target
            ):
                enter_event.current_target = enter_event.target
                enter_event.current_target.emit("mouse_enter", enter_event)
                enter_event.target = enter_event.target.parent

        self.mouse_context.over_targets = move_event.target.propagation_path

    def handle_mouse_up(self, py_event: pygame.event.Event) -> None:
        event = self.create_mouse_event_with_target(py_event)

        if event.target is None:
            return
        self.dispatch("mouse_up", event)
        if event.target is self.mouse_context.leaf_press_target:
            self.dispatch("click", event)

    def handle_keydown(self, py_event: pygame.event.Event) -> None:
        pass
