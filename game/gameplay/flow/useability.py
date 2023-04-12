from game.constant import ColorableAbilityType, NonColorableAbilityType
from game.gameplay.card import Card
from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.gamestate import GameState


class UseAbilityFlowNode(AbstractGameFlowNode):
    def __init__(self, game_state: GameState, card: Card, is_prepare: bool) -> None:
        super().__init__(game_state)
        self.card = card
        self.is_prepare = is_prepare

    def enter(self) -> None:
        super().enter()

        if ColorableAbilityType.GIVE_TWO_CARDS == self.card.ability:
            self.game_state.attack_cards(2)
        elif ColorableAbilityType.GIVE_FOUR_CARDS == self.card.ability:
            self.game_state.attack_cards(4)
        elif ColorableAbilityType.SKIP_ORDER == self.card.ability:
            self.game_state.reserve_skip(1)
        elif ColorableAbilityType.REVERSE_ORDER == self.card.ability:
            self.game_state.turn.reverse()
        elif NonColorableAbilityType.CHANGE_CARD_COLOR == self.card.ability:
            pass
            # self.change_card_color()

        from game.gameplay.flow.endability import EndAbilityFlowNode

        self.machine.transition_to(
            EndAbilityFlowNode(self.game_state, self.card, self.is_prepare)
        )
