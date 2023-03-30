from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.flow.gameend import GameEndFlowNode
from game.gameplay.flow.turnstart import TurnStartFlowNode
from game.gameplay.gamestate import GameState


class TurnNextFlowNode(AbstractGameFlowNode):
    def __init__(self, game_state: GameState) -> None:
        super().__init__(game_state)

    def enter(self) -> None:
        super().enter()
        if len(self.game_state.get_current_player().cards) == 1:
            pass
        elif len(self.game_state.get_current_player().cards) == 0:
            self.machine.transition_to(GameEndFlowNode(self.game_state))
        else:
            self.game_state.turn.next()
            self.machine.transition_to(TurnStartFlowNode(self.game_state))
