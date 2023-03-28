import abc

from engine.fsm import FlowNode
from game.gameplay.gamestate import GameState


class AbstractGameFlowNode(FlowNode, abc.ABC):
    game_state: GameState

    def __init__(self, game_state: GameState) -> None:
        super().__init__()
        self.game_state = game_state
