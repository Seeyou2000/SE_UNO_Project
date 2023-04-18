class Turn:
    # clockwise: turn + 1, counter-clockwise: turn - 1
    _is_clockwise: bool
    _index: int
    _player_count: int
    _total_turn: int

    def __init__(self, player_count: int) -> None:
        self._is_clockwise = True
        self._player_count = player_count
        self._index = 0
        self._total_turn = 0

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

    def skip(self, n: int) -> None:
        for _ in range(0, n):
            self.next()

    @property
    def current(self) -> int:
        return self._index

    @property
    def is_clockwise(self) -> bool:
        return self._is_clockwise
