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
            self.give_two_cards()
        elif ColorableAbilityType.GIVE_FOUR_CARDS == self.card.ability:
            self.give_four_cards()
        elif ColorableAbilityType.SKIP_ORDER == self.card.ability:
            self.skip_order()
        elif ColorableAbilityType.REVERSE_ORDER == self.card.ability:
            self.reverse_order()
        elif NonColorableAbilityType.CHANGE_CARD_COLOR == self.card.ability:
            self.change_card_color()

        from game.gameplay.flow.endability import EndAbilityFlowNode

        self.machine.transition_to(
            EndAbilityFlowNode(self.game_state, self.card, self.is_prepare)
        )

    def give_two_cards(self) -> None:
        for _ in range(0, 2):
            self.game_state.attack_cards.append(self.game_state.game_deck.draw())

    def give_four_cards(self) -> None:
        for _ in range(0, 4):
            self.game_state.attack_cards.append(self.game_state.game_deck.draw())

    def skip_order(self) -> None:
        self.game_state.turn.next()

    def reverse_order(self) -> None:
        self.game_state.turn.reverse()

    def change_card_color(self) -> None:
        pass
