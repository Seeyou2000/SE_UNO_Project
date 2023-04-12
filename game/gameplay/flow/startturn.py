from game.constant import ColorableAbilityType
from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.gamestate import GameState


class StartTurnFlowNode(AbstractGameFlowNode):
    def __init__(self, gamestate: GameState) -> None:
        super().__init__(gamestate)

    def enter(self) -> None:
        super().enter()
        player = self.game_state.get_current_player()

        if len(self.game_state.attack_cards) != 0:
            for card in player.cards:
                # 공격 카드
                if (card.ability != ColorableAbilityType.GIVE_FOUR_CARDS) or (
                    card.ability != ColorableAbilityType.GIVE_TWO_CARDS
                ):
                    player.cards += self.game_state.flush_attack_cards()

    def update(self, dt: float) -> None:
        super().update(dt)
