import pygame

from engine.button import Button
from engine.layout import LayoutAnchor
from engine.scene import Scene
from engine.world import World
from game.font import FontType, get_font
from game.ingame.ingamescene import InGameScene


class StoryModeSelectScene(Scene):
    def __init__(self, world: World) -> None:
        super().__init__(world)

        story_button_size = pygame.Rect(0, 0, 300, 100)
        self.font = get_font(FontType.UI_BOLD, 20)

        story_button_list = [
            Button(
                "Area 1",
                story_button_size.copy(),
                self.font,
                lambda _: world.director.change_scene(InGameScene(self.world, 2, True)),
            ),
            Button(
                "Area 2",
                story_button_size.copy(),
                self.font,
                lambda _: world.director.change_scene(
                    InGameScene(self.world, 4, False, True)
                ),
            ),
            Button(
                "Area 3",
                story_button_size.copy(),
                self.font,
                lambda _: world.director.change_scene(
                    InGameScene(self.world, 3, False, False, True)
                ),
            ),
            Button(
                "Area 4",
                story_button_size.copy(),
                self.font,
                lambda _: world.director.change_scene(
                    InGameScene(self.world, 6, False, False, False, True)
                ),
            ),
        ]

        for i, item in enumerate(story_button_list):
            self.layout.add(item, LayoutAnchor.CENTER, pygame.Vector2(0, 120 * i - 120))
            self.focus_controller.add(item)

        self.add_children(story_button_list)
