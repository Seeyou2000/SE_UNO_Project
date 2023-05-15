import abc

from game.gameplay.aicontroller import AIController
from network.server.common.user.usersession import UserSession


class RoomPlayer(abc.ABC):
    """
    방에 참가한 플레이어를 나타내는 클래스
    """

    @abc.abstractmethod
    def get_name(self) -> str:
        pass


class RoomHumanPlayer(RoomPlayer):
    user: UserSession

    def __init__(self, user: UserSession) -> None:
        super().__init__()
        self.user = user

    def get_name(self) -> str:
        return self.user.name


class RoomAIPlayer(RoomPlayer):
    controller: AIController

    def __init__(self, controller: AIController) -> None:
        super().__init__()
        self.controller = controller

    def get_name(self) -> str:
        return "AI"
