import pygame

from engine.button import Button
from engine.layout import Vertical
from engine.modal import Modal
from engine.scene import Scene
from engine.text import Text
from game.font import FontType, get_font


class MessageModal(Modal):
    def __init__(self, scene: Scene, text: str) -> None:
        super().__init__([300, 300], scene)
        self.text = text
        self.font = get_font(FontType.UI_BOLD, 20)
        self.display_ui()

    def display_ui(self) -> None:
        self.display_text = Text(
            self.text,
            pygame.Vector2(0, 0),
            get_font(FontType.UI_BOLD, 20),
            pygame.Color("gray"),
        )
        self.back_button = Button(
            "돌아가기",
            pygame.Rect(0, 0, 200, 60),
            self.font,
            lambda _: self.close(),
        )
        self.focus_controller.add(self.back_button)

        self.add_child(
            Vertical(
                pygame.Vector2(50, 100),
                20,
                [self.display_text, self.back_button],
            )
        )
