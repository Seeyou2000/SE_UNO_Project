import pygame

from engine.button import Button
from engine.layout import LayoutAnchor, LayoutConstraint, Vertical
from engine.scene import Scene
from engine.text import Text
from engine.world import World
from game.achievementscene import AchievementScene
from game.font import FontType, get_font
from game.settings.settingscene import SettingScene


class InGamePauseScene(Scene):
    def __init__(self, world: World, count: int, scene: Scene) -> None:
        super().__init__(world)
        self.scene = scene
        self.count = count
        self.font = get_font(FontType.UI_BOLD, 20)

        self.pause_text = Text(
            "일시정지",
            pygame.Vector2(0, 0),
            get_font(FontType.UI_BOLD, 60),
            pygame.Color("black"),
        )

        self.ingame_button = Button(
            "게임으로 돌아가기",
            pygame.Rect(0, 0, 250, 100),
            self.font,
            lambda _: self.world.director.change_scene(self.scene),
        )

        self.achievements_button = Button(
            "업적 화면",
            pygame.Rect(0, 0, 250, 100),
            self.font,
            lambda _: self.world.director.change_scene(AchievementScene(self.world)),
        )

        self.settings_button = Button(
            "설정 화면",
            pygame.Rect(0, 0, 250, 100),
            self.font,
            lambda _: self.world.director.change_scene(SettingScene(self.world)),
        )

        self.game_end_button = Button(
            "게임 종료",
            pygame.Rect(0, 0, 250, 100),
            self.font,
            lambda _: self.world.exit(),
        )

        self.add(
            self.pause_text,
            LayoutConstraint(LayoutAnchor.TOP_CENTER, pygame.Vector2(0, 50)),
        )

        self.add(
            Vertical(
                pygame.Vector2(),
                50,
                [
                    self.ingame_button,
                    self.achievements_button,
                    self.settings_button,
                    self.game_end_button,
                ],
            ),
            LayoutConstraint(LayoutAnchor.CENTER, pygame.Vector2(0, 50)),
        )
