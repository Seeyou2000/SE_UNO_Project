from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.flow.turnnext import TurnNextFlowNode
from game.gameplay.flow.turnstart import TurnStartFlowNode
from game.gameplay.gamestate import GameState
from game.scene.card import Card


class NumberCardFlowNode(AbstractGameFlowNode):
    def __init__(self, game_state: GameState, card: Card) -> None:
        super().__init__(game_state)
        self.card = card

    def enter(self) -> None:
        super().enter()
        drawn_card = self.game_state.drawn_deck.get_last()
        if drawn_card.color == self.card.color or drawn_card.number == self.card.number:
            self.game_state.drawn_deck.cards.append(self.card)
            self.game_state.get_current_player().cards.remove(self.card)
            self.machine.transition_to(TurnNextFlowNode(self.game_state))
        else:
            self.machine.transition_to(TurnStartFlowNode(self.game_state))
