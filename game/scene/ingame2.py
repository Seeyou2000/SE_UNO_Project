from __future__ import annotations
import sys
import pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.scene.menu import MenuScene
from engine.scene import Scene
from engine.sprite import Sprite
from engine.world import World
from engine.button import Button

class InGameScene2(Scene):
   def __init__(self, world: World):
        super().__init__(world)

        font = pygame.font.SysFont('나눔스퀘어', 20)
        button_rect = pygame.Rect(0, 0, 200, 80)

        self.children.extend([
            Button('Exit2', button_rect.move(80, 110), font, on_click = lambda event : sys.exit()),
            Button('Firstscene', button_rect.move(80, 200), font, on_click=lambda event:self.world.director.change_scene(MenuScene)),
            #MenuScene으로 전환할때 circular import 오류 확인, TYPE_CHECKING 기법을 사용했을 때 NameError 오류.
            Button('Nothing', button_rect.move(80, 20), font),
        ])
  