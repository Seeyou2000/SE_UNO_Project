import pygame

from engine.button import Button
from engine.scene import Scene
from engine.world import World
from game.scene.menu import MenuScene


class SettingScene(Scene):
    def __init__(self, world: World) -> None:
        super().__init__(world)

        font = pygame.font.SysFont("나눔스퀘어", 20)
        button_rect = pygame.Rect(0, 0, 60, 60)

        self.add_children(
            [
                Button(
                    "Small",
                    button_rect.move(20, 20),
                    font,
                    on_click=lambda event: self.world.set_size((400, 300)),
                ),
                Button(
                    "Medium",
                    button_rect.move(20, 90),
                    font,
                    on_click=lambda event: self.world.set_size((800, 600)),
                ),
                Button(
                    "Large",
                    button_rect.move(20, 160),
                    font,
                    on_click=lambda event: self.world.set_size((1600, 1200)),
                ),
                Button(
                    "Main Menu",
                    button_rect.move(20, 230),
                    font,
                    on_click=lambda event: self.world.director.change_scene(
                        MenuScene(self.world)
                    ),
                ),
            ]
        )
