import pygame

from engine.button import Button
from engine.layout import Horizontal, Vertical
from engine.modal import Modal
from engine.scene import Scene
from engine.text import Text
from game.font import FontType, get_font


class StoryInfoModal(Modal):
    def __init__(self, scene: Scene, text_list: list[str], area: int) -> None:
        super().__init__([800, 500], scene)
        self.scene = scene
        self.text_list = text_list
        self.area = area
        self.display_text_list = []
        self.font = get_font(FontType.UI_BOLD, 20)

        for text in self.text_list:
            self.display_text = Text(
                text,
                pygame.Vector2(0, 0),
                self.font,
                pygame.Color("black"),
            )
            self.display_text_list.append(self.display_text)

        gap = 20
        self.add_child(
            Vertical(
                pygame.Vector2(30, 30),
                gap,
                self.display_text_list,
            )
        )

        self.find_story_mode_and_back_button()

    def find_story_mode_and_back_button(self) -> None:
        from game.ingame.ingamescene import InGameScene

        if self.area == 1:
            self.enter_button = Button(
                "입장하기",
                pygame.Rect(0, 0, 80, 60),
                self.font,
                lambda _: self.scene.world.director.change_scene(
                    InGameScene(self.scene.world, 2, True)
                ),
            )
        elif self.area == 2:
            self.enter_button = Button(
                "입장하기",
                pygame.Rect(0, 0, 80, 60),
                self.font,
                lambda _: self.scene.world.director.change_scene(
                    InGameScene(self.scene.world, 4, False, True)
                ),
            )
        elif self.area == 3:
            self.enter_button = Button(
                "입장하기",
                pygame.Rect(0, 0, 80, 60),
                self.font,
                lambda _: self.scene.world.director.change_scene(
                    InGameScene(self.scene.world, 3, False, False, True)
                ),
            )
        elif self.area == 4:
            self.enter_button = Button(
                "입장하기",
                pygame.Rect(0, 0, 80, 60),
                self.font,
                lambda _: self.scene.world.director.change_scene(
                    InGameScene(self.scene.world, 5, False, False, False, True)
                ),
            )
        self.focus_controller.add(self.enter_button)

        self.back_button = Button(
            "돌아가기", pygame.Rect(0, 0, 80, 60), self.font, lambda _: self.close()
        )
        self.focus_controller.add(self.back_button)

        gap = 300
        self.add_child(
            Horizontal(
                pygame.Vector2(190, 400),
                gap,
                [self.enter_button, self.back_button],
            )
        )
