from __future__ import annotations
from typing import Any, Callable, Self

EventData = dict[str, Any] | None

class Event():
    data: EventData
    is_propagation_stopped: bool
    target: EventEmitter | None

    def __init__(self, data: EventData) -> None:
        self.is_propagation_stopped = False

        self.data = data
        self.target = None
    
    def stopPropagation(self):
        self.is_propagation_stopped = True

EventHandler = Callable[[Event], None]

class EventEmitter():
    event_map: dict[str, list[EventHandler]]
    parent: Self | None

    def __init__(self, parent: Self | None = None) -> None:
        self.event_map = {}
        self.parent = parent
        
    def on(self, event_name: str, handler: EventHandler):
        if handler is None:
            return
        if event_name in self.event_map:
            self.event_map[event_name].append(handler)
        else:
            self.event_map[event_name] = [handler]

    def emit(self, event_name: str, event: Event):
        if event.is_propagation_stopped:
            return

        if event_name in self.event_map:
            for handler in self.event_map[event_name]:
                handler(event)