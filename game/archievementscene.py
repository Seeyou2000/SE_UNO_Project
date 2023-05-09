import pygame

from engine.button import Button
from engine.scene import Scene
from engine.sprite import Sprite
from engine.text import Text
from engine.textinput import TextInput
from engine.world import World
from game.font import FontType, get_font


class ArchievementScene(Scene):
    def __init__(self, world: World) -> None:
        super().__init__(world)
        self.font = get_font(FontType.UI_BOLD, 20)

        from game.menu.menuscene import MenuScene

        menu_button = Button(
            "Back to menu",
            pygame.Rect(10, 10, 180, 60),
            self.font,
            lambda _: self.world.director.change_scene(MenuScene(self.world)),
        )
        self.add_child(menu_button)

        archieve_list = [
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
        ]

        for i, item in enumerate(archieve_list):
            self.layout.add(
                item, pygame.Vector2(0.5, 0.5), pygame.Vector2(-400, (i - 2) * 115 + 20)
            )

        self.add_children(archieve_list)
