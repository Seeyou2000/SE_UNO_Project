import pygame

from engine.button import Button
from engine.focus import FocusMoveDirection
from engine.layout import LayoutAnchor
from engine.scene import Scene
from engine.world import World
from game.font import FontType, get_font


class LobbyScene(Scene):
    def __init__(self, world: World) -> None:
        super().__init__(world)

        font = get_font(FontType.UI_BOLD, 20)

        player_count_buttons = []
        for i in range(2, 7):
            button = Button(
                str(i),
                pygame.Rect(0, 0, 50, 50),
                font,
                lambda _, num=i: self.start_with_player_count(num),
            )
            self.layout.add(
                button, LayoutAnchor.CENTER, pygame.Vector2((i - 4) * 500 / 5, 0)
            )
            self.focus_controller.add(button)
            button.on("focus", lambda _, button=button: print(button))
            self.add_child(button)
            player_count_buttons.append(button)

        from game.menu.menuscene import MenuScene

        menu_button = Button(
            "Back to menu",
            pygame.Rect(0, 0, 180, 60),
            font,
            lambda _: self.world.director.change_scene(MenuScene(self.world)),
        )
        self.layout.add(
            menu_button, LayoutAnchor.BOTTOM_RIGHT, pygame.Vector2(-50, -50)
        )
        self.add_child(menu_button)

        self.focus_controller.set_siblings(
            player_count_buttons[-1], {FocusMoveDirection.RIGHT: menu_button}
        )
        self.focus_controller.set_siblings(
            menu_button, {FocusMoveDirection.LEFT: player_count_buttons[-1]}
        )

    def update(self, dt: float) -> None:
        super().update(dt)

    def start_with_player_count(self, count: int) -> None:
        from game.ingame.ingamescene import InGameScene

        self.world.director.change_scene(InGameScene(self.world, count))
