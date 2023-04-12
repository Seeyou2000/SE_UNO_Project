from game.gameplay.card import Card
from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.gamestate import GameState


class ChangeFieldColorFlowNode(AbstractGameFlowNode):
    def __init__(self, game_state: GameState, card: Card) -> None:
        super().__init__(game_state)

        self.card = card

    def enter(self) -> None:
        super().enter()

        # 색 변경 대기 로직 구현

        from gameplay.flow.endturn import EndTurnFlowNode

        self.machine.transition_to(EndTurnFlowNode(self.game_state))
