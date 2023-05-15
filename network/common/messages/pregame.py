from dataclasses import dataclass, field
from enum import Enum

from network.common.message import Message
from network.common.schema import NON_EMPTY_STRING


class PreGameMessageType(Enum):
    HOST_CHANGED = "host_changed"
    HUMAN_REMOVED = "room_player_removed"
    HUMAN_ADDED = "room_player_added"
    AI_REMOVED = "room_player_removed"
    AI_ADDED = "room_player_added"
    PLAYER_NAME_CHANGED = "room_player_name_changed"
    PLAYER_SLOT_OPENED = "player_slot_opened"
    QUIT_ROOM = "quit_room"


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
