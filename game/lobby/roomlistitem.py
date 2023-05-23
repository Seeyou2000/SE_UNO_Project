import pygame
from loguru import logger

from engine.button import BaseButton, create_default_button_surfaces
from engine.events.event import Event
from engine.gameobjectcontainer import GameObjectContainer
from engine.layout import Layout, LayoutAnchor
from engine.scene import Scene
from engine.text import Text
from game.font import FontType, get_font
from game.lobby.validatepasswordmodal import ValidatePasswordModal
from game.messagemodal import MessageModal
from network.common.messages.lobby import JoinRoom
from network.common.models import LobbyRoom


class RoomListItem(BaseButton, GameObjectContainer):
    font: pygame.font.Font
    text_color: pygame.Color

    def __init__(
        self,
        scene: Scene,
        room: LobbyRoom,
        rect: pygame.Rect,
    ) -> None:
        surface_rect = pygame.Rect(0, 0, rect.width, rect.height)

        super().__init__(
            rect.copy(), create_default_button_surfaces(surface_rect, surface_rect, 10)
        )
        self.scene = scene
        self.room = room
        self.layout = Layout(self.rect)

        self.text_color = pygame.Color("black")
        self.sub_text_color = pygame.Color("#222222")
        self.font_size = 20

        self.room_id = room.id
        self.room_name = Text(
            room.name,
            pygame.Vector2(0, 0),
            get_font(FontType.UI_BOLD, self.font_size),
            self.text_color,
        )
        self.player_data = Text(
            str(room.current_player) + "/" + str(room.max_player),
            pygame.Vector2(0, 0),
            get_font(FontType.UI_NORMAL, self.font_size),
            self.text_color,
        )
        self.is_private = room.is_private
        self.password_is_exist = Text(
            "비밀",
            pygame.Vector2(0, 0),
            get_font(FontType.UI_NORMAL, self.font_size),
            self.sub_text_color,
        )
        self.password_is_not_exist = Text(
            "공개",
            pygame.Vector2(0, 0),
            get_font(FontType.UI_NORMAL, self.font_size),
            self.sub_text_color,
        )
        self.room_data = []

        self.layout.add(self.room_name, LayoutAnchor.MIDDLE_LEFT, pygame.Vector2(40, 0))
        self.layout.add(
            self.player_data, LayoutAnchor.MIDDLE_RIGHT, pygame.Vector2(-120, 0)
        )
        self.layout.add(
            self.password_is_exist, LayoutAnchor.MIDDLE_RIGHT, pygame.Vector2(-40, 0)
        )
        self.layout.add(
            self.password_is_not_exist,
            LayoutAnchor.MIDDLE_RIGHT,
            pygame.Vector2(-40, 0),
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
        super().render(surface)
        GameObjectContainer.render(self, surface)

        if self.has_focus:
            focus_ring_rect = self.absolute_rect.copy()
            pygame.draw.rect(
                surface,
                pygame.Color("#FF9549"),
                focus_ring_rect,
                width=2,
                border_radius=8,
            )

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
        success = self.scene.io.call(
            "join_room", JoinRoom(self.room_id, password).to_dict()
        )
        if success:
            pass  # 방 안에 들어가는 거(동훈이 코드 필요.)
        else:
            self.show_connect_fail_modal()
        logger.info(success)
