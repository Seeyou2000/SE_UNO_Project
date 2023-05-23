import os

import socketio

from engine.events.emitter import EventEmitter
from engine.events.event import Event
from network.common.messages.common import Connected, PlayerNameChanged
from network.common.messages.pregame import RoomStateChanged
from network.common.models import PreGameRoom
from network.common.schema import parse_message

PORT = 10008
LOCAL_SERVER_ADDRESS = f"http://127.0.0.1:{PORT}"
REMOTE_SERVER_ADDRESS = f"{os.environ.get('SERVER_IP', 'http://127.0.0.1')}:{PORT}"


class Client(EventEmitter):
    io = socketio.Client(logger=True)

    my_id: str = ""
    my_name: str = "Player"
    pre_game_room: PreGameRoom | None = None

    def __init__(self) -> None:
        super().__init__()

        self.setup_handlers()

    def setup_handlers(self) -> None:
        @self.io.event
        def connected(data: dict) -> None:
            message = parse_message(Connected, data, "아이디 부여")
            self.my_id = message.id

        @self.io.event
        def player_name_changed(data: dict) -> None:
            message = parse_message(PlayerNameChanged, data, "새 이름")
            if message is None:
                return

            if message.id == self.my_id:
                self.my_name = message.new_name
                self.emit("my_name_changed", Event({"message": message}))

            self.emit("other_name_changed", Event({"message": message}))

        @self.io.event
        def room_state_changed(data: dict) -> None:
            message = parse_message(RoomStateChanged, data, "방 입장")
            if message is None:
                return

            print(message)

            self.pregame_room = message.room
            self.emit("room_state_changed", Event({"room": message.room}))

        @self.io.event
        def game_started(data: dict) -> None:
            pass

        @self.io.event
        def change_color_started(data: dict) -> None:
            pass
