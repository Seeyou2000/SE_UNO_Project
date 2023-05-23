from enum import Enum

from engine.button import Button
from engine.focus import FocusController
from engine.gameobjectcontainer import GameObjectContainer
from network.common.models import PreGameRoomPlayer


class SlotStatusType(Enum):
    CLOSE = 0
    OPEN = 1


SlotState = PreGameRoomPlayer | SlotStatusType


# class Slot(GameObjectContainer):
#     def __init__(self, slot: SlotState, focus_controller: FocusController) -> None:
#         super().__init__()

#         self.place_child()
#         self.set_state(slot)

#     def place_child(self) -> None:
#         self.ai_player_button = Button()

#     def set_state(self, slot: SlotState) -> None:
#         match slot:
#             case PreGameRoomPlayer(is_ai=True):
#                 self.ai_player_button.is_visible = False
#             case PreGameRoomPlayer():
#                 self.
