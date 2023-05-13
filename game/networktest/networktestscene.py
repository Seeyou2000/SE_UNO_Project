import pygame
import socketio
from loguru import logger

from engine.button import Button
from engine.layout import Horizontal, Vertical
from engine.scene import Scene
from engine.textinput import TextInput
from engine.world import World
from game.font import FontType, get_font
from network.client.client import clientio
from network.common.messages import CreateRoom, JoinRoom
from network.common.models import LobbyRoom


class NetworkTestScene(Scene):
    def __init__(self, world: World) -> None:
        super().__init__(world)
        self.place_ui()

    def place_ui(self) -> None:
        font = get_font(FontType.UI_BOLD, 16)
        ip_input = TextInput(
            "http://127.0.0.1:10008",
            pygame.Rect(0, 0, 300, 60),
            font,
            pygame.Color("black"),
            30,
            self.focus_controller,
        )
        self.focus_controller.add(ip_input)

        connect_button = Button(
            "접속",
            pygame.Rect(0, 0, 80, 60),
            font,
            lambda _: self.try_connect(ip_input.text),
        )

        room_input = TextInput(
            "방 이름",
            pygame.Rect(0, 0, 500, 60),
            font,
            pygame.Color("black"),
            60,
            self.focus_controller,
        )
        self.focus_controller.add(room_input)

        password_input = TextInput(
            "비밀번호",
            pygame.Rect(0, 0, 300, 60),
            font,
            pygame.Color("black"),
            15,
            self.focus_controller,
        )
        self.focus_controller.add(password_input)

        room_create_button = Button(
            "생성",
            pygame.Rect(0, 0, 80, 60),
            font,
            lambda _: self.create_room(room_input.text, password_input.text),
        )

        room_enter_button = Button(
            "입장",
            pygame.Rect(0, 0, 80, 60),
            font,
            lambda _: self.enter_room(room_input.text, password_input.text),
        )

        gap = 30
        self.add_child(
            Vertical(
                pygame.Vector2(50, 50),
                gap,
                [
                    Horizontal(pygame.Vector2(0, 0), gap, [ip_input, connect_button]),
                    Horizontal(
                        pygame.Vector2(0, 0),
                        gap,
                        [
                            room_input,
                            password_input,
                            room_create_button,
                            room_enter_button,
                        ],
                    ),
                ],
            )
        )

    def try_connect(self, server_ip: str) -> None:
        try:
            clientio.connect(server_ip, auth={"username": "Test Player"})
            rooms: list[LobbyRoom] = clientio.call("room_list")
            logger.info(rooms)

        except socketio.client.exceptions.ConnectionError as e:
            logger.error(f"방 접속 실패 {e}")

    def create_room(self, room_name: str, password: str) -> None:
        success = clientio.call(
            "create_room",
            CreateRoom(room_name, password).to_dict(),
        )
        logger.info(success)
        rooms: list[LobbyRoom] = clientio.call("room_list")
        logger.info(rooms)

    def enter_room(self, room_id: str, password: str) -> None:
        success = clientio.call("join_room", JoinRoom(room_id, password).to_dict())
        logger.info(success)
