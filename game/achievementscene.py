import json

import pygame

from engine.button import Button
from engine.scene import Scene
from engine.sprite import Sprite
from engine.text import Text
from engine.world import World
from game.font import FontType, get_font


class AchievementScene(Scene):
    def __init__(self, world: World) -> None:
        super().__init__(world)

        self.font = get_font(FontType.UI_BOLD, 20)

        from game.menu.menuscene import MenuScene

        self.is_cleared = []  # 업적 정보 받아서 bool로 클리어 유무 저장
        print(self.world.achievements.win_less_10turn)
        win_less_10turn = self.world.achievements.win_less_10turn
        if win_less_10turn[0] == True:
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

        self.achieve_icon1_list = [
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
        ]
        self.achieve_icon2_list = [
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
        ]
        self.achieve_text1_list = [
            Text(
                "싱글 플레이어에서 승리",
                pygame.Vector2(50, 300),
                get_font(FontType.UI_BOLD, 20),
                pygame.Color("black"),
            ),
            Text(
                "10턴 내에 승리",
                pygame.Vector2(50, 300),
                get_font(FontType.UI_BOLD, 20),
                pygame.Color("black"),
            ),
            Text(
                "기술 카드 사용하지 않고 승리",
                pygame.Vector2(50, 300),
                get_font(FontType.UI_BOLD, 20),
                pygame.Color("black"),
            ),
            Text(
                "다른 플레이어가 UNO를 선언한 뒤 승리",
                pygame.Vector2(50, 300),
                get_font(FontType.UI_BOLD, 20),
                pygame.Color("black"),
            ),
            Text(
                "???",
                pygame.Vector2(50, 300),
                get_font(FontType.UI_BOLD, 20),
                pygame.Color("black"),
            ),
            Text(
                "???",
                pygame.Vector2(50, 300),
                get_font(FontType.UI_BOLD, 20),
                pygame.Color("black"),
            ),
        ]
        self.achieve_text2_list = [
            Text(
                "???",
                pygame.Vector2(50, 300),
                get_font(FontType.UI_BOLD, 20),
                pygame.Color("black"),
            ),
            Text(
                "스테이지 1 클리어",
                pygame.Vector2(50, 300),
                get_font(FontType.UI_BOLD, 20),
                pygame.Color("black"),
            ),
            Text(
                "스테이지 2 클리어",
                pygame.Vector2(50, 300),
                get_font(FontType.UI_BOLD, 20),
                pygame.Color("black"),
            ),
            Text(
                "스테이지 3 클리어",
                pygame.Vector2(50, 300),
                get_font(FontType.UI_BOLD, 20),
                pygame.Color("black"),
            ),
            Text(
                "스테이지 4 클리어",
                pygame.Vector2(50, 300),
                get_font(FontType.UI_BOLD, 20),
                pygame.Color("black"),
            ),
        ]
        self.clear_list = []
        self.clear_count = 0
        # for 문 내에 is_cleared 변수로 if문 돌려서 is_cleared = true 시 cleared 에셋 출력
        # cleared 에셋은 배경 없는 png로 할 것, 사이즈는 100x100 px / png로 덮어쓰기 시 뒤에 아이콘 에셋 살아있는거 확인했음
        self.place_achieve1()
        self.place_achieve2()

        self.add_children(self.achieve_icon1_list + self.achieve_text1_list)
        self.add_children(self.achieve_icon2_list + self.achieve_text2_list)
        self.add_children(self.clear_list)

    def place_achieve1(self) -> None:
        for i, item in enumerate(self.achieve_icon1_list):
            self.layout.add(
                item, pygame.Vector2(0.5, 0.5), pygame.Vector2(-550, (i - 2) * 103 + 20)
            )
            if self.is_cleared[i] == True:
                self.clear_list.append(
                    Sprite(pygame.image.load("resources/unocleared.png"))
                )
                self.layout.add(
                    self.clear_list[self.clear_count],
                    pygame.Vector2(0.5, 0.5),
                    pygame.Vector2(-550, (i - 2) * 103 + 20),
                )
                self.clear_count += 1

        for i, item in enumerate(self.achieve_text1_list):
            self.layout.add(
                item, pygame.Vector2(0.5, 0.5), pygame.Vector2(-250, (i - 2) * 103 + 20)
            )

    def place_achieve2(self) -> None:
        for i, item in enumerate(self.achieve_icon2_list):
            self.layout.add(
                item, pygame.Vector2(0.5, 0.5), pygame.Vector2(100, (i - 2) * 103 + 20)
            )
            if self.is_cleared[i + len(self.achieve_icon1_list)] == True:
                self.clear_list.append(
                    Sprite(pygame.image.load("resources/unocleared.png"))
                )
                self.layout.add(
                    self.clear_list[self.clear_count],
                    pygame.Vector2(0.5, 0.5),
                    pygame.Vector2(100, (i - 2) * 103 + 20),
                )
                self.clear_count += 1
        for i, item in enumerate(self.achieve_text2_list):
            self.layout.add(
                item, pygame.Vector2(0.5, 0.5), pygame.Vector2(400, (i - 2) * 103 + 20)
            )
