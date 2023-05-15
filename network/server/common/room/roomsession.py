import asyncio
from enum import Enum
from uuid import UUID

from loguru import logger

from game.gameplay.aicontroller import AIController
from game.gameplay.card import Card
from game.gameplay.flow.changefieldcolor import ChangeFieldColorFlowNode
from game.gameplay.flow.endability import EndAbilityFlowNode
from game.gameplay.flow.gameflowmachine import (
    GameFlowMachine,
    GameFlowMachineEventType,
    on_transition,
)
from game.gameplay.flow.prepare import PrepareFlowNode
from game.gameplay.flow.startturn import StartTurnFlowNode
from game.gameplay.flow.useability import UseAbilityFlowNode
from game.gameplay.gameparams import GameParams
from game.gameplay.gamestate import GameState
from game.gameplay.player import Player
from network.common.messages.ingame import InGameMessageType
from network.common.messages.pregame import HostChanged, PreGameMessageType
from network.common.models import LobbyRoom
from network.server.common.room.models import RoomAIPlayer, RoomHumanPlayer, RoomPlayer
from network.server.common.user.usersession import UserSession
from network.server.ingame.gamesession import GameSession
from network.server.server import io


class SlotState(Enum):
    CLOSE = 0
    OPEN = 1


Slot = RoomAIPlayer | RoomHumanPlayer | SlotState


class RoomSession:
    MAX_PLAYER = 6
    id: str
    name: str
    host_player: UserSession
    slots: dict[int, Slot]
    password: str | None
    game_session: GameSession

    def __init__(
        self,
        id: str,
        name: str,
        password: str | None,
        host_player: UserSession,
    ) -> None:
        self.id = id
        self.name = name
        self.host_player = host_player
        self.slots = {i: SlotState.OPEN for i in range(0, self.MAX_PLAYER)}
        self.slots[0] = RoomHumanPlayer(host_player)
        io.enter_room(host_player.sid, self.id)

        self.password = password
        self.is_game_started = False
        self.game_session = None

    async def join(self, password: str | None, user: UserSession) -> bool:
        is_same_password = (
            self.password is password if password is None else self.password == password
        )

        current_players, max_players = self.player_count
        is_not_full = current_players < max_players

        if is_same_password and is_not_full:
            io.enter_room(user.sid, self.id)
            await self.add_human_player(user)

            logger.success(f"[방 입장] 플레이어: {user.sid}, 방 ID: {self.id}")
            return True

        if not is_same_password:
            logger.warning(f"[방 입장 실패] 비밀번호 틀림(플레이어: {user.sid}, 시도한 ID: {self.id})")

        return False

    async def add_human_player(self, user: UserSession) -> None:
        if self.has_human_player(user) is True:
            logger.error("중복 입장")
            return
        available_index = 0
        while self.slots[available_index] != SlotState.OPEN:
            available_index += 1
        if available_index >= 6:
            return
        self.slots[available_index] = RoomHumanPlayer(user)

        await io.emit("room_player_changed", room=self.id)

    async def remove_human_player(self, user_to_remove: UserSession) -> None:
        from network.server.common.room.roomrepository import room_repository

        def is_user_slot(slot: Slot) -> bool:
            match slot:
                case RoomHumanPlayer(user=user) if user is user_to_remove:
                    return True
                case _:
                    return False

        self.slots = {
            key: slot for key, slot in self.slots.items() if not is_user_slot(slot)
        }

        if user_to_remove is self.host_player:
            logger.info("방장이 나감")
            human_players = self.get_human_players()
            if len(human_players) > 0:
                self.host_player = human_players[0].user

        if len(human_players) == 0:
            logger.info("방에 아무도 없어서 방 제거")
            room_repository.delete(self.id)
            return

        await io.emit(PreGameMessageType.HUMAN_ADDED, room=self.id)
        await io.emit(
            PreGameMessageType.HOST_CHANGED,
            HostChanged(self.host_player.id).to_dict(),
            room=self.id,
        )

    async def start_game(self, game_params: GameParams) -> None:
        self.is_game_started = True
        self.setup_session(game_params)

    def setup_session(self, game_params: GameParams) -> None:
        game_players: list[Player] = []
        ai_controllers: list[AIController] = []
        for index, room_player in self.players.items():
            game_player = Player(room_player.get_name())
            self.game_player_by_room_player[room_player] = game_player
            game_players.append(game_player)

            if isinstance(room_player, RoomAIPlayer):
                ai_controllers.append(room_player.controller)
                game_player.name = f"AI {index}"

        self.game_session = GameSession(
            GameFlowMachine(ai_controllers), GameState(game_params)
        )
        machine = self.game_session.machine

        transition_handlers = [
            on_transition(
                UseAbilityFlowNode,
                ChangeFieldColorFlowNode,
                lambda _: asyncio.create_task(
                    self.sio.emit(InGameMessageType.CHANGE_COLOR_STARTED, room=self.id)
                ),
            ),
            on_transition(
                ChangeFieldColorFlowNode,
                EndAbilityFlowNode,
                lambda _: asyncio.create_task(
                    self.sio.emit(InGameMessageType.CHANGE_COLOR_FINISHED, room=self.id)
                ),
            ),
            on_transition(
                None,
                StartTurnFlowNode,
                lambda _: asyncio.create_task(
                    self.sio.emit(InGameMessageType.GAME_STARTED, room=self.id)
                ),
            ),
            # on_transition(
            #     None,
            #     StartTurnFlowNode,
            #     lambda event: print(
            #         f"턴 시작: {self.game_state.get_current_player().name}"
            #     ),
            # ),
            # on_transition(None, StartTurnFlowNode, self.handle_color_change),
            # on_transition(None, StartTurnFlowNode, self.handle_reverse_change),
            # on_transition(DiscardCardFlowNode, None, self.place_discarded_card),
            # on_transition(None, GameEndFlowNode, self.end_game),
            # on_transition(None, GameEndFlowNode, self.back_to_menu),
        ]
        machine.events.on(GameFlowMachineEventType.TRANSITION, transition_handlers)

        machine.transition_to(
            PrepareFlowNode(
                self.game_session.state,
                game_players,
            )
        )

    def get_ai_players(self) -> list[RoomAIPlayer]:
        return [p for p in self.slots.values() if isinstance(p, RoomAIPlayer)]

    def get_human_players(self) -> list[RoomHumanPlayer]:
        return [p for p in self.slots.values() if isinstance(p, RoomHumanPlayer)]

    def has_human_player(self, user: UserSession) -> bool:
        existing_players = list(
            filter(
                lambda p: p.user is user,
                self.get_human_players(),
            )
        )

        return len(existing_players) > 0

    def find_human_game_player(self, sid: str) -> RoomHumanPlayer | None:
        existing_players = list(
            filter(
                lambda p: p.user.sid == sid,
                self.get_human_players(),
            )
        )

        return None if len(existing_players) == 0 else existing_players[0]

    def change_color(self, color: str) -> None:
        # HACK: 이거 엄밀히 하려면 색 바꾸기 요청 받으면 요청한 플레이어를 저장하고
        # 그 외 플레이어에게서 요청이 오면 무시해야됨(패킷 만들어서 해킹하는 것 방지)
        card: Card = self.flow._current_node.card  # noqa: SLF001
        self.game_state.change_card_color(color)
        self.game_session.machine.transition_to(
            EndAbilityFlowNode(
                self.game_state,
                card,
                self.flow._current_node.is_prepare,  # noqa: SLF001
            )
        )

    def open_player_slot(self, slot_index: int) -> None:
        match self.slots[slot_index]:
            case SlotState.CLOSE:
                self.slots[slot_index] = SlotState.OPEN

    def swap_player_slot(self, left: int, right: int) -> None:
        self.slots[left], self.slots[right] = self.slots[right], self.slots[left]

    @property
    def player_count(self) -> tuple[int, int]:
        current_player_count = 0
        max_player_count = 0

        for slot in self.slots.values():
            match slot:
                case SlotState.OPEN:
                    max_player_count += 1
                case RoomPlayer():
                    current_player_count += 1
                    max_player_count += 1

        return (current_player_count, max_player_count)

    def convert_to_lobby(self) -> LobbyRoom:
        current, max = self.player_count
        return LobbyRoom(
            self.id,
            self.name,
            self.host_player.name,
            current,
            max,
            self.password is not None,
            self.is_game_started,
        )

    def __str__(self) -> str:
        return f"ServerRoomMetadata(id: {self.id}, name: {self.name}, host:{self.host_player.name})"  # noqa: E501
