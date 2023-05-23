import pygame

from engine.button import Button
from engine.events.event import Event
from engine.layout import LayoutAnchor, LayoutConstraint
from engine.scene import Scene
from engine.text import Text
from engine.textinput import TextInput
from engine.world import World
from game.changeplayernamemodal import ChangePlayerNameModal
from game.font import FontType, get_font
from game.gameplay.aicontroller import AIType
from game.gameplay.gameparams import GameParams
from game.gameplay.timer import Timer
from game.room.slot import SlotStatusType
from network.common.messages.common import PlayerNameChanged
from network.common.messages.pregame import PreGameMessageType
from network.common.messages.pregamehost import (
    AddAI,
    ClosePlayerSlot,
    HostMessageType,
    KickPlayer,
    OpenPlayerSlot,
    StartGame,
    SwapPlayerSlot,
)
from network.common.models import PreGameRoom, PreGameRoomSlot


class RoomScene(Scene):
    def __init__(self, world: World, room: PreGameRoom) -> None:
        super().__init__(world)

        self.world.client.on("my_name_changed", self.change_player_name)
        self.world.client.on("other_name_changed", self.change_other_player_name)

        self.place_ui()
        self.refresh(room)
        self.world.client.on("room_state_changed", self.handle_refresh)

    def cleanup(self) -> None:
        self.world.client.off("room_state_changed", self.handle_refresh)

    def place_ui(self) -> None:
        self.on("mouse_down", self.drag())
        self.on("mouse_up", self.drop())
        self.drag_data: PreGameRoomSlot | None = None
        self.drag_button: Button | None = None
        self.connect_failure_timer = Timer(2)
        self.text_connect_failure = Text(
            "", pygame.Vector2(), get_font(FontType.UI_BOLD, 20), pygame.Color("black")
        )
        self.connect_failure_timer.on("tick", self.hide_text_connect_failure)
        self.layout.add(
            self.text_connect_failure, LayoutAnchor.CENTER, pygame.Vector2(0, -300)
        )

        self.font = get_font(FontType.UI_BOLD, 20)

        self.password_text = Text(
            "PASSWORD",
            pygame.Vector2(50, 150),
            get_font(FontType.UI_BOLD, 16),
            pygame.Color("gray"),
        )
        self.add_child(self.password_text)
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
        self.add_ai_buttons: list[Button] = []
        self.open_slot_buttons: list[Button] = []
        self.player_buttons: list[Button] = []
        self.kick_buttons: list[Button] = []
        self.return_buttons: list[Button] = []

        for i in range(0, 6):
            button = Button(
                "AI",
                pygame.Rect(0, 0, 150, 100),
                self.font,
                lambda _, i=i: self.io.emit(
                    HostMessageType.ADD_AI.value,
                    AddAI(i, AIType.NORMAL.value).to_dict(),
                ),
            )
            self.add(
                button,
                LayoutConstraint(
                    LayoutAnchor.MIDDLE_RIGHT, pygame.Vector2(-200, (i - 3) * 500 / 5)
                ),
            )
            self.add_ai_buttons.insert(i, button)

            button = Button(
                "슬롯 열기",
                pygame.Rect(0, 0, 150, 100),
                self.font,
                lambda _, i=i: self.io.emit(
                    HostMessageType.OPEN_PLAYER_SLOT.value, OpenPlayerSlot(i).to_dict()
                ),
            )
            self.add(
                button,
                LayoutConstraint(
                    LayoutAnchor.MIDDLE_RIGHT,
                    pygame.Vector2(-50, (i - 3) * 500 / 5),
                ),
            )
            self.open_slot_buttons.insert(i, button)
            self.create_player_button_set(i)

        lobby_button = Button(
            "나가기", pygame.Rect(0, 0, 150, 60), self.font, self.handle_lobby_button
        )
        self.layout.add(lobby_button, LayoutAnchor.TOP_LEFT, pygame.Vector2(50, 50))
        self.add_child(lobby_button)

        start_button = Button(
            "게임 시작", pygame.Rect(0, 0, 180, 60), self.font, lambda _: self.start_game()
        )
        self.layout.add(
            start_button, LayoutAnchor.BOTTOM_RIGHT, pygame.Vector2(-50, -50)
        )
        self.add_child(start_button)
        self.focus_controller.add(start_button)

        self.player_name = Text(
            self.world.client.my_name,
            pygame.Vector2(),
            get_font(FontType.UI_BOLD, 30),
            pygame.Color("black"),
        )
        self.add(
            self.player_name,
            LayoutConstraint(LayoutAnchor.BOTTOM_LEFT, pygame.Vector2(60, -130)),
        )

        self.change_name_button = Button(
            "플레이어 이름 변경",
            pygame.Rect(0, 0, 180, 60),
            self.font,
            lambda _: self.show_change_player_name_modal(),
        )
        self.add(
            self.change_name_button,
            LayoutConstraint(LayoutAnchor.BOTTOM_LEFT, pygame.Vector2(50, -50)),
        )

    def handle_lobby_button(self, event: Event) -> None:
        from game.lobby.multilobbyscene import MultiLobbyScene

        self.io.emit(PreGameMessageType.QUIT_ROOM.value)
        self.world.director.change_scene(MultiLobbyScene(self.world))

    def handle_refresh(self, event: Event) -> None:
        self.refresh(event.data["room"])

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
        self.add(
            button,
            LayoutConstraint(
                LayoutAnchor.MIDDLE_RIGHT, pygame.Vector2(-50, (i - 3) * 500 / 5)
            ),
        )

    def create_kick_button(self, i: int) -> None:
        button = Button(
            "추방",
            pygame.Rect(0, 0, 60, 30),
            self.font,
            lambda _: self.io.emit(
                HostMessageType.KICK_PLAYER.value, KickPlayer(i).to_dict()
            ),
        )
        self.kick_buttons.insert(i, button)
        self.add(
            button,
            LayoutConstraint(
                LayoutAnchor.MIDDLE_RIGHT, pygame.Vector2(-55, (i - 3) * 500 / 5 - 30)
            ),
        )

    def create_return_button(self, i: int) -> None:
        button = Button(
            "<",
            pygame.Rect(0, 0, 30, 30),
            self.font,
            lambda _: self.io.emit(
                HostMessageType.CLOSE_PLAYER_SLOT.value, ClosePlayerSlot(i).to_dict()
            ),
        )
        self.return_buttons.insert(i, button)
        self.add(
            button,
            LayoutConstraint(
                LayoutAnchor.MIDDLE_RIGHT, pygame.Vector2(-315, (i - 3) * 500 / 5 - 30)
            ),
        )

    def open_slot(self, i: int, is_host: bool) -> None:
        self.player_buttons[i].set_text("+")
        self.player_buttons[i].is_visible = True
        self.return_buttons[i].is_visible = is_host

        self.add_ai_buttons[i].is_visible = False
        self.open_slot_buttons[i].is_visible = False

    def close_slot(self, i: int, is_host: bool) -> None:
        if is_host:
            self.player_buttons[i].is_visible = False
            self.return_buttons[i].is_visible = False

            self.add_ai_buttons[i].is_visible = True
            self.open_slot_buttons[i].is_visible = True
        else:
            self.player_buttons[i].set_text("닫힘")
            self.player_buttons[i].is_visible = True

    def set_host_control_visibility(self, visible: bool, host_index: int) -> None:
        for slot_index, kick_button in enumerate(self.kick_buttons):
            return_button = self.return_buttons[slot_index]
            if slot_index == host_index:
                return_button.is_visible = False
                kick_button.is_visible = False
                continue

            is_host_and_slot_occupied = (
                visible and self.room.slots[slot_index].player is not None
            )

            return_button.is_visible = is_host_and_slot_occupied
            kick_button.is_visible = is_host_and_slot_occupied

        self.password_text.is_visible = visible
        self.password_input.is_visible = visible

    def refresh(self, room: PreGameRoom) -> None:
        me = [
            slot
            for slot in room.slots
            if slot.player is not None and slot.player.id == self.world.client.my_id
        ]
        if len(me) == 0:
            # TODO: 싱글일때 다르게
            from game.lobby.multilobbyscene import MultiLobbyScene

            self.world.director.change_scene(MultiLobbyScene(self.world))
            return

        self.room = room
        host_index = [
            slot.slot_index
            for slot in room.slots
            if slot.player is not None and slot.player.id == room.host.id
        ]
        is_host = room.host.id == self.world.client.my_id
        self.set_host_control_visibility(is_host, host_index[0])

        for slot in room.slots:
            if slot.status is not None:
                if slot.status == SlotStatusType.CLOSE.value:
                    self.close_slot(slot.slot_index, is_host)
                else:
                    self.open_slot(slot.slot_index, is_host)
            else:
                self.player_buttons[slot.slot_index].set_text(slot.player.name)
                self.player_buttons[slot.slot_index].is_visible = True
                self.add_ai_buttons[slot.slot_index].is_visible = False
                self.open_slot_buttons[slot.slot_index].is_visible = False

    def start_game(self) -> None:
        self.io.emit(
            HostMessageType.START_GAME.value,
            # TODO
            StartGame(GameParams()).to_dict(),
        )

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
            for slot_index, player_button in enumerate(self.player_buttons):
                if (
                    event.target is player_button
                    and self.room.slots[slot_index].player is not None
                ):
                    self.drag_data = self.room.slots[slot_index]
                    self.drag_button = event.target
                    event.target.set_text("+")
                    break

        return handler

    def drop(self) -> None:
        def handler(event: Event) -> None:
            # print(f"{event.target}")
            for target_slot_index, player_button in enumerate(self.player_buttons):
                if (
                    self.drag_button is not None
                    and event.target is player_button
                    and self.drag_data is not None
                    and target_slot_index != self.drag_data.slot_index
                ):
                    self.io.emit(
                        HostMessageType.SWAP_PLAYER_SLOT.value,
                        SwapPlayerSlot(
                            self.drag_data.slot_index, target_slot_index
                        ).to_dict(),
                    )
                    self.drag_data = None
                    self.drag_button = None
                    break

        return handler

    def show_change_player_name_modal(self) -> None:
        self.change_player_name_modal = ChangePlayerNameModal(self)
        self.open_modal(self.change_player_name_modal)

    def change_player_name(self, event: Event) -> None:
        message: PlayerNameChanged = event.data["message"]

        self.player_name.set_text(message.new_name)

        for i, player_button in enumerate(self.player_buttons):
            slot = self.room.slots[i]
            if slot.player is not None and slot.player.id == message.id:
                player_button.set_text(message.new_name)

    def change_other_player_name(self, event: Event) -> None:
        message: PlayerNameChanged = event.data["message"]

        for i, player_button in enumerate(self.player_buttons):
            slot = self.room.slots[i]
            if slot.player is not None and slot.player.id == message.id:
                player_button.set_text(message.new_name)
