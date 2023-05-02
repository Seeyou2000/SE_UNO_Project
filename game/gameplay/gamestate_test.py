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

    full_deck_num = (
        9 * len(COLORS) + len(COLORABLEABILITY) * len(COLORS) + len(NONCOLORABLEABILITY)
    )

    assert len(game_state.game_deck.cards) == full_deck_num

    card_deck = []
    for i in range(len(game_state.game_deck.cards)):
        card_index = str(game_state.game_deck.cards[i])
        card_deck.append(card_index)

    for i in range(full_deck_num):
        print(card_deck[i])

    # 숫자 카드 체크
    error_num = 0
    for find_num in range(1, 10):
        find_num_card = str(find_num)
        num_list = [s for s in card_deck if find_num_card in s]
        print(len(num_list))
        if len(num_list) != 4:
            error_num = find_num
            break

    assert error_num == 0, "error_num 숫자카드 수량 이상 발생"

    # 색 별 카드 수량 체크
    error_color = 0
    for find_color in COLORS:
        find_color_card = str(find_color)
        color_list = [s for s in card_deck if find_color_card in s]
        print(len(color_list))
        if len(color_list) != 9 + len(COLORABLEABILITY):
            error_color = find_color
            break

    assert error_color == 0, "error_color 색 카드 수량 이상 발생"

    # 색 있는 능력카드 체크
    error_colorability = 0
    for find_colorability in COLORABLEABILITY:
        find_colorability_card = str(find_colorability)
        colorability_list = [s for s in card_deck if find_colorability_card in s]
        print(len(colorability_list))
        if len(colorability_list) != len(COLORABLEABILITY):
            error_colorability = find_colorability
            break

    assert error_colorability == 0, "색 있는 능력카드 수량 이상 발생"

    # 색 없는 능력카드 체크
    noncolor_card_num = 0
    for find_noncolorability in NONCOLORABLEABILITY:
        noncolor_list = [s for s in card_deck if str(find_noncolorability) in s]
        print(len(noncolor_list))
        noncolor_card_num += len(noncolor_list)
    assert noncolor_card_num == len(NONCOLORABLEABILITY), "색 없는 능력 카드 수량 이상 발생"
