import sys
import pygame
from engine.button import Button
from engine.scene import Scene
from engine.sprite import Sprite
from engine.world import World
from game.scene.ingame import InGameScene
from game.scene.ingame2 import InGameScene2


class MenuScene(Scene):
    def __init__(self, world: World):
        super().__init__(world)

        font = pygame.font.SysFont('나눔스퀘어', 20)
        button_rect = pygame.Rect(0, 0, 200, 80)

        sprite = Sprite(pygame.image.load('resources/uno.jpg'))
        sprite.rect.move_ip(200, 200)

        self.children.extend([
            Button('Start', button_rect.move(20, 20), font, on_click=lambda event: self.world.director.change_scene(InGameScene)),
            Button('Settings', button_rect.move(20, 110), font),
            Button('Exit', button_rect.move(20, 200), font, on_click=lambda event: sys.exit()),
            Button('Start', button_rect.move(250, 20), font, on_click=lambda event: self.world.director.change_scene(InGameScene2)),
            sprite
        ])