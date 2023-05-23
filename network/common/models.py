from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin

from game.gameplay.aicontroller import AIType
from game.gameplay.gameparams import GameParams


class Model(DataClassJsonMixin):
    pass


@dataclass
class LobbyRoom(Model):
    id: str
    name: str
    host_player_name: str
    current_player: int
    max_player: int
    is_private: bool
    is_game_started: bool


@dataclass
class PreGameRoomPlayer(Model):
    id: str
    name: str
    is_ai: bool
    ai_type: int | None


@dataclass
class PreGameRoomSlot(Model):
    slot_index: int
    status: int | None = None
    player: PreGameRoomPlayer | None = None


@dataclass
class PreGameRoom(Model):
    id: str
    host: PreGameRoomPlayer
    slots: list[PreGameRoomSlot]
    game_params: GameParams
