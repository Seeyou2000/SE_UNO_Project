import sys
import pygame
from engine.button import Button
from engine.scene import Scene
from engine.sprite import Sprite
from engine.world import World


class MenuScene(Scene):
    def __init__(self, world: World):
        super().__init__(world)

        font = pygame.font.SysFont('나눔스퀘어', 20)
        button_rect = pygame.Rect(0, 0, 200, 80)

        sprite = Sprite(pygame.image.load('resources/uno.jpg'))
        sprite.rect.move_ip(200, 200)

        from game.scene.ingame import InGameScene
        self.add_children([
            Button('Start', button_rect.move(20, 20), font, on_click=lambda event: self.world.director.change_scene(InGameScene(self.world))),
            Button('Settings', button_rect.move(20, 110), font),
            Button('Exit', button_rect.move(20, 200), font, on_click=lambda event: sys.exit()),
            sprite
        ])
