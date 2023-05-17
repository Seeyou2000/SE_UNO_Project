from collections.abc import Callable

import pygame

from engine.button import Button
from engine.layout import Horizontal, Vertical
from engine.modal import Modal
from engine.scene import Scene
from engine.text import Text
from engine.textinput import TextInput
from game.font import FontType, get_font


class ValidatePasswordModal(Modal):
    def __init__(self, scene: Scene, enter_room: Callable[[str], None]) -> None:
        super().__init__([700, 350], scene)
        self.font = get_font(FontType.UI_BOLD, 20)
        self.enter_room = enter_room
        self.validate_password_modal_ui()

    def validate_password_modal_ui(self) -> None:
        self.verify_password = Text(
            "비밀번호 입력",
            pygame.Vector2(0, 0),
            get_font(FontType.UI_BOLD, 20),
            pygame.Color("gray"),
        )
        self.verify_password_text = TextInput(
            "",
            pygame.Rect(0, 0, 500, 60),
            self.font,
            pygame.Color("black"),
            15,
            self.focus_controller,
        )
        self.focus_controller.add(self.verify_password_text)

        self.join_room_button = Button(
            "입장",
            pygame.Rect(0, 0, 80, 60),
            self.font,
            lambda _: self.enter_room(self.verify_password_text.text),
        )
        self.focus_controller.add(self.join_room_button)

        self.back_multi_lobby_scene = Button(
            "돌아가기",
            pygame.Rect(0, 0, 80, 60),
            self.font,
            lambda _: self.close(),
        )
        self.focus_controller.add(self.back_multi_lobby_scene)

        self.add_child(
            Vertical(
                pygame.Vector2(50, 100),
                20,
                [
                    Horizontal(
                        pygame.Vector2(0, 0),
                        20,
                        [
                            self.verify_password,
                            self.verify_password_text,
                        ],
                    ),
                    Horizontal(
                        pygame.Vector2(400, 0),
                        30,
                        [
                            self.join_room_button,
                            self.back_multi_lobby_scene,
                        ],
                    ),
                ],
            ),
        )
