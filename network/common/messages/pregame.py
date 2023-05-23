from dataclasses import dataclass, field
from enum import Enum

from network.common.message import Message
from network.common.models import PreGameRoom
from network.common.schema import NON_EMPTY_STRING


class PreGameMessageType(Enum):
    ROOM_STATE_CHANGED = "room_state_changed"
    PLAYER_NAME_CHANGED = "room_player_name_changed"
    QUIT_ROOM = "quit_room"


@dataclass
class RoomStateChanged(Message):
    room: PreGameRoom


@dataclass
class HostChanged(Message):
    new_host_id: str


@dataclass
class HumanRemoved(Message):
    id: str


@dataclass
class HumanAdded(Message):
    id: str
    name: str


@dataclass
class AIRemoved(Message):
    id: str


@dataclass
class AIAdded(Message):
    id: str
    name: str


@dataclass
class PlayerNameChanged(Message):
    before_name: str = field(metadata=NON_EMPTY_STRING)
    after_name: str = field(metadata=NON_EMPTY_STRING)


@dataclass
class PlayerSlotOpened(Message):
    slot_index: int
