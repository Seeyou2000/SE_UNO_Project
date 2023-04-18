from game.constant import AbilityType
from game.gameplay.card import Card
from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.gamestate import GameState


class ValidateCardFlowNode(AbstractGameFlowNode):
    def __init__(self, game_state: GameState, card: Card) -> None:
        super().__init__(game_state)

        self.card = card

    def enter(self) -> None:
        super().enter()
        print(type(self).__name__, self.card)

        is_card_color_valid = (self.game_state.now_color == self.card.color) or (
            self.card.color == "black"
        )

        is_number_card = self.card.number is not None

        last_card = self.game_state.discard_pile.get_last()
        is_card_content_valid = (
            self.card.number == last_card.number
            if is_number_card
            else self.card.ability == last_card.ability
        )
        is_attack_valid = (
            self.card.ability == AbilityType.GIVE_TWO_CARDS
            or self.card.ability == AbilityType.GIVE_FOUR_CARDS
        ) and (
            last_card.ability == AbilityType.GIVE_TWO_CARDS
            or last_card.ability == AbilityType.GIVE_FOUR_CARDS
        )

        if self.game_state.is_attacked() and not (
            self.card.ability == AbilityType.GIVE_FOUR_CARDS
            or self.card.ability == AbilityType.GIVE_TWO_CARDS
            or self.card.ability == AbilityType.ABSOULTE_ATTACK
            or self.card.ability == AbilityType.ABSOULTE_PROTECT
        ):
            from game.gameplay.flow.startturn import StartTurnFlowNode

            self.machine.transition_to(StartTurnFlowNode(self.game_state))
            return

        if is_card_color_valid or is_card_content_valid or is_attack_valid:
            if is_number_card:
                from game.gameplay.flow.discardcard import DiscardCardFlowNode

                self.machine.transition_to(
                    DiscardCardFlowNode(self.game_state, self.card)
                )
            else:
                from game.gameplay.flow.useability import UseAbilityFlowNode

                self.machine.transition_to(
                    UseAbilityFlowNode(self.game_state, self.card, False)
                )
        else:
            from game.gameplay.flow.startturn import StartTurnFlowNode

            self.machine.transition_to(StartTurnFlowNode(self.game_state))
            self.machine.transition_to(StartTurnFlowNode(self.game_state))
