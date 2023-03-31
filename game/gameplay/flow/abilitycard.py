from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.flow.turnnext import TurnNextFlowNode
from game.gameplay.flow.turnstart import TurnStartFlowNode
from game.gameplay.gamestate import GameState
from game.scene.card import Card
from game.scene.constant import ColorableAbilityType, NonColorableAbilityType


class AbilityCardFlowNode(AbstractGameFlowNode):
    def __init__(self, game_state: GameState, card: Card) -> None:
        super().__init__(game_state)
        self.card = card

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
        self.game_state.turn.next()

    def change_card_color(self) -> None:
        pass

    def enter(self) -> None:
        super().enter()
        # drawn_card = self.game_state.drawn_deck.get_last()
        print(self.game_state.now_color, self.card.color)
        if (
            (self.game_state.now_color == self.card.color)
            or (self.card.color == "black")
            or (self.game_state.now_color == "black")
        ):
            self.game_state.to_drawn_deck(self.card)
            # 기능카드의 기능 실행
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

            self.machine.transition_to(TurnNextFlowNode(self.game_state))
        else:
            self.machine.transition_to(TurnStartFlowNode(self.game_state))
