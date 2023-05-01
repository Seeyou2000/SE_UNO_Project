import pygame

from game.constant import (
    COLORABLEABILITY,
    COLORS,
    NAME,
    NONCOLORABLEABILITY,
)
from game.gameplay.card import Card
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


def test_create_full_deck_cards() -> None:
    player_count = 2
    game_state = GameState()
    game_state.reset([Player(name) for name in NAME[:player_count]])
    not_exist = 0

    full_deck_num = (
        9 * len(COLORS) + len(COLORABLEABILITY) * len(COLORS) + len(NONCOLORABLEABILITY)
    )

    assert len(game_state.game_deck.cards) == full_deck_num

    newcards = [Card(color, number) for number in (range(1, 10)) for color in COLORS]
    newcards += [
        Card(color, None, ability) for ability in COLORABLEABILITY for color in COLORS
    ]
    newcards += [Card("black", None, ability) for ability in NONCOLORABLEABILITY]

    game_deck = [card.info() for card in game_state.game_deck.cards]

    for i in range(full_deck_num):
        if newcards[i].info() not in game_deck:
            not_exist = 1
        else:
            for j in range(len(game_state.game_deck.cards)):
                if newcards[i].info() == game_state.game_deck.cards[j].info():
                    game_state.game_deck.cards.remove(game_state.game_deck.cards[j])
                    break

    assert len(game_state.game_deck.cards) == 0, "중복된 카드 존재"
    assert not_exist == 0, "생성되지 않은 카드 존재"
