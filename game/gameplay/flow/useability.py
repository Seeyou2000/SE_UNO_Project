from game.constant import AbilityType
from game.gameplay.card import Card
from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.flow.changefieldcolor import ChangeFieldColorFlowNode
from game.gameplay.gamestate import GameState


class UseAbilityFlowNode(AbstractGameFlowNode):
    def __init__(self, game_state: GameState, card: Card, is_prepare: bool) -> None:
        super().__init__(game_state)
        self.card = card
        self.is_prepare = is_prepare

    def enter(self) -> None:
        super().enter()
        print(type(self).__name__, self.card)

        if AbilityType.GIVE_TWO_CARDS == self.card.ability:
            self.game_state.attack_cards(2)
        elif AbilityType.GIVE_FOUR_CARDS == self.card.ability:
            self.game_state.attack_cards(4)
        elif AbilityType.SKIP_ORDER == self.card.ability:
            self.game_state.reserve_skip(1)
        elif AbilityType.REVERSE_ORDER == self.card.ability:
            self.game_state.reverse_turn_direction()
        elif AbilityType.ABSOULTE_ATTACK == self.card.ability:
            self.game_state.attack_cards(2)
        elif AbilityType.ABSOULTE_PROTECT == self.card.ability:
            self.game_state.absoulte_protect_cards()

        from game.gameplay.flow.endability import EndAbilityFlowNode

        if self.card.color == "black":
            self.machine.transition_to(
                ChangeFieldColorFlowNode(self.game_state, self.card, self.is_prepare)
            )
        else:
            self.machine.transition_to(
                EndAbilityFlowNode(self.game_state, self.card, self.is_prepare)
            )
