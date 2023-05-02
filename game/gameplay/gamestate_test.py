from collections.abc import Callable

from game.constant import COLORABLEABILITY, COLORS, NAME, NONCOLORABLEABILITY
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

    deck_cards = game_state.game_deck.cards

    def count_deck_if(predicate: Callable[[Card], bool]) -> int:
        return len([card for card in deck_cards if predicate(card)])

    number_range = range(1, 10)

    # 숫자 카드 체크
    expected_colors_per_number = len(COLORS)

    for number_to_find in number_range:
        same_number_count = count_deck_if(lambda card: card.number == number_to_find)
        assert (
            same_number_count == expected_colors_per_number
        ), "같은 숫자를 가진 카드가 각 색깔별 하나씩 있어야 한다"

    # 색 별 카드 수량 체크
    expected_numbers_per_color = len(number_range)
    expected_abilities_per_color = len(COLORABLEABILITY)

    for color_to_find in COLORS:
        same_color_count = count_deck_if(lambda card: card.color == color_to_find)
        assert (
            same_color_count
            == expected_numbers_per_color + expected_abilities_per_color
        ), "같은 색을 가진 카드가 숫자 하나씩 + 능력 하나씩 있어야 한다"

    # 색 있는 능력카드 체크
    for colorable_ability_to_find in COLORABLEABILITY:
        same_colorable_ability_count = count_deck_if(
            lambda card: card.ability == colorable_ability_to_find
        )
        assert (
            same_colorable_ability_count == expected_abilities_per_color
        ), "한 색에 같은 능력을 가진 카드가 하나씩만 있어야 한다"

    # 색 없는 능력카드 체크
    expected_non_colorable_abilities = 1

    for noncolorable_ability_to_find in NONCOLORABLEABILITY:
        same_noncolorable_ability_count = count_deck_if(
            lambda card: card.ability == noncolorable_ability_to_find
        )
        assert (
            same_noncolorable_ability_count == expected_non_colorable_abilities
        ), "색 없는 능력 카드는 종류별로 하나씩만 있어야 한다"
