from dataclasses import dataclass, field
from enum import Enum

from network.common.message import Message
from network.common.schema import NON_EMPTY_STRING


class CommonMessageType(Enum):
    CONNECTED = "connected"
    CHANGE_PLAYER_NAME = "change_player_name"
    PLAYER_NAME_CHANGED = "player_name_changed"


@dataclass
class Connected(Message):
    id: str


@dataclass
class ChangePlayerName(Message):
    new_name: str = field(metadata=NON_EMPTY_STRING)


@dataclass
class PlayerNameChanged(Message):
    id: str = field(metadata=NON_EMPTY_STRING)
    new_name: str = field(metadata=NON_EMPTY_STRING)
