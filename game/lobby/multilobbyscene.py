import pygame
import socketio
from loguru import logger

from engine.button import Button
from engine.layout import Horizontal, LayoutAnchor, Vertical
from engine.scene import Scene
from engine.text import Text
from engine.textinput import TextInput
from engine.world import World
from game.constant import NAME
from game.font import FontType, get_font
from game.lobby.createroommodal import CreateRoomModal
from game.lobby.roomlistitem import RoomListItem
from game.messagemodal import MessageModal
from network.common.messages import parse_message
from network.common.models import LobbyRoom


class MultiLobbyScene(Scene):
    room_list: list[RoomListItem]

    def __init__(self, world: World) -> None:
        super().__init__(world)

        self.font = get_font(FontType.UI_BOLD, 16)
        self.room_list = []
        self.place_ui(world)

    def place_ui(self, world: World) -> None:
        ip_input = TextInput(
            "http://127.0.0.1:10008",
            pygame.Rect(0, 0, 300, 60),
            self.font,
            pygame.Color("black"),
            30,
            self.focus_controller,
        )
        self.focus_controller.add(ip_input)

        connect_button = Button(
            "접속",
            pygame.Rect(0, 0, 80, 60),
            self.font,
            lambda _: self.try_connect(ip_input.text),
        )

        refresh_button = Button(
            "새로고침", pygame.Rect(0, 0, 80, 60), self.font, lambda _: self.refresh_lobby()
        )
        self.add_child(refresh_button)
        self.layout.add(refresh_button, LayoutAnchor.TOP_RIGHT, pygame.Vector2(-50, 50))

        from game.menu.menuscene import MenuScene

        change_menu_scene = Button(
            "뒤로가기",
            pygame.Rect(0, 0, 80, 60),
            self.font,
            lambda _: world.director.change_scene(MenuScene(world)),
        )
        self.add_child(change_menu_scene)
        self.layout.add(
            change_menu_scene, LayoutAnchor.BOTTOM_RIGHT, pygame.Vector2(-50, -50)
        )

        create_room_button = Button(
            "방 만들기",
            pygame.Rect(0, 0, 80, 60),
            self.font,
            lambda _: self.show_create_room_modal(),
        )
        self.add_child(create_room_button)
        self.layout.add(
            create_room_button, LayoutAnchor.BOTTOM_RIGHT, pygame.Vector2(-150, -50)
        )

        name_text = Text(
            "PLAYER NAME",
            pygame.Vector2(0, 0),
            get_font(FontType.UI_BOLD, 16),
            pygame.Color("gray"),
        )

        name_input = TextInput(
            NAME[0],
            pygame.Rect(0, 0, 300, 60),
            get_font(FontType.UI_BOLD, 30),
            pygame.Color("black"),
            10,
            self.focus_controller,
        )

        self.add_child(
            Vertical(
                pygame.Vector2(50, 600),
                20,
                [name_text, name_input],
            )
        )
        self.focus_controller.add(name_input)

        gap = 30
        self.add_child(
            Vertical(
                pygame.Vector2(50, 50),
                gap,
                [
                    Horizontal(pygame.Vector2(0, 0), gap, [ip_input, connect_button]),
                ],
            )
        )

    def show_create_room_modal(self) -> None:
        self.create_room_modal = CreateRoomModal(self)
        self.layout.add(
            self.create_room_modal, LayoutAnchor.CENTER, pygame.Vector2(0, 0)
        )
        self.open_modal(self.create_room_modal)

    def refresh_lobby(self) -> None:
        rooms: list[LobbyRoom] = clientio.call("room_list")

        if len(self.room_list) != 0:
            for room in self.room_list:
                self.remove_child(room)
            self.room_list.clear()

        for data in rooms:
            room = parse_message(LobbyRoom, data, "FAILED REFRESH")
            if room is None:
                return False
            room_info = RoomListItem(
                self,
                room,
                pygame.Rect(0, 0, 1200, 60),
                self.font,
                pygame.Color("black"),
            )
            self.room_list.append(room_info)
        for i, item in enumerate(self.room_list):
            self.layout.add(
                item, LayoutAnchor.TOP_CENTER, pygame.Vector2(0, 80 * i + 150)
            )
            self.focus_controller.add(item)
        self.add_children(self.room_list)

    def try_connect(self, server_ip: str) -> None:
        try:
            clientio.connect(server_ip, auth={"username": "Test Player"})
            rooms: list[LobbyRoom] = clientio.call("room_list")
            logger.info(rooms)

        except socketio.client.exceptions.ConnectionError as e:
            logger.error(f"방 접속 실패 {e}")
