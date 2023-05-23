from dataclasses import dataclass
from enum import Enum

from game.gameplay.gameparams import GameParams
from network.common.message import Message


class HostMessageType(Enum):
    START_GAME = "start_game"
    ADD_AI = "add_ai"
    OPEN_PLAYER_SLOT = "open_player_slot"
    CLOSE_PLAYER_SLOT = "close_player_slot"
    SWAP_PLAYER_SLOT = "swap_player_slot"
    KICK_PLAYER = "kick_player"


@dataclass
class StartGame(Message):
    game_params: GameParams


@dataclass
class AddAI(Message):
    slot_index: int
    ai_type: int


@dataclass
class OpenPlayerSlot(Message):
    slot_index: int


@dataclass
class ClosePlayerSlot(Message):
    slot_index: int


@dataclass
class SwapPlayerSlot(Message):
    before_slot_index: int
    after_slot_index: int


@dataclass
class KickPlayer(Message):
    slot_index: int
