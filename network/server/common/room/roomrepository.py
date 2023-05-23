from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from loguru import logger

from network.common.models import LobbyRoom
from network.server.common.room.roomsession import RoomSession

if TYPE_CHECKING:
    from network.server.common.user.usersession import UserSession
from network.server.server import io


class RoomRepository:
    _room_by_id: dict[UUID, RoomSession]

    def __init__(self) -> None:
        self._room_by_id = {}

    def create(self, name: str, password: str | None, host: UserSession) -> RoomSession:
        new_id = str(uuid4())
        new_room = RoomSession(
            new_id,
            name,
            password,
            host,
        )
        self._room_by_id[new_id] = new_room
        logger.success(f"user: {host}, room id: {new_id}")
        return new_room

    def delete(self, room_id: str) -> None:
        del self._room_by_id[room_id]

    def has(self, room_id: str) -> bool:
        return self.get_by_id(room_id) is not None

    def get_by_id(self, room_id: str) -> RoomSession | None:
        return self._room_by_id.get(room_id, None)

    def get_by_sid(self, user_sid: str) -> RoomSession | None:
        room_ids = io.rooms(user_sid)
        room_ids = list(filter(lambda id: id != user_sid, room_ids))
        if len(room_ids) > 1:
            logger.error("방에 두 번 들어갔으면 안되는데 들어감")
        if len(room_ids) == 0:
            return None
        return self._room_by_id.get(room_ids[0], None)

    def update_rooms(self, dt: float) -> None:
        for room in self._room_by_id.values():
            if room.game_session is None:
                continue

            machine = room.game_session.machine
            if machine is None:
                continue
            machine.update(dt)

    def as_lobby_rooms(self) -> list[LobbyRoom]:
        return [room.as_lobby().to_dict() for room in self._room_by_id.values()]


room_repository = RoomRepository()
