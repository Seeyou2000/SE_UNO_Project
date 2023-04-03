import pygame

from game.constant import NAME
from game.gameplay.gamestate import GameState
from game.gameplay.player import Player


def test_gamestate():
    pygame.font.init()
    player_count = 2
    game_state = GameState()
    game_state.reset([Player(name) for name in NAME[:player_count]])
    before_player = game_state.get_current_player()
    game_state.turn.next()
    next_player = game_state.get_current_player()
    assert before_player != next_player
