import sys

import pygame

from engine.button import Button
from engine.scene import Scene
from engine.sprite import Sprite
from engine.world import World


class MenuScene(Scene):
    def __init__(self, world: World) -> None:
        super().__init__(world)

        font = pygame.font.SysFont("나눔스퀘어", 20)
        button_rect = pygame.Rect(0, 0, 200, 80)

        sprite = Sprite(
            pygame.transform.scale(pygame.image.load("resources/uno.jpg"), [500, 600])
        )

        self.add_children(
            [
                Button(
                    "Start",
                    button_rect.move(500, 20),
                    font,
                ),
                Button("Settings", button_rect.move(500, 110), font),
                Button(
                    "Exit",
                    button_rect.move(500, 200),
                    font,
                    on_click=lambda event: sys.exit(),
                ),
                sprite,
            ]
        )
