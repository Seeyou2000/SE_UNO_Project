from game.gameplay.card import Card
from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.gamestate import GameState


class ChangeFieldColorFlowNode(AbstractGameFlowNode):
    def __init__(self, game_state: GameState, card: Card, is_prepare: bool) -> None:
        super().__init__(game_state)

        self.card = card
        self.game_state = game_state
        self.is_prepare = is_prepare

    def enter(self) -> None:
        super().enter()
        # 색 변경 대기 로직 구현
