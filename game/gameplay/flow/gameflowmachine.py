from enum import Enum

from engine.event import Event, EventEmitter
from engine.fsm import FlowMachine
from game.gameplay.flow.abstractflownode import AbstractGameFlowNode


class GameFlowMachineEventType(Enum):
    TRANSITION = "transition"
    CARD_PLAYED = "card_played"


class TransitionEvent(Event):
    before: AbstractGameFlowNode
    after: AbstractGameFlowNode

    def __init__(
        self,
        transition_from: AbstractGameFlowNode,
        transition_to: AbstractGameFlowNode,
    ) -> None:
        super().__init__(None)
        self.before = transition_from
        self.after = transition_to


class GameFlowMachine(FlowMachine, EventEmitter):
    events: EventEmitter

    def __init__(self) -> None:
        super().__init__()
        self.events = EventEmitter()

    def transition_to(self, new_node: AbstractGameFlowNode) -> None:
        self.events.emit(
            GameFlowMachineEventType.TRANSITION,
            TransitionEvent(self._current_node, new_node),
        )
        super().transition_to(new_node)
