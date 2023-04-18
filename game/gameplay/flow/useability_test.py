from game.constant import AbilityType
from game.gameplay.aiplayer import AIPlayer
from game.gameplay.card import Card
from game.gameplay.flow.gameflowmachine import GameFlowMachine
from game.gameplay.flow.validatecard import ValidateCardFlowNode
from game.gameplay.gamestate import GameState


def test_give_four(flow_machine_2p: GameFlowMachine, game_state: GameState) -> None:
    game_state.now_color = "red"
    attacker = game_state.get_current_player()
    attacker.cards[0] = Card("red", None, AbilityType.GIVE_FOUR_CARDS)

    victim = game_state.get_next_player()
    victim.cards = [Card("red", 1, None) for _ in range(0, 7)]

    assert game_state.get_current_player() is attacker, "공격자가 현재 플레이어인지 확인"

    before_attacked_player_cards = len(victim.cards)
    flow_machine_2p.transition_to(ValidateCardFlowNode(game_state, attacker.cards[0]))
    after_attacked_player_cards = len(victim.cards)

    assert (before_attacked_player_cards + 4) == after_attacked_player_cards, "4장 주기"


def test_skip(flow_machine_2p: GameFlowMachine, game_state: GameState) -> None:
    game_state.now_color = "red"
    attacker = game_state.get_current_player()
    attacker.cards[0] = Card("red", None, AbilityType.SKIP_ORDER)

    victim = game_state.get_next_player()
    victim.cards = [Card("red", 1, None) for _ in range(0, 7)]

    assert game_state.get_current_player() is attacker, "공격자가 현재 플레이어인지 확인"

    flow_machine_2p.transition_to(ValidateCardFlowNode(game_state, attacker.cards[0]))

    assert game_state.get_current_player() is attacker, "스킵 후 다시 자기 차례인가?"


def test_ai_skip(
    flow_machine_2p_ai: tuple[GameFlowMachine, AIPlayer], game_state: GameState
) -> None:
    flow, ai = flow_machine_2p_ai
    game_state.now_color = "red"
    attacker = game_state.get_current_player()
    attacker.cards[0] = Card("red", None, AbilityType.SKIP_ORDER)

    victim = game_state.get_next_player()
    victim.cards = [Card("red", 1, None) for _ in range(0, 7)]

    assert attacker is ai.player, "공격자가 AI인지 확인"

    flow.transition_to(ValidateCardFlowNode(game_state, attacker.cards[0]))
    ai.update(4)

    assert game_state.get_current_player() is attacker, "스킵 후 다시 자기 차례인가?"

    ai.update(4)
    # flow.transition_to(ValidateCardFlowNode(game_state, attacker.cards[0]))

    assert game_state.get_current_player() is victim, "AI가 연속으로 내는가?"
