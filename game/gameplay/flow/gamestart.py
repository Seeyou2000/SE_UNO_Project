from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.gamestate import GameState
from game.gameplay.player import Player


class GameStartFlowNode(AbstractGameFlowNode):
    def __init__(self, game_state: GameState, players: list[Player]) -> None:
        super().__init__(game_state)

        self.players = players

    def enter(self) -> None:
        super().enter()

        self.game_state.reset(self.players)
        for player in self.players:
            for _ in range(0, 7):
                player.draw_card(self.game_state.game_deck)
        self.game_state.drawn_deck.cards.append(self.game_state.game_deck.draw())
        self.game_state.now_color = self.game_state.drawn_deck.get_last().color

        from game.gameplay.flow.turnstart import TurnStartFlowNode

        self.machine.transition_to(TurnStartFlowNode(self.game_state))
