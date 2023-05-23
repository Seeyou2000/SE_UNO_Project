import abc

from game.gameplay.aicontroller import AIController
from network.common.models import PreGameRoomPlayer
from network.server.common.user.usersession import UserSession


class RoomPlayer(abc.ABC):
    """
    방에 참가한 플레이어를 나타내는 클래스
    """

    @abc.abstractmethod
    def get_name(self) -> str:
        pass

    @abc.abstractmethod
    def as_pregame_room_player(self) -> PreGameRoomPlayer:
        pass


class RoomHumanPlayer(RoomPlayer):
    user: UserSession

    def __init__(self, user: UserSession) -> None:
        super().__init__()
        self.user = user

    def get_name(self) -> str:
        return self.user.name

    def as_pregame_room_player(self) -> PreGameRoomPlayer:
        return PreGameRoomPlayer(self.user.id, self.get_name(), False, None)


class RoomAIPlayer(RoomPlayer):
    controller: AIController

    def __init__(self, id: str, controller: AIController) -> None:
        super().__init__()
        self.id = id
        self.controller = controller

    def get_name(self) -> str:
        return "AI"

    def as_pregame_room_player(self) -> PreGameRoomPlayer:
        return PreGameRoomPlayer(
            self.id, self.get_name(), True, self.controller.type.value
        )
