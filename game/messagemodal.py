import pygame

from engine.button import Button
from engine.layout import Vertical
from engine.modal import Modal
from engine.scene import Scene
from engine.text import Text
from game.font import FontType, get_font


class MessageModal(Modal):
    def __init__(self, scene: Scene, text: str) -> None:
        self.text = text
        self.font = get_font(FontType.UI_BOLD, 20)

        self.display_text = Text(
            self.text,
            pygame.Vector2(0, 0),
            get_font(FontType.UI_BOLD, 20),
            pygame.Color("black"),
        )

        super().__init__([self.display_text.rect.width + 100, 300], scene)

        self.display_text.rect.center = self.rect.center
        self.display_text.rect.centery -= 50
        self.add_child(self.display_text)

        self.back_button = Button(
            "돌아가기",
            pygame.Rect(0, 0, 200, 60),
            self.font,
            lambda _: self.close(),
        )
        self.back_button.rect.centerx = self.rect.centerx
        self.back_button.rect.bottom = self.rect.bottom - 40
        self.add_child(self.back_button)
        self.focus_controller.add(self.back_button)
