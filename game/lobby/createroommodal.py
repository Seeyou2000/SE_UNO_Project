import pygame
from loguru import logger

from engine.button import Button
from engine.checkbox import Checkbox
from engine.events.event import Event
from engine.layout import Horizontal
from engine.modal import Modal
from engine.scene import Scene
from engine.text import Text
from engine.textinput import TextInput
from game.font import FontType, get_font
from game.messagemodal import MessageModal
from network.common.messages.lobby import CreateRoom, LobbyMessageType
from network.common.models import LobbyRoom


class CreateRoomModal(Modal):
    def __init__(self, scene: Scene) -> None:
        super().__init__([700, 350], scene)
        self.font = get_font(FontType.UI_BOLD, 20)
        self.create_room_modal_ui()

    def create_room_modal_ui(self) -> None:
        room_text = Text(
            "방 이름",
            pygame.Vector2(0, 20),
            get_font(FontType.UI_BOLD, 20),
            pygame.Color("gray"),
        )

        room_input = TextInput(
            "",
            pygame.Rect(0, 0, 500, 60),
            self.font,
            pygame.Color("black"),
            60,
            self.focus_controller,
        )
        self.focus_controller.add(room_input)

        self.add_child(
            Horizontal(
                pygame.Vector2(50, 50),
                20,
                [room_text, room_input],
            )
        )

        password_text = Text(
            "비밀번호 유무",
            pygame.Vector2(0, 20),
            get_font(FontType.UI_BOLD, 20),
            pygame.Color("gray"),
        )

        self.password_check_box = Checkbox(
            pygame.Rect(0, 15, 30, 30),
            self.font,
        )

        self.password_check_box.on("click", self.toggle_password_input)

        self.password_input = TextInput(
            "",
            pygame.Rect(250, 150, 400, 60),
            self.font,
            pygame.Color("black"),
            15,
            self.focus_controller,
        )
        self.focus_controller.add(self.password_input)

        self.add_child(
            Horizontal(
                pygame.Vector2(50, 150),
                20,
                [
                    password_text,
                    self.password_check_box,
                ],
            )
        )

        create_room_button = Button(
            "생성",
            pygame.Rect(50, 250, 80, 60),
            self.font,
            lambda _: self.create_room(room_input.text, self.password_input.text),
        )
        self.focus_controller.add(create_room_button)
        self.add_child(create_room_button)

        back_multi_lobby_scene = Button(
            "돌아가기",
            pygame.Rect(150, 250, 80, 60),
            self.font,
            lambda _: self.close(),
        )
        self.focus_controller.add(back_multi_lobby_scene)
        self.add_child(back_multi_lobby_scene)

    def toggle_password_input(self, event: Event) -> None:
        if self.password_check_box.is_checked:
            if not self.has_child(self.password_input):
                self.add_child(self.password_input)
        else:
            if self.has_child(self.password_input):
                self.remove_child(self.password_input)

    def create_room(self, room_name: str, password: str) -> None:
        if len(password.strip()) == 0:
            password = None

        if len(room_name.strip()) == 0:
            self.show_create_room_fail_modal()

        self.scene.io.call(
            LobbyMessageType.CREATE_ROOM.value,
            CreateRoom(room_name, password).to_dict(),
        )

    def show_create_room_fail_modal(self) -> None:
        self.create_room_fail_modal = MessageModal(self.scene, "방 이름을 입력해주세요.")
        self.scene.open_modal(self.create_room_fail_modal)
