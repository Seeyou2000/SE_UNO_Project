import pygame

from engine.button import Button
from engine.scene import Scene
from engine.sprite import Sprite
from engine.text import Text
from engine.world import World
from game.achievements import ACHIEVEMENT_DATA
from game.font import FontType, get_font


class AchievementScene(Scene):
    def __init__(self, world: World) -> None:
        super().__init__(world)

        self.font = get_font(FontType.UI_BOLD, 20)
        self.achieve_font = get_font(FontType.UI_BOLD, 18)
        self.text_font = get_font(FontType.UI_NORMAL, 11)

        from game.menu.menuscene import MenuScene

        self.is_cleared = []  # 업적 정보 받아서 bool로 클리어 유무 저장
        win_less_10turn = self.world.achievements.win_less_10turn
        if win_less_10turn[0] is True:
            self.is_cleared.append(True)
        else:
            self.is_cleared.append(False)
        for i in range(1, 6):
            self.is_cleared.append(False)
        for i in range(6, 12):
            self.is_cleared.append(True)

        menu_button = Button(
            "Back to menu",
            pygame.Rect(10, 10, 180, 60),
            self.font,
            lambda _: self.world.director.change_scene(MenuScene(self.world)),
        )
        self.add_child(menu_button)

        self.achieve_text1_cleartime_list = [
            Text(
                win_less_10turn[1],
                pygame.Vector2(50, 300),
                self.text_font,
                pygame.Color("black"),
            ),
        ]
        self.clear_list = []
        self.clear_count = 0

        self.place_clear_time()
        self.add_children(self.achieve_text1_cleartime_list)
        self.place_achieve()
        self.add_children(self.clear_list)

    def place_achieve(self) -> None:
        for i, item in enumerate(ACHIEVEMENT_DATA):
            if i <= 5:
                icon = Sprite(ACHIEVEMENT_DATA[item].icon)
                self.layout.add(
                    icon,
                    pygame.Vector2(0.5, 0.5),
                    pygame.Vector2(-550, (i - 2) * 103 - 20),
                )
                title = Text(
                    ACHIEVEMENT_DATA[item].title,
                    pygame.Vector2(50, 300),
                    self.achieve_font,
                    pygame.Color("black"),
                )
                self.layout.add(
                    title,
                    pygame.Vector2(0.5, 0.5),
                    pygame.Vector2(-250, (i - 2) * 103 - 53),
                )
                detail = Text(
                    ACHIEVEMENT_DATA[item].description,
                    pygame.Vector2(50, 300),
                    self.text_font,
                    pygame.Color("black"),
                )
                self.layout.add(
                    detail,
                    pygame.Vector2(0.5, 0.5),
                    pygame.Vector2(-250, (i - 2) * 103 - 23),
                )
                self.add_child(icon)
                self.add_child(title)
                self.add_child(detail)
                if self.is_cleared[i] is True:
                    self.clear_list.append(
                        Sprite(pygame.image.load("resources/images/unocleared.png"))
                    )
                    self.layout.add(
                        self.clear_list[self.clear_count],
                        pygame.Vector2(0.5, 0.5),
                        pygame.Vector2(-550, (i - 2) * 103 - 20),
                    )
                    self.clear_count += 1
            else:
                icon = Sprite(ACHIEVEMENT_DATA[item].icon)
                self.layout.add(
                    icon,
                    pygame.Vector2(0.5, 0.5),
                    pygame.Vector2(100, (i - 8) * 103 + 20),
                )
                title = Text(
                    ACHIEVEMENT_DATA[item].title,
                    pygame.Vector2(50, 300),
                    self.achieve_font,
                    pygame.Color("black"),
                )
                self.layout.add(
                    title,
                    pygame.Vector2(0.5, 0.5),
                    pygame.Vector2(400, (i - 8) * 103 - 13),
                )
                detail = Text(
                    ACHIEVEMENT_DATA[item].description,
                    pygame.Vector2(50, 300),
                    self.text_font,
                    pygame.Color("black"),
                )
                self.layout.add(
                    detail,
                    pygame.Vector2(0.5, 0.5),
                    pygame.Vector2(400, (i - 8) * 103 + 17),
                )
                self.add_child(icon)
                self.add_child(title)
                self.add_child(detail)
                if self.is_cleared[i] is True:
                    self.clear_list.append(
                        Sprite(pygame.image.load("resources/images/unocleared.png"))
                    )
                    self.layout.add(
                        self.clear_list[self.clear_count],
                        pygame.Vector2(0.5, 0.5),
                        pygame.Vector2(100, (i - 8) * 103 + 20),
                    )
                    self.clear_count += 1

    def place_clear_time(self) -> None:
        for i, item in enumerate(self.achieve_text1_cleartime_list):
            self.layout.add(
                item, pygame.Vector2(0.5, 0.5), pygame.Vector2(-250, (i - 2) * 103 - 3)
            )
