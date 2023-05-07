from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


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
