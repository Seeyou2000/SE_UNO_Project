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
from network.client.client import clientio, my_user_id
from network.common.messages.pregame import HumanRemoved, PreGameMessageType
from network.common.schema import parse_message


class RoomScene(Scene):
    def __init__(self, world: World, room_id: str) -> None:
        super().__init__(world)

        clientio.on(PreGameMessageType.HUMAN_REMOVED.value, self.handle_human_removed)

        self.on("mouse_down", self.drag())
        self.on("mouse_up", self.drop())
        self.drag_data: str
        self.drag_button: Button = None
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
                "슬롯 열기",
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

        lobby_button = Button(
            "나가기", pygame.Rect(0, 0, 150, 60), self.font, self.handle_lobby_button
        )
        self.layout.add(lobby_button, LayoutAnchor.TOP_LEFT, pygame.Vector2(50, 50))
        self.add_child(lobby_button)

        start_button = Button(
            "게임 시작",
            pygame.Rect(0, 0, 180, 60),
            self.font,
        )
        self.layout.add(
            start_button, LayoutAnchor.BOTTOM_RIGHT, pygame.Vector2(-50, -50)
        )
        self.add_child(start_button)
        self.focus_controller.add(start_button)

    def handle_human_removed(self, data: dict) -> None:
        message = parse_message(HumanRemoved, data, "사람 나감")

        if message.id == my_user_id:
            from game.lobby.multilobbyscene import MultiLobbyScene

            self.world.director.change_scene(MultiLobbyScene(self.world))

    def handle_lobby_button(self, event: Event) -> None:
        from game.lobby.multilobbyscene import MultiLobbyScene

        clientio.emit(PreGameMessageType.QUIT_ROOM.value)
        self.world.director.change_scene(MultiLobbyScene(self.world))

    def update(self, dt: float) -> None:
        super().update(dt)
        self.connect_failure_timer.update(dt)

    def create_player_button_set(self, i: int) -> None:
        self.create_player_button(i)
        self.create_kick_button(i)
        self.create_return_button(i)

    def create_player_button(self, i: int) -> None:
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

    def drag(self) -> None:
        def handler(event: Event) -> None:
            # print(f"{event.target}")
            for player_button in self.player_buttons:
                if event.target is player_button and event.target.text != "+":
                    self.drag_data = event.target.text
                    self.drag_button = event.target
                    event.target.set_text("+")
                    break

        return handler

    def drop(self) -> None:
        def handler(event: Event) -> None:
            # print(f"{event.target}")
            for player_button in self.player_buttons:
                if (
                    self.drag_button is not None
                    and event.target is player_button
                    and self.drag_data != ""
                    and event.target.text == "+"
                ):
                    event.target.set_text(f"{self.drag_data}")
                    self.drag_data = ""
                    self.drag_button is None
                    return handler

            for player_button in self.player_buttons:
                if (
                    self.drag_button is not None
                    and self.drag_button is player_button
                    and self.drag_data != ""
                ):
                    self.drag_button.set_text(f"{self.drag_data}")
                    self.drag_data = ""
                    self.drag_button = None
                    break

        return handler
