import pygame

from game.constant import NAME
from game.gameplay.flow.gameflowmachine import GameFlowMachine
from game.gameplay.flow.gamestart import GameStartFlowNode
from game.gameplay.flow.numbercard import NumberCardFlowNode
from game.gameplay.gamestate import GameState
from game.gameplay.player import Player


def test_numbercard():
    pygame.font.init()
    player_count = 2
    game_state = GameState()
    flow = GameFlowMachine()
    flow.transition_to(
        GameStartFlowNode(game_state, [Player(name) for name in NAME[:player_count]])
    )
    # game_state.drawn_deck.get_last().number = 1
    game_state.now_color = "red"
    # game_state.players[0].cards[0].number = 1
    game_state.players[0].cards[0].color = "red"
    before_cardlen = len(game_state.players[0].cards)
    before_turn = game_state.turn.current
    flow.transition_to(NumberCardFlowNode(game_state, game_state.players[0].cards[0]))
    after_cardlen = len(game_state.players[0].cards)
    assert before_cardlen == after_cardlen + 1  # "카드가 잘 내졌는지(이전보다 한 장 줄었는지) 검사"
    assert before_turn + 1 == game_state.turn.current
