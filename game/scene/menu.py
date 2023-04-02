import sys

import pygame

from engine.button import Button
from engine.layout import Layout
from engine.scene import Scene
from engine.sprite import Sprite
from engine.world import World


class MenuScene(Scene):
    def __init__(self, world: World) -> None:
        super().__init__(world)

        from game.scene.ingame import InGameScene
        from game.settings.settingscene import SettingScene

        font = pygame.font.SysFont("나눔스퀘어", 20)
        button_rect = pygame.Rect(0, 0, 200, 80)

        sprite = Sprite(
            pygame.transform.scale(pygame.image.load("resources/uno.jpg"), [500, 600])
        )
        button_list = [
            Button(
                "Start",
                button_rect.copy(),
                font,
                lambda _: world.director.change_scene(InGameScene(world)),
            ),
            Button(
                "Settings",
                button_rect.copy(),
                font,
                lambda _: world.director.change_scene(SettingScene(world)),
            ),
            Button(
                "Exit",
                button_rect.copy(),
                font,
                on_click=lambda _: sys.exit(),
            ),
        ]

        self.layout = Layout(world.get_rect())
        self.on("resize", lambda _: self.layout.rect.update(self.world.get_rect()))

        self.layout.add(sprite, pygame.Vector2(0.5, 0.5), pygame.Vector2(0, -130))

        for i, item in enumerate(button_list):
            self.layout.add(item, pygame.Vector2(0.5, 0.5), pygame.Vector2(0, 90 * i))
        self.layout.update()

        self.add_children([sprite] + button_list)

    def update(self) -> None:
        super().update()
        self.layout.update()
