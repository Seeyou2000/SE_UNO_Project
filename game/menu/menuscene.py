import sys

import pygame

from engine.scene import Scene
from engine.sprite import Sprite
from engine.world import World
from game.archievementscene import ArchievementScene
from game.lobby.lobbyscene import LobbyScene
from game.menu.menubutton import MenuButton
from game.storyselect.storymodeselectscene import StoryModeSelectScene


class MenuScene(Scene):
    def __init__(self, world: World) -> None:
        super().__init__(world)
        from game.settings.settingscene import SettingScene

        button_size = pygame.Vector2(200, 80)

        sprite = Sprite(pygame.image.load("resources/uno.jpg"))

        button_list = [
            MenuButton(
                "Start",
                button_size,
                lambda _: world.director.change_scene(LobbyScene(world)),
            ),
            MenuButton(
                "Story Mode",
                button_size,
                lambda _: world.director.change_scene(StoryModeSelectScene(world)),
            ),
            MenuButton(
                "Archievements",
                button_size,
                lambda _: world.director.change_scene(ArchievementScene(world)),
            ),
            MenuButton(
                "Settings",
                button_size,
                lambda _: world.director.change_scene(SettingScene(world)),
            ),
            MenuButton(
                "Exit",
                button_size,
                lambda _: sys.exit(),
            ),
        ]

        self.layout.add(sprite, pygame.Vector2(0.5, 0.5), pygame.Vector2(0, -130))

        for i, item in enumerate(button_list):
            self.layout.add(
                item, pygame.Vector2(0.5, 0.5), pygame.Vector2(0, 70 * i + 80)
            )
            self.focus_controller.add(item)

        self.add_children([sprite] + button_list)
