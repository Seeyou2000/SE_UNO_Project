from dataclasses import dataclass, field
from enum import Enum

from game.gameplay.aicontroller import AIType
from game.gameplay.gameparams import GameParams
from network.common.message import Message
from network.common.schema import NON_EMPTY_STRING


class HostMessageType(Enum):
    START_GAME = "start_game"
    ADD_AI = "add_ai"
    OPEN_PLAYER_SLOT = "open_player_slot"
    CHANGE_PLAYER_SLOT = "change_player_slot"
    KICK_PLAYER = "kick_player"


@dataclass
class StartGame(Message):
    game_params: GameParams


@dataclass
class AddAI(Message):
    slot_index: int
    ai_type: AIType


@dataclass
class OpenPlayerSlot(Message):
    slot_index: int


@dataclass
class SwapPlayerSlot(Message):
    before_slot_index: int
    after_slot_index: int


@dataclass
class KickPlayer(Message):
    slot_index: int
