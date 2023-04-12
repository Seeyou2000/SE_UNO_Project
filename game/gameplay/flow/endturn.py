from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.flow.gameend import GameEndFlowNode
from game.gameplay.flow.startturn import StartTurnFlowNode
from game.gameplay.gamestate import GameState


class EndTurnFlowNode(AbstractGameFlowNode):
    def __init__(self, game_state: GameState) -> None:
        super().__init__(game_state)

    def enter(self) -> None:
        super().enter()
        if len(self.game_state.get_current_player().cards) == 1:
            pass  # UNO 판별 필요
        elif len(self.game_state.get_current_player().cards) == 0:
            self.machine.transition_to(GameEndFlowNode(self.game_state))
        else:
            self.game_state.turn.next()
            self.machine.transition_to(StartTurnFlowNode(self.game_state))
