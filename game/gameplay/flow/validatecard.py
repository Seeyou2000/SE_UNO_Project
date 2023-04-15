from game.gameplay.card import Card
from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.gamestate import GameState


class ValidateCardFlowNode(AbstractGameFlowNode):
    def __init__(self, game_state: GameState, card: Card) -> None:
        super().__init__(game_state)

        self.card = card

    def enter(self) -> None:
        super().enter()

        is_card_color_valid = (
            (self.game_state.now_color == self.card.color)
            or (self.card.color == "black")
            or (self.game_state.now_color == "black")
        )

        is_number_card = self.card.number is not None

        last_card = self.game_state.discard_pile.get_last()
        is_card_content_valid = (
            self.card.number == last_card.number
            if is_number_card
            else self.card.ability == last_card.ability
        )

        # 디버그용
        is_card_color_valid = True

        if is_card_color_valid or is_card_content_valid:
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
