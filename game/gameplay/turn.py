class Turn:
    # clockwise: turn + 1, counter-clockwise: turn - 1
    _is_clockwise: bool
    _index: int
    _player_count: int

    def __init__(self, player_count: int) -> None:
        self._is_clockwise = True
        self._player_count = player_count
        self._index = 0

    def next(self) -> None:
        if self._is_clockwise:
            self._index += 1
            self._index %= self._player_count
        else:
            self._index -= 1
            if self._index < 0:
                self._index = self._player_count - 1

    def reverse(self) -> None:
        self._is_clockwise = not self._is_clockwise

    @property
    def current(self) -> int:
        return self._index
