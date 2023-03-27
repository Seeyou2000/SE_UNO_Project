import sys

import pygame

from engine.button import Button
from engine.scene import Scene
from engine.world import World
from game.scene.select import SelectScene


class MenuScene(Scene):
    def __init__(self, world: World) -> None:
        super().__init__(world)

        font = pygame.font.SysFont("나눔스퀘어", 20)
        button_rect = pygame.Rect(0, 0, 200, 80)

        from game.scene.settings import SettingScene

        self.add_children(
            [
                Button(
                    "Start",
                    button_rect.move(20, 20),
                    font,
                    on_click=lambda event: self.world.director.change_scene(
                        SelectScene(self.world)
                    ),
                ),
                Button(
                    "Settings",
                    button_rect.move(20, 110),
                    font,
                    on_click=lambda event: self.world.director.change_scene(
                        SettingScene(self.world)
                    ),
                ),
                Button(
                    "Exit",
                    button_rect.move(20, 200),
                    font,
                    on_click=lambda event: sys.exit(),
                ),
            ]
        )
