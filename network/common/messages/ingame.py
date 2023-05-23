from dataclasses import dataclass, field
from enum import Enum

from game.gameplay.card import Card
from game.gameplay.gameparams import GameParams
from network.client.localgamestate import LocalGameState
from network.common.message import Message
from network.common.schema import NON_EMPTY_STRING


class InGameMessageType(Enum):
    GAME_STARTED = "game_started"
    CHANGE_COLOR = "change_color"
    CHANGE_COLOR_STARTED = "change_color_started"
    CHANGE_COLOR_FINISHED = "changed_color_finished"
    TURN_STARTED = "turn_started"
    CARD_EARNED = "card_earned"
    PLAY_CARD = "play_card"
    CARD_PLAYED = "card_played"
    GAME_ENDED = "game_ended"
    UNO = "uno"


@dataclass
class GameStarted(Message):
    state: LocalGameState
    start_index: int


@dataclass
class ChangeColor(Message):
    color: str


@dataclass
class PlayCard(Message):
    card: Card
