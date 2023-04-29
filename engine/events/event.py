from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from engine.events.emitter import EventEmitter

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