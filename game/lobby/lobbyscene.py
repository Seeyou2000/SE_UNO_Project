import pygame

from engine.button import Button
from engine.event import Event
from engine.focus import FocusMoveDirection
from engine.layout import LayoutAnchor
from engine.scene import Scene
from engine.text import Text
from engine.textinput import TextInput
from engine.world import World
from game.constant import NAME
from game.font import FontType, get_font


class LobbyScene(Scene):
    def __init__(self, world: World) -> None:
        super().__init__(world)

        font = get_font(FontType.UI_BOLD, 20)

        name_text = Text(
            "PLAYER NAME",
            pygame.Vector2(50, 300),
            get_font(FontType.UI_BOLD, 16),
            pygame.Color("gray"),
        )
        self.add_child(name_text)
        self.name_input = TextInput(
            NAME[0],
            pygame.Rect(50, 340, 300, 80),
            get_font(FontType.UI_BOLD, 30),
            pygame.Color("black"),
            10,
        )
        self.add_child(self.name_input)

        self.names = []

        ai_player_buttons = []
        for i in range(1, 6):
            button = Button(
                "+",
                pygame.Rect(0, 0, 300, 100),
                font,
                self.create_toggle_ai_button(i),
            )
            self.layout.add(
                button,
                LayoutAnchor.MIDDLE_RIGHT,
                pygame.Vector2(-50, (i - 4) * 500 / 5),
            )
            self.focus_controller.add(button)
            button.on("focus", lambda _, button=button: print(button))
            self.add_child(button)
            ai_player_buttons.append(button)

        from game.menu.menuscene import MenuScene

        menu_button = Button(
            "Back to menu",
            pygame.Rect(0, 0, 180, 60),
            font,
            lambda _: self.world.director.change_scene(MenuScene(self.world)),
        )
        self.layout.add(
            menu_button, LayoutAnchor.BOTTOM_RIGHT, pygame.Vector2(-250, -50)
        )
        self.add_child(menu_button)

        start_button = Button(
            "Start",
            pygame.Rect(0, 0, 180, 60),
            font,
            self.start_with_player_count,
        )
        self.layout.add(
            start_button, LayoutAnchor.BOTTOM_RIGHT, pygame.Vector2(-50, -50)
        )
        self.add_child(start_button)

        self.focus_controller.set_siblings(
            ai_player_buttons[-1], {FocusMoveDirection.RIGHT: menu_button}
        )
        self.focus_controller.set_siblings(
            menu_button, {FocusMoveDirection.LEFT: ai_player_buttons[-1]}
        )

    def update(self, dt: float) -> None:
        super().update(dt)

    def create_toggle_ai_button(self, index: int) -> None:
        def handler(event: Event) -> None:
            if NAME[index] in self.names:
                self.names.remove(NAME[index])
                event.target.set_text("+")
            else:
                self.names.append(NAME[index])
                event.target.set_text(NAME[index])

        return handler

    def start_with_player_count(self, event: Event) -> None:
        final_names = [self.name_input.text] + self.names
        NAME[0] = self.name_input.text
        count = len(final_names)
        if count == 1:
            return
        from game.ingame.ingamescene import InGameScene

        self.world.director.change_scene(InGameScene(self.world, count))
