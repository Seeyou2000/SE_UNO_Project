from collections import namedtuple
from collections.abc import Callable
from typing import Self

from engine.events.event import Event

EventHandler = Callable[[Event], None]
EmitterHandler = namedtuple("EmitterHandler", ["fn", "capturing", "bubbling"])


class EventEmitter:
    event_map: dict[str, list[EmitterHandler]]
    parent: Self | None
    propagation_path: list[Self]

    def __init__(self, parent: Self | None = None) -> None:
        self.event_map = {}
        self.propagation_path = []
        self.parent = parent

    def set_parent(self, parent: Self | None) -> None:
        self.propagation_path.clear()
        self.parent = parent

        self.propagation_path.append(self)

        if parent is not None:
            current = parent
            while current is not None:
                self.propagation_path.append(current)
                current = current.parent
        self.propagation_path = list(reversed(self.propagation_path))

    def on(
        self,
        event_name: str,
        handler: EventHandler | list[EventHandler],
        capturing: bool = True,
        bubbling: bool = False,
    ) -> None:
        if handler is None:
            return

        if event_name not in self.event_map:
            self.event_map[event_name] = []

        target = self.event_map[event_name]
        if type(handler) == list:
            for fn in handler:
                target.append(EmitterHandler(fn, capturing, bubbling))
        else:
            target.append(EmitterHandler(handler, capturing, bubbling))

    def off_all(self, event_name: str) -> None:
        self.event_map[event_name] = []

    def off(
        self,
        event_name: str,
        handler: EventHandler,
        capturing: bool = True,
        bubbling: bool = False,
    ) -> None:
        emitter_handler = EmitterHandler(handler, capturing, bubbling)

        if emitter_handler in self.event_map[event_name]:
            self.event_map[event_name].remove(emitter_handler)

    def emit(
        self,
        event_name: str,
        event: Event,
        capturing: bool = True,
        bubbling: bool = False,
    ) -> None:
        event.name = event_name

        if event.is_propagation_stopped:
            return

        if event_name in self.event_map:
            for handler in self.event_map[event_name]:
                if (handler.capturing and capturing) or (handler.bubbling and bubbling):
                    handler.fn(event)
