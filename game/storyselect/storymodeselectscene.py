import pygame

from engine.button import Button
from engine.layout import LayoutAnchor, LayoutConstraint
from engine.scene import Scene
from engine.world import World
from game.font import FontType, get_font
from game.ingame.ingamescene import InGameScene
from game.storyselect.storymodal.storyinfomodal import StoryInfoModal


class StoryModeSelectScene(Scene):
    def __init__(self, world: World) -> None:
        super().__init__(world)

        story_button_size = pygame.Rect(0, 0, 300, 100)
        self.font = get_font(FontType.UI_BOLD, 20)

        self.area_one_text = """
        Area 1
        1명의 컴퓨터 플레이어와 대전.
        첫 분배시 컴퓨터 플레이어가 기술 카드를 50% 더 높은 확률로 받게 됨.
        컴퓨터 플레이어가 거꾸로 진행과 건너 뛰기 등의 기술카드를 적절히 조합하여 
        2~3장 이상의 카드를 한 번에 낼 수 있는 콤보를 사용.
        """
        self.area_two_text = """
        Area 2
        3명의 컴퓨터 플레이어와 대전.
        첫 카드를 제외하고 모든 카드를 같은 수만큼 플레이어들에게 분배.
        """
        self.area_three_text = """
        Area 3
        2명의 컴퓨터 플레이어와 대전.
        매 5턴마다 낼 수 있는 카드의 색상이 무작위로 변경됨.
        """
        self.area_four_text = """
        Area 4
        4명의 컴퓨터 플레이어와 대전.
        매 5턴마다 턴이 역으로 바뀜.
        """
        self.area_one_text_list = self.area_one_text.splitlines()
        self.area_two_text_list = self.area_two_text.splitlines()
        self.area_three_text_list = self.area_three_text.splitlines()
        self.area_four_text_list = self.area_four_text.splitlines()

        story_button_list = [
            Button(
                "Area 1",
                story_button_size.copy(),
                self.font,
                lambda _: self.show_story_info_modal(self.area_one_text_list, 1),
            ),
            Button(
                "Area 2",
                story_button_size.copy(),
                self.font,
                lambda _: self.show_story_info_modal(self.area_two_text_list, 2),
            ),
            Button(
                "Area 3",
                story_button_size.copy(),
                self.font,
                lambda _: self.show_story_info_modal(self.area_three_text_list, 3),
            ),
            Button(
                "Area 4",
                story_button_size.copy(),
                self.font,
                lambda _: self.show_story_info_modal(self.area_four_text_list, 4),
            ),
        ]

        for i, item in enumerate(story_button_list):
            self.layout.add(item, LayoutAnchor.CENTER, pygame.Vector2(0, 120 * i - 120))
            self.focus_controller.add(item)

        self.add_children(story_button_list)

        from game.menu.menuscene import MenuScene

        back_button = Button(
            "뒤로가기",
            pygame.Rect(0, 0, 80, 60),
            self.font,
            lambda _: world.director.change_scene(MenuScene(self.world)),
        )
        self.add(
            back_button, LayoutConstraint(LayoutAnchor.TOP_LEFT, pygame.Vector2(50, 50))
        )

    def show_story_info_modal(self, text: str, area: int) -> None:
        self.story_info_modal = StoryInfoModal(self, text, area)
        self.open_modal(self.story_info_modal)
