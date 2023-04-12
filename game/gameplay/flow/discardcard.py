from engine.event import Event
from game.gameplay.card import Card
from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.flow.gameflowmachine import GameFlowMachineEventType
from game.gameplay.gamestate import GameState


class DiscardCardFlowNode(AbstractGameFlowNode):
    def __init__(self, game_state: GameState, card: Card) -> None:
        super().__init__(game_state)

        self.card = card

    def enter(self) -> None:
        super().enter()

        self.game_state.discard(self.card)
        self.machine.events.emit(
            GameFlowMachineEventType.CARD_PLAYED,
            Event({"card": self.card, "player": self.game_state.get_current_player()}),
        )

        from game.gameplay.flow.endturn import EndTurnFlowNode

        self.machine.transition_to(EndTurnFlowNode(self.game_state))
