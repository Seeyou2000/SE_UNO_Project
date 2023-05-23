from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from loguru import logger

from network.common.message import Message
from network.common.schema import parse_message

if TYPE_CHECKING:
    from network.server.common.room.roomsession import RoomSession

TMessage = TypeVar("TMessage", bound=Message)


def parse_if_valid_room(
    sid: str, message_cls: type[TMessage], data: dict, error_category: str
) -> tuple[RoomSession | None, type[TMessage] | None]:
    from network.server.common.room.roomrepository import room_repository

    room = room_repository.get_by_sid(sid)
    if room is None:
        logger.error("방이 없음")
        return (None, None)
    message = parse_message(message_cls, data, error_category)
    if message is None:
        return (None, None)
    return (room, message)
