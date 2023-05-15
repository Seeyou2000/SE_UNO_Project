from dataclasses import dataclass, field
from enum import Enum

from network.common.message import Message
from network.common.schema import NON_EMPTY_STRING


class LobbyMessageType(Enum):
    CREATE_ROOM = "create_room"
    ROOM_CREATED = "room_created"
    JOIN_ROOM = "join_room"
    QUIT_LOBBY = "quit_lobby"


@dataclass
class CreateRoom(Message):
    name: str = field(metadata=NON_EMPTY_STRING)
    password: str | None = None


@dataclass
class JoinRoom(Message):
    id: str = field(metadata=NON_EMPTY_STRING)
    password: str | None = None
