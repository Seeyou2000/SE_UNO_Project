from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.flow.turnnext import TurnNextFlowNode
from game.gameplay.gamestate import GameState


class DrawCardFlowNode(AbstractGameFlowNode):
    def __init__(self, game_state: GameState) -> None:
        super().__init__(game_state)

    def enter(self) -> None:
        super().enter()
        self.game_state.get_current_player().draw_card(self.game_state.game_deck)
        self.machine.transition_to(TurnNextFlowNode(self.game_state))
