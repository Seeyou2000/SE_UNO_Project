import pygame

from game.constant import NAME, ColorableAbilityType
from game.gameplay.card import Card
from game.gameplay.flow.abilitycard import AbilityCardFlowNode
from game.gameplay.flow.gameflowmachine import GameFlowMachine
from game.gameplay.flow.gamestart import GameStartFlowNode
from game.gameplay.gamestate import GameState
from game.gameplay.player import Player


def test_abilitycard():
    pygame.font.init()
    player_count = 2
    game_state = GameState()
    flow = GameFlowMachine()
    flow.transition_to(
        GameStartFlowNode(game_state, [Player(name) for name in NAME[:player_count]])
    )
    game_state.now_color = "red"
    game_state.players[0].cards[0] = Card(
        "red", None, ColorableAbilityType.GIVE_FOUR_CARDS
    )

    game_state.players[1].cards = [Card("red", 1, None) for _ in range(0, 7)]
    # before_cardlen = len(game_state.players[0].cards)
    # before_turn = game_state.turn.current

    before_attacked_player_cards = len(game_state.players[1].cards)

    flow.transition_to(AbilityCardFlowNode(game_state, game_state.players[0].cards[0]))
    # after_cardlen = len(game_state.players[0].cards)
    after_attacked_player_cards = len(game_state.players[1].cards)

    assert (before_attacked_player_cards + 4) == after_attacked_player_cards
