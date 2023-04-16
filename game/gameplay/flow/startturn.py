from engine.event import Event
from game.constant import ColorableAbilityType
from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.gamestate import GameState


class StartTurnFlowNode(AbstractGameFlowNode):
    def __init__(self, gamestate: GameState) -> None:
        super().__init__(gamestate)

    def enter(self) -> None:
        super().enter()
        player = self.game_state.get_current_player()

        if self.game_state.is_attacked():
            for card in player.cards:
                # 공격 카드
                if (card.ability != ColorableAbilityType.GIVE_FOUR_CARDS) or (
                    card.ability != ColorableAbilityType.GIVE_TWO_CARDS
                ):
                    self.game_state.flush_attack_cards(
                        self.game_state.get_current_player()
                    )
        self.game_state.turn_timer.on("tick", self.transition_to_draw_card)

    def transition_to_draw_card(self, event: Event) -> None:
        from game.gameplay.flow.drawcard import DrawCardFlowNode

        self.machine.transition_to(DrawCardFlowNode(self.game_state))

    def update(self, dt: float) -> None:
        super().update(dt)

    def exit(self) -> None:
        super().exit()
        self.game_state.turn_timer.off_one("tick", self.transition_to_draw_card)
