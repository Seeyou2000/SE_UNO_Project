from game.gameplay.deck import Deck
from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.gamestate import GameState
from game.gameplay.player import Player


class PrepareFlowNode(AbstractGameFlowNode):
    def __init__(
        self,
        game_state: GameState,
        players: list[Player],
    ) -> None:
        super().__init__(game_state)

        self.players = players

    def enter(self) -> None:
        super().enter()

        self.game_state.reset(self.players)

        first_card = self.game_state.game_deck.draw()
        self.game_state.discard_pile.cards.append(first_card)
        self.game_state.now_color = self.game_state.discard_pile.get_last().color

        if self.game_state.game_params.more_ability_cards:
            self.give_more_ability_cards_to_ai()
        elif self.game_state.game_params.give_every_card_to_players:
            self.give_all_cards()
        else:
            self.give_players_initial_cards()

        if first_card.ability is not None:
            from game.gameplay.flow.useability import UseAbilityFlowNode

            self.machine.transition_to(
                UseAbilityFlowNode(self.game_state, first_card, True)
            )
            return

        from game.gameplay.flow.startturn import StartTurnFlowNode

        self.machine.transition_to(StartTurnFlowNode(self.game_state))

    def give_players_initial_cards(self) -> None:
        for player in self.players:
            for _ in range(0, 7):
                self.game_state.draw_card(player)

    def give_more_ability_cards_to_ai(self) -> None:
        cards = self.game_state.weighty_draw_cards()

        for _ in range(0, 7):
            self.players[1].cards.append(cards.pop())
        for _ in range(0, 7):
            self.players[0].cards.append(cards.pop())

        self.game_state.game_deck = Deck(cards)

    def give_all_cards(self) -> None:
        for player in self.players:
            for _ in range(0, 13):
                self.game_state.draw_card(player)
