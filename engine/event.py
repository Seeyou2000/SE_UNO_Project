from typing import Callable


class EventEmiiter():
    event_map: dict[str, list[Callable]]

    def __init__(self) -> None:
        self.event_map = {}
        
    def on(self, event_name: str, handler: Callable):
        if handler is None:
            return
        if event_name in self.event_map:
            self.event_map[event_name].append(handler)
        else:
            self.event_map[event_name] = [handler]

    def emit(self, event_name: str, event_data):
        if event_name in self.event_map:
            for handler in self.event_map[event_name]:
                handler(event_data)