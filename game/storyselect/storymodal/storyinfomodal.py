import pygame

from engine.button import Button
from engine.events.event import Event
from engine.layout import Horizontal, Layout, LayoutAnchor, Vertical
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
        self.font = get_font(FontType.UI_BOLD, 20)
        self.layout = Layout(self.rect)
        self.display_text_list = []

        self.area_text = Text(
            self.text_list[0],
            pygame.Vector2(0, 0),
            get_font(FontType.UI_BOLD, 40),
            pygame.Color("black"),
        )
        self.layout.add(self.area_text, LayoutAnchor.TOP_LEFT, pygame.Vector2(50, 50))
        self.add_child(self.area_text)

        for text in self.text_list[1:]:
            self.display_text = Text(
                text.strip(),
                pygame.Vector2(0, 0),
                self.font,
                pygame.Color("black"),
            )
            self.display_text_list.append(self.display_text)

        gap = 30
        self.add_child(
            Vertical(
                pygame.Vector2(50, 130),
                gap,
                self.display_text_list,
            )
        )

        self.enter_button = Button(
            "입장하기",
            pygame.Rect(0, 0, 150, 60),
            self.font,
            self.handle_story_select,
        )
        self.focus_controller.add(self.enter_button)

        self.back_button = Button(
            "돌아가기", pygame.Rect(0, 0, 150, 60), self.font, lambda _: self.close()
        )
        self.focus_controller.add(self.back_button)

        buttons = Horizontal(
            pygame.Vector2(0, 400),
            50,
            [self.back_button, self.enter_button],
        )

        self.layout.add(buttons, LayoutAnchor.BOTTOM_CENTER, pygame.Vector2(0, -50))
        self.add_child(buttons)
        self.layout.update(0)

    def handle_story_select(self, event: Event) -> None:
        from game.ingame.ingamescene import InGameScene

        if self.area == 1:
            self.scene.world.director.change_scene(
                InGameScene(self.scene.world, 2, True, area_number=1)
            )
        elif self.area == 2:
            self.scene.world.director.change_scene(
                InGameScene(self.scene.world, 4, False, True, area_number=2)
            )
        elif self.area == 3:
            self.scene.world.director.change_scene(
                InGameScene(self.scene.world, 3, False, False, True, area_number=3)
            )
        elif self.area == 4:
            self.scene.world.director.change_scene(
                InGameScene(
                    self.scene.world, 5, False, False, False, True, area_number=4
                )
            )
