from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.gamestate import GameState


class TurnStartFlowNode(AbstractGameFlowNode):
    def __init__(self, gamestate: GameState) -> None:
        super().__init__(gamestate)
