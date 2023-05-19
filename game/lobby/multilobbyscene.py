import pygame

from engine.button import Button
from engine.events.event import Event
from engine.layout import LayoutAnchor, LayoutConstraint, Vertical
from engine.scene import Scene
from engine.text import Text
from engine.textinput import TextInput
from engine.world import World
from game.constant import NAME
from game.font import FontType, get_font
from game.lobby.createroommodal import CreateRoomModal
from game.lobby.roomlistitem import RoomListItem
from network.client.client import clientio
from network.common.messages import parse_message
from network.common.models import LobbyRoom


class MultiLobbyScene(Scene):
    room_list: list[RoomListItem]

    def __init__(self, world: World) -> None:
        super().__init__(world)

        self.font = get_font(FontType.UI_BOLD, 16)
        self.room_list = []
        self.place_ui(world)
        self.refresh_lobby()

    def place_ui(self, world: World) -> None:
        refresh_button = Button(
            "새로고침",
            pygame.Rect(0, 0, 180, 60),
            self.font,
            lambda _: self.refresh_lobby(),
        )
        self.add(
            refresh_button,
            LayoutConstraint(LayoutAnchor.TOP_RIGHT, pygame.Vector2(-50, 50)),
        )

        change_menu_scene = Button(
            "메뉴로 돌아가기",
            pygame.Rect(0, 0, 180, 60),
            self.font,
            self.change_to_menuscene,
        )
        self.add(
            change_menu_scene,
            LayoutConstraint(LayoutAnchor.TOP_LEFT, pygame.Vector2(50, 50)),
        )

        create_room_button = Button(
            "방 만들기",
            pygame.Rect(0, 0, 180, 60),
            self.font,
            lambda _: self.show_create_room_modal(),
        )
        self.add(
            create_room_button,
            LayoutConstraint(LayoutAnchor.BOTTOM_RIGHT, pygame.Vector2(-50, -50)),
        )

        name_text = Text(
            "플레이어 이름",
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
        self.focus_controller.add(name_input)

        name_area = Vertical(
            pygame.Vector2(),
            20,
            [name_text, name_input],
        )
        self.add(
            name_area,
            LayoutConstraint(LayoutAnchor.BOTTOM_LEFT, pygame.Vector2(50, -50)),
        )

        self.empty_lobby_text = Text(
            "방을 만들어보세요!",
            pygame.Vector2(),
            get_font(FontType.UI_BOLD, 30),
            pygame.Color("#ffaa6e"),
        )
        self.add(
            self.empty_lobby_text,
            LayoutConstraint(LayoutAnchor.CENTER, pygame.Vector2()),
        )

    def show_create_room_modal(self) -> None:
        self.create_room_modal = CreateRoomModal(self)
        self.open_modal(self.create_room_modal)

    def refresh_lobby(self) -> None:
        rooms: list[LobbyRoom] = clientio.call("room_list")

        if len(self.room_list) != 0:
            for room in self.room_list:
                self.remove_child(room)
            self.room_list.clear()

        for data in rooms:
            room = parse_message(LobbyRoom, data, "새로고침")
            if room is None:
                return
            room_info = RoomListItem(
                self,
                room,
                pygame.Rect(0, 0, 1200, 60),
            )
            self.room_list.append(room_info)
        for i, item in enumerate(self.room_list):
            self.layout.add(
                item, LayoutAnchor.TOP_CENTER, pygame.Vector2(0, 80 * i + 150)
            )
            self.focus_controller.add(item)
        self.add_children(self.room_list)

        self.empty_lobby_text.is_visible = len(self.room_list) == 0

    def change_to_menuscene(self, e: Event) -> None:
        from game.menu.menuscene import MenuScene

        self.world.director.change_scene(MenuScene(self.world))
        clientio.disconnect()
