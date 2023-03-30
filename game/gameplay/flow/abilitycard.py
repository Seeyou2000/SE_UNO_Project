from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.flow.turnnext import TurnNextFlowNode
from game.gameplay.flow.turnstart import TurnStartFlowNode
from game.gameplay.gamestate import GameState
from game.scene.card import Card


class AbilityCardFlowNode(AbstractGameFlowNode):
    def __init__(self, game_state: GameState, card: Card) -> None:
        super().__init__(game_state)
        self.card = card

    def enter(self) -> None:
        super().enter()
        # drawn_card = self.game_state.drawn_deck.get_last()
        if (
            self.game_state.now_color == self.card.color
            or self.card.color == "black"
            or self.game_state.now_color == "black"
        ):
            self.game_state.to_drawn_deck(self.card)
            # 기능카드의 기능 실행
            self.machine.transition_to(TurnNextFlowNode(self.game_state))
        else:
            self.machine.transition_to(TurnStartFlowNode(self.game_state))
