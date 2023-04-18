from game.gameplay.flow.drawcard import DrawCardFlowNode
from game.gameplay.flow.gameflowmachine import GameFlowMachine
from game.gameplay.gamestate import GameState


def test_draw_card(flow_machine_2p: GameFlowMachine, game_state: GameState) -> None:
    current_player = game_state.get_current_player()
    before_cards = len(current_player.cards)
    flow_machine_2p.transition_to(DrawCardFlowNode(game_state))
    after_cards = len(current_player.cards)
    assert before_cards + 1 == after_cards
