import pygame
from loguru import logger

from engine.events.event import Event
from engine.focus import Focusable
from engine.gameobjectcontainer import GameObjectContainer
from engine.layout import Layout, LayoutAnchor
from engine.scene import Scene
from engine.text import Text
from game.lobby.validatepasswordmodal import ValidatePasswordModal
from game.messagemodal import MessageModal
from network.client.client import clientio
from network.common.messages import JoinRoom
from network.common.models import LobbyRoom


class RoomListItem(GameObjectContainer, Focusable):
    font: pygame.font.Font
    color: pygame.Color

    def __init__(
        self,
        scene: Scene,
        room: LobbyRoom,
        rect: pygame.Rect,
        font: pygame.font.Font,
        color: pygame.Color,
    ) -> None:
        super().__init__()
        self.scene = scene
        self.room = room
        self.font = font
        self.color = color
        self.rect = rect.copy()
        self.layout = Layout(self.rect)
        self.room_id = room.id
        self.room_name = Text(room.name, pygame.Vector2(0, 0), self.font, self.color)
        self.player_data = Text(
            str(room.current_player) + "/" + str(room.max_player),
            pygame.Vector2(0, 0),
            self.font,
            self.color,
        )
        self.is_private = room.is_private
        self.password_is_exist = Text(
            "비밀번호 O", pygame.Vector2(0, 0), self.font, self.color
        )
        self.password_is_not_exist = Text(
            "비밀번호 X", pygame.Vector2(0, 0), self.font, self.color
        )
        self.room_data = []

        self.layout.add(self.room_name, LayoutAnchor.MIDDLE_LEFT, pygame.Vector2(10, 0))
        self.layout.add(self.player_data, LayoutAnchor.CENTER, pygame.Vector2(0, 0))
        self.layout.add(
            self.password_is_exist, LayoutAnchor.MIDDLE_RIGHT, pygame.Vector2(-10, 0)
        )
        self.layout.add(
            self.password_is_not_exist,
            LayoutAnchor.MIDDLE_RIGHT,
            pygame.Vector2(-10, 0),
        )

        self.on("click", self.try_enter_room)

        if self.is_private:
            self.room_data = [
                self.room_name,
                self.player_data,
                self.password_is_exist,
            ]
            self.add_children(self.room_data)
        else:
            self.room_data = [
                self.room_name,
                self.player_data,
                self.password_is_not_exist,
            ]
            self.add_children(self.room_data)

        self.layout.update(0)

    def render(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface,
            pygame.Color("#fff1e7"),
            self.absolute_rect,
            border_radius=8,
        )

        if self.has_focus:
            focus_ring_rect = self.absolute_rect.copy()
            pygame.draw.rect(
                surface,
                pygame.Color("#FF9549"),
                focus_ring_rect,
                width=2,
                border_radius=8,
            )
        super().render(surface)

    def try_enter_room(self, event: Event) -> None:
        if self.is_private:
            self.show_validate_room_modal()
        else:
            self.enter_room()

    def show_validate_room_modal(self) -> None:
        self.validate_room_modal = ValidatePasswordModal(self.scene, self.enter_room)
        self.scene.open_modal(self.validate_room_modal)

    def show_connect_fail_modal(self) -> None:
        self.connect_fail_modal = MessageModal(self.scene, "접속에 실패했습니다.")
        self.scene.open_modal(self.connect_fail_modal)

    def enter_room(self, password: str | None = None) -> None:
        success = clientio.call("join_room", JoinRoom(self.room_id, password).to_dict())
        if success:
            pass  # 방 안에 들어가는 거(동훈이 코드 필요.)
        else:
            self.show_connect_fail_modal()
        logger.info(success)
