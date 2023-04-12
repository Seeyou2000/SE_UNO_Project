import pygame

from game.constant import NAME
from game.gameplay.flow.drawcard import DrawCardFlowNode
from game.gameplay.flow.gameflowmachine import GameFlowMachine
from game.gameplay.flow.prepare import PrepareFlowNode
from game.gameplay.gamestate import GameState
from game.gameplay.player import Player


def test_draw_card() -> None:
    pygame.font.init()
    player_count = 2
    game_state = GameState()
    flow = GameFlowMachine()
    flow.transition_to(
        PrepareFlowNode(game_state, [Player(name) for name in NAME[:player_count]])
    )
    before_cards = len(game_state.players[0].cards)
    flow.transition_to(DrawCardFlowNode(game_state))
    after_cards = len(game_state.players[0].cards)
    assert before_cards + 1 == after_cards
    assert len(game_state.get_current_player().cards) == before_cards
