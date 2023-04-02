from enum import Enum

from engine.event import Event, EventEmitter
from engine.fsm import FlowMachine, FlowNode


class GameFlowMachineEventType(Enum):
    TRANSITION = "transition"


class TransitionEvent(Event):
    transition_from: str
    transition_to: str

    def __init__(self, transition_from: str, transition_to: str) -> None:
        super().__init__(None)
        self.transition_from = transition_from
        self.transition_to = transition_to


class GameFlowMachine(FlowMachine, EventEmitter):
    events: EventEmitter

    def __init__(self) -> None:
        super().__init__()
        self.events = EventEmitter()

    def transition_to(self, new_node: FlowNode) -> None:
        self.events.emit(
            GameFlowMachineEventType.TRANSITION,
            TransitionEvent(
                self._current_node.__class__.__name__, new_node.__class__.__name__
            ),
        )
        return super().transition_to(new_node)
