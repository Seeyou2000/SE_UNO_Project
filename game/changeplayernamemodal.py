import pygame

from engine.button import Button
from engine.layout import Horizontal, LayoutAnchor, LayoutConstraint, Vertical
from engine.modal import Modal
from engine.scene import Scene
from engine.text import Text
from engine.textinput import TextInput
from game.constant import NAME
from game.font import FontType, get_font
from network.client.client import clientio
from network.common.messages.common import ChangePlayerName, CommonMessageType


class ChangePlayerNameModal(Modal):
    def __init__(self, scene: Scene) -> None:
        super().__init__([700, 350], scene)
        self.scene = scene
        self.font = get_font(FontType.UI_BOLD, 20)
        self.current_name = NAME[0]
        self.name_prefix = "현재 플레이어 이름 : "
        self.new_name = ""
        
        self.text_name = Text(
            self.name_prefix + self.current_name,
            pygame.Vector2(0, 0),
            self.font,
            pygame.Color("gray"),
        )
        
        self.input_name = TextInput(
            self.new_name,
            pygame.Rect(0, 0, 500, 60),
            self.font,
            pygame.Color("black"),
            60,
            self.scene.focus_controller,
        )
        self.focus_controller.add(self.input_name)
        
        self.accept_button = Button(
            "확인",
            pygame.Rect(0, 0, 150, 80),
            self.font,
            lambda _: self.change_player_name(),
        )
        
        self.back_button = Button(
            "뒤로 가기",
            pygame.Rect(0, 0, 150, 80),
            self.font,
            lambda _: self.close()
        )
        
        self.add_child(
            Vertical(
                pygame.Vector2(50, 50), 
                50, 
                [Vertical(pygame.Vector2(0, 0), 
                          50, 
                          [self.text_name, self.input_name,]), 
                 Horizontal(pygame.Vector2(0, 0), 
                          50, 
                          [self.back_button, self.accept_button])]))
   
        
    def change_player_name(self) -> None:
        clientio.call(
            CommonMessageType.CHANGE_PLAYER_NAME.value, 
            ChangePlayerName(self.input_name.text).to_dict(),
        )
        self.text_name.set_text(self.name_prefix + self.input_name.text)