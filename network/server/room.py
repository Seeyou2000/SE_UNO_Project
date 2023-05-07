from dataclasses import dataclass
from enum import Enum

from network.common.models import LobbyRoom


class PlayerLocation(Enum):
    LOBBY = 0
    ROOM = 1


@dataclass
class PlayerSession:
    name: str
    sid: str
    current_location: PlayerLocation


class ServerRoomMetadata:
    id: str
    name: str
    host_player: PlayerSession
    players: dict[int, PlayerSession]
    password: str | None

    def __init__(
        self, id: str, name: str, host_player: PlayerSession, password: str | None
    ) -> None:
        self.id = id
        self.name = name

        assert isinstance(host_player, PlayerSession)
        self.host_player = host_player
        self.players = {}
        self.password = password

    def convert_to_lobby(self) -> LobbyRoom:
        return LobbyRoom(
            self.id,
            self.name,
            self.host_player.name,
            len(self.players.values()),
            6,
            self.password is not None,
        )

    def __str__(self) -> str:
        return f"ServerRoomMetadata(id: {self.id}, name: {self.name}, host:{self.host_player.name})"  # noqa: E501
