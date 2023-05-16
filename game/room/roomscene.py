import pygame

from engine.button import Button
from engine.events.event import Event
from engine.focus import FocusMoveDirection
from engine.layout import LayoutAnchor
from engine.scene import Scene
from engine.text import Text
from engine.textinput import TextInput
from engine.world import World
from game.constant import NAME
from game.font import FontType, get_font
from game.gameplay.timer import Timer


class RoomScene(Scene):
    def __init__(self, world: World) -> None:
        super().__init__(world)

        self.connect_failure_timer = Timer(2)
        self.text_connect_failure = Text(
            "", pygame.Vector2(), get_font(FontType.UI_BOLD, 20), pygame.Color("black")
        )
        self.connect_failure_timer.on("tick", self.hide_text_connect_failure)
        self.layout.add(
            self.text_connect_failure, LayoutAnchor.CENTER, pygame.Vector2(0, -300)
        )

        self.font = get_font(FontType.UI_BOLD, 20)

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
            self.focus_controller,
        )
        self.add_child(self.name_input)
        self.focus_controller.add(self.name_input)

        password_text = Text(
            "PASSWORD",
            pygame.Vector2(50, 150),
            get_font(FontType.UI_BOLD, 16),
            pygame.Color("gray"),
        )
        self.add_child(password_text)
        self.password_input = TextInput(
            "",
            pygame.Rect(50, 190, 300, 80),
            get_font(FontType.UI_BOLD, 30),
            pygame.Color("black"),
            10,
            self.focus_controller,
        )
        self.add_child(self.password_input)
        self.focus_controller.add(self.password_input)

        self.names = []
        self.ai_buttons = []
        self.player_slot_buttons = []
        self.player_buttons = []
        self.return_buttons = []
        self.kick_buttons = []

        for i in range(0, 5):
            button = Button(
                "AI",
                pygame.Rect(0, 0, 150, 100),
                self.font,
            )
            self.layout.add(
                button,
                LayoutAnchor.MIDDLE_RIGHT,
                pygame.Vector2(-200, (i - 3) * 500 / 5),
            )
            self.focus_controller.add(button)
            self.add_child(button)
            self.ai_buttons.insert(i, button)

            button = Button(
                "Player Slot",
                pygame.Rect(0, 0, 150, 100),
                self.font,
                self.show_buttons(i),
            )
            self.layout.add(
                button,
                LayoutAnchor.MIDDLE_RIGHT,
                pygame.Vector2(-50, (i - 3) * 500 / 5),
            )
            self.focus_controller.add(button)
            self.add_child(button)
            self.player_slot_buttons.insert(i, button)
            self.create_player_button_set(i)

        from game.menu.menuscene import MenuScene

        menu_button = Button(
            "Back to menu",
            pygame.Rect(0, 0, 180, 60),
            self.font,
            lambda _: self.world.director.change_scene(MenuScene(self.world)),
        )
        self.layout.add(
            menu_button, LayoutAnchor.BOTTOM_RIGHT, pygame.Vector2(-250, -50)
        )
        self.add_child(menu_button)

        start_button = Button(
            "Start",
            pygame.Rect(0, 0, 180, 60),
            self.font,
        )
        self.layout.add(
            start_button, LayoutAnchor.BOTTOM_RIGHT, pygame.Vector2(-50, -50)
        )
        self.add_child(start_button)
        self.focus_controller.add(start_button)

    def update(self, dt: float) -> None:
        super().update(dt)
        self.connect_failure_timer.update(dt)

    def create_player_button_set(self, i: int) -> None:
        self.create_player_slot_button(i)
        self.create_kick_button(i)
        self.create_return_button(i)

    def create_player_slot_button(self, i: int) -> None:
        button = Button(
            "+",
            pygame.Rect(0, 0, 300, 100),
            self.font,
        )
        self.player_buttons.insert(i, button)

    def create_kick_button(self, i: int) -> None:
        button = Button(
            "X",
            pygame.Rect(0, 0, 30, 30),
            self.font,
        )
        self.kick_buttons.insert(i, button)

    def create_return_button(self, i: int) -> None:
        button = Button(
            "◀", pygame.Rect(0, 0, 30, 30), self.font, self.remove_buttons(i)
        )
        self.return_buttons.insert(i, button)

    def show_buttons(self, i: int) -> None:
        def handler(event: Event) -> None:
            self.layout.add(
                self.player_buttons[i],
                LayoutAnchor.MIDDLE_RIGHT,
                pygame.Vector2(-50, (i - 3) * 500 / 5),
            )
            self.focus_controller.add(self.player_buttons[i])
            self.add_child(self.player_buttons[i])
            self.layout.add(
                self.kick_buttons[i],
                LayoutAnchor.MIDDLE_RIGHT,
                pygame.Vector2(-55, (i - 3) * 500 / 5 - 30),
            )
            self.focus_controller.add(self.kick_buttons[i])
            self.add_child(self.kick_buttons[i])
            self.layout.add(
                self.return_buttons[i],
                LayoutAnchor.MIDDLE_RIGHT,
                pygame.Vector2(-315, (i - 3) * 500 / 5 - 30),
            )
            self.focus_controller.add(self.return_buttons[i])
            self.add_child(self.return_buttons[i])

            self.remove_child(self.ai_buttons[i])
            self.layout.remove(self.ai_buttons[i])
            self.focus_controller.remove(self.ai_buttons[i])
            self.remove_child(self.player_slot_buttons[i])
            self.layout.remove(self.player_slot_buttons[i])
            self.focus_controller.remove(self.player_slot_buttons[i])

        return handler

    def remove_buttons(self, i: int) -> None:
        def handler(event: Event) -> None:
            self.remove_child(self.player_buttons[i])
            self.layout.remove(self.player_buttons[i])
            self.focus_controller.remove(self.player_buttons[i])
            self.remove_child(self.return_buttons[i])
            self.layout.remove(self.return_buttons[i])
            self.focus_controller.remove(self.return_buttons[i])
            self.remove_child(self.kick_buttons[i])
            self.layout.remove(self.kick_buttons[i])
            self.focus_controller.remove(self.kick_buttons[i])

            self.layout.add(
                self.ai_buttons[i],
                LayoutAnchor.MIDDLE_RIGHT,
                pygame.Vector2(-200, (i - 3) * 500 / 5),
            )
            self.focus_controller.add(self.ai_buttons[i])
            self.add_child(self.ai_buttons[i])

            self.layout.add(
                self.player_slot_buttons[i],
                LayoutAnchor.MIDDLE_RIGHT,
                pygame.Vector2(-50, (i - 3) * 500 / 5),
            )
            self.focus_controller.add(self.player_slot_buttons[i])
            self.add_child(self.player_slot_buttons[i])

        return handler

    def connect_failure(self) -> None:
        self.text_connect_failure.set_text("다른 플레이어가 접속할 슬롯이 없어 접속하지 못했습니다.")
        if not self.has_child(self.text_connect_failure):
            self.add_child(self.text_connect_failure)
        self.connect_failure_timer.reset()

    def hide_text_connect_failure(self, event: Event) -> None:
        if self.has_child(self.text_connect_failure):
            self.remove_child(self.text_connect_failure)
