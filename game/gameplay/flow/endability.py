from game.gameplay.card import Card
from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.flow.discardcard import DiscardCardFlowNode
from game.gameplay.flow.startturn import StartTurnFlowNode
from game.gameplay.gamestate import GameState


class EndAbilityFlowNode(AbstractGameFlowNode):
    def __init__(self, game_state: GameState, card: Card, is_prepare: bool) -> None:
        super().__init__(game_state)
        self.card = card
        self.is_prepare = is_prepare

    def enter(self) -> None:
        super().enter()

        if self.is_prepare:
            self.machine.transition_to(StartTurnFlowNode(self.game_state))
        else:
            self.machine.transition_to(DiscardCardFlowNode(self.game_state, self.card))
