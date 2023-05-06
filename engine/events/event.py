from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from engine.events.emitter import EventEmitter
    from engine.events.system import EventSystem

EventData = dict[str, Any] | None


class EventPhase(Enum):
    CAPTURE = 0
    TARGET = 1
    BUBBLE = 2


class Event:
    data: EventData

    name: str
    target: EventEmitter | None
    current_target: EventEmitter | None
    system: EventSystem
    bubbles: bool
    phase: EventPhase
    is_propagation_stopped: bool

    def __init__(
        self, data: EventData | None = None, target: EventEmitter | None = None
    ) -> None:
        self.is_propagation_stopped = False
        self.bubbles = True

        self.data = data
        self.target = target

    def stop_propagation(self) -> None:
        self.is_propagation_stopped = True
