import pygame

from engine.button import Button
from engine.scene import Scene
from engine.sprite import Sprite
from engine.text import Text
from engine.world import World
from game.font import FontType, get_font


class ArchievementScene(Scene):
    def __init__(self, world: World) -> None:
        super().__init__(world)
        self.font = get_font(FontType.UI_BOLD, 20)

        from game.menu.menuscene import MenuScene

        is_cleared = []  # 업적 정보 받아서 bool로 클리어 유무 저장
        for i in range(0, 6):
            is_cleared.append(False)
        for i in range(6, 12):
            is_cleared.append(True)

        menu_button = Button(
            "Back to menu",
            pygame.Rect(10, 10, 180, 60),
            self.font,
            lambda _: self.world.director.change_scene(MenuScene(self.world)),
        )
        self.add_child(menu_button)

        archieve_icon1_list = [
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
        ]
        archieve_icon2_list = [
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
            Sprite(pygame.image.load("resources/unoarchieve_temp.jpg")),
        ]
        archieve_text1_list = [
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
        archieve_text2_list = [
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
        clear_list = []
        clear_count = 0
        # for 문 내에 is_cleared 변수로 if문 돌려서 is_cleared = true 시 cleared 에셋 출력
        # cleared 에셋은 배경 없는 png로 할 것, 사이즈는 100x100 px / png로 덮어쓰기 시 뒤에 아이콘 에셋 살아있는거 확인했음
        for i, item in enumerate(archieve_icon1_list):
            self.layout.add(
                item, pygame.Vector2(0.5, 0.5), pygame.Vector2(-550, (i - 2) * 103 + 20)
            )
            if is_cleared[i] == True:
                clear_list.append(Sprite(pygame.image.load("resources/unocleared.png")))
                self.layout.add(
                    clear_list[clear_count],
                    pygame.Vector2(0.5, 0.5),
                    pygame.Vector2(-550, (i - 2) * 103 + 20),
                )
                clear_count += 1

        for i, item in enumerate(archieve_text1_list):
            self.layout.add(
                item, pygame.Vector2(0.5, 0.5), pygame.Vector2(-250, (i - 2) * 103 + 20)
            )
        for i, item in enumerate(archieve_icon2_list):
            self.layout.add(
                item, pygame.Vector2(0.5, 0.5), pygame.Vector2(100, (i - 2) * 103 + 20)
            )
            if is_cleared[i + len(archieve_icon1_list)] == True:
                clear_list.append(Sprite(pygame.image.load("resources/unocleared.png")))
                self.layout.add(
                    clear_list[clear_count],
                    pygame.Vector2(0.5, 0.5),
                    pygame.Vector2(100, (i - 2) * 103 + 20),
                )
                clear_count += 1
        for i, item in enumerate(archieve_text2_list):
            self.layout.add(
                item, pygame.Vector2(0.5, 0.5), pygame.Vector2(400, (i - 2) * 103 + 20)
            )
        self.add_children(archieve_icon1_list + archieve_text1_list)
        self.add_children(archieve_icon2_list + archieve_text2_list)
        self.add_children(clear_list)
