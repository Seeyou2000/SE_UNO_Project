import pygame

from game.constant import NAME
from game.gameplay.gamestate import GameState
from game.gameplay.player import Player


def test_weighted_draw() -> None:
    player_count = 2
    game_state = GameState()
    game_state.reset([Player(name) for name in NAME[:player_count]])

    # 로직상의 매직넘버
    weighted_cards_at_once = 7
    ability_count = 0
    number_count = 0
    for i in range(0, round(1000 / weighted_cards_at_once)):
        cards = game_state.weighty_draw_cards()
        for _ in range(0, weighted_cards_at_once):
            card = cards.pop()
            if card.ability is not None:
                ability_count += 1
            elif card.number is not None:
                number_count += 1

    print(ability_count, number_count)

    target = 600
    tolerance = 600 * 0.05
    assert abs(ability_count - target) <= tolerance
