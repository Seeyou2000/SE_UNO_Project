from game.gameplay.turn import Turn


def test_turn() -> None:
    player_count = 2
    turn = Turn(player_count)
    assert turn.current == 0
    turn.next()
    assert turn.current == 1
    turn.next()
    assert turn.current == 0
