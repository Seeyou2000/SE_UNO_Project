from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.gamestate import GameState
from game.gameplay.player import Player


class PrepareFlowNode(AbstractGameFlowNode):
    def __init__(self, game_state: GameState, players: list[Player]) -> None:
        super().__init__(game_state)

        self.players = players

    def enter(self) -> None:
        super().enter()

        self.game_state.reset(self.players)
        self.give_players_initial_cards()

        first_card = self.game_state.game_deck.draw()
        self.game_state.discard_pile.cards.append(first_card)
        self.game_state.now_color = self.game_state.discard_pile.get_last().color
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
                player.draw_card(self.game_state.game_deck)
