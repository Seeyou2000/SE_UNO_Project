from loguru import logger

from network.common.messages.lobby import CreateRoom, JoinRoom
from network.common.models import LobbyRoom
from network.common.schema import parse_message
from network.server.server import io


@io.event
async def create_room(sid: str, data: dict) -> str | bool:
    from network.server.common.room.roomrepository import room_repository
    from network.server.common.user.userrepository import user_repository

    message = parse_message(CreateRoom, data, "방 생성")
    if message is None:
        return False

    user = await user_repository.get_by_sid(sid)
    created_room = room_repository.create(message.name, message.password, user)
    return created_room.id


@io.event
async def join_room(sid: str, data: dict) -> bool:
    from network.server.common.room.roomrepository import room_repository
    from network.server.common.user.userrepository import user_repository

    message = parse_message(JoinRoom, data, "방 입장")
    if message is None:
        return False

    room = room_repository.get_by_id(message.id)
    if room is None:
        return False

    user = await user_repository.get_by_sid(sid)
    return await room.join(message.password, user)


@io.event
async def room_list(sid: str) -> list[LobbyRoom]:
    from network.server.common.room.roomrepository import room_repository

    logger.info(f"{sid}")

    return room_repository.as_lobby_rooms()


@io.event
async def quit_room(sid: str) -> bool:
    from network.server.common.user.userrepository import user_repository

    await user_repository.delete(sid)
