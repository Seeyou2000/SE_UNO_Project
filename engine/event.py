from __future__ import annotations

from collections.abc import Callable
from typing import Any, Self

EventData = dict[str, Any] | None


class Event:
    name: str
    data: EventData
    is_propagation_stopped: bool
    target: EventEmitter | None

    def __init__(self, data: EventData) -> None:
        self.is_propagation_stopped = False

        self.data = data
        self.target = None

    def stop_propagation(self) -> None:
        self.is_propagation_stopped = True


EventHandler = Callable[[Event], None]


class EventEmitter:
    event_map: dict[str, list[EventHandler]]
    parent: Self | None

    def __init__(self, parent: Self | None = None) -> None:
        self.event_map = {}
        self.parent = parent

    def on(
        self, event_name: str, handler: EventHandler | list[EventHandler] | None
    ) -> None:
        if handler is None:
            return
        if event_name in self.event_map:
            target = self.event_map[event_name]
            if type(handler) is list:
                target += handler
            else:
                target.append(handler)
        else:
            if type(handler) is list:
                self.event_map[event_name] = handler
            else:
                self.event_map[event_name] = [handler]

    def off_all(self, event_name: str) -> None:
        self.event_map[event_name] = []

    def off(self, event_name: str, handler: EventHandler) -> None:
        self.event_map[event_name].remove(handler)

    def emit(self, event_name: str, event: Event, is_target_self: bool = True) -> None:
        event.name = event_name
        if is_target_self:
            event.target = self
        if event.is_propagation_stopped:
            return

        if event_name in self.event_map:
            for handler in self.event_map[event_name]:
                handler(event)
