from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.flow.endturn import EndTurnFlowNode
from game.gameplay.gamestate import GameState


class DrawCardFlowNode(AbstractGameFlowNode):
    def __init__(self, game_state: GameState) -> None:
        super().__init__(game_state)

    def enter(self) -> None:
        super().enter()
        self.game_state.draw_card(self.game_state.get_current_player())
        self.machine.transition_to(EndTurnFlowNode(self.game_state))
