from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin

from game.gameplay.card import Card
from game.gameplay.player import Player
from game.gameplay.timer import Timer
from game.gameplay.turn import Turn


@dataclass
class LocalGameState(DataClassJsonMixin):
    """네트워크를 통해 동기화되는 상태. 전체를 복제하진 않는다."""

    players: list[Player]
    turn: Turn = Turn(6)
    turn_timer: Timer = Timer(5)

    def get_current_player(self) -> Player:
        return self.players[self.turn.current]

    def get_next_player(self) -> Player:
        for player in self.players:
            if self.is_player_next_turn(player):
                return player

    def is_player_next_turn(self, player: Player) -> bool:
        is_clockwise = self.turn.is_clockwise
        target_turn_diff = -1 if is_clockwise else 1

        player_index = self.players.index(player)
        current_index = self.turn.current
        diff = current_index - player_index
        reverse_diff = (
            diff - len(self.players) if is_clockwise else diff + len(self.players)
        )
        return (diff == target_turn_diff) or (reverse_diff == target_turn_diff)
