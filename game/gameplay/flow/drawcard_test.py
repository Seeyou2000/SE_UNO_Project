import pygame

from game.gameplay.flow.drawcard import DrawCardFlowNode
from game.gameplay.flow.gameflowmachine import GameFlowMachine, GameFlowMachineEventType
from game.gameplay.flow.gamestart import GameStartFlowNode
from game.gameplay.gamestate import GameState
from game.scene.constant import NAME
from game.scene.player import Player


def test_draw_card():
    pygame.font.init()
    player_count = 2
    game_state = GameState()
    flow = GameFlowMachine()
    flow.transition_to(
        GameStartFlowNode(game_state, [Player(name) for name in NAME[:player_count]])
    )
    before_cards = len(game_state.players[0].cards)
    flow.transition_to(DrawCardFlowNode(game_state))
    after_cards = len(game_state.players[0].cards)
    assert before_cards + 1 == after_cards
    assert len(game_state.get_current_player().cards) == before_cards
