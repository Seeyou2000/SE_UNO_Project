from typing import cast
from uuid import uuid4

import socketio
from aiohttp import web
from loguru import logger

from network.common.messages import CreateRoom, JoinRoom, parse_message
from network.server.room import (
    PlayerLocation,
    PlayerSession,
    ServerRoomMetadata,
)

sio = socketio.AsyncServer(async_mode="aiohttp")
app = web.Application()
sio.attach(app)

room_meta_by_id: dict[str, ServerRoomMetadata] = {}


@sio.event
async def connect(sid: str, environ: dict, auth: dict) -> None:
    logger.info(f"[CONNECT] {auth['username']}({sid})")

    # TODO: 재접속 처리
    await sio.save_session(
        sid,
        {
            "session": PlayerSession(
                auth["username"],
                sid,
                PlayerLocation.LOBBY,
            )
        },
    )


@sio.event
async def disconnect(sid: str) -> None:
    name = (await sio.get_session(sid))["session"].name
    logger.info(f"[CONNECT] {name}({sid})")


@sio.event
async def room_list(sid: str) -> None:
    logger.info(f"{sid}")
    return [
        room_meta.convert_to_lobby().to_dict() for room_meta in room_meta_by_id.values()
    ]


@sio.event
async def create_room(sid: str, data: dict) -> None:
    message = parse_message(CreateRoom, data, "CREATE ROOM")
    if message is None:
        return

    new_room_id = str(uuid4())

    host_player_session = await sio.get_session(sid)
    room_meta_by_id[new_room_id] = ServerRoomMetadata(
        new_room_id, message.name, host_player_session["session"], message.password
    )

    logger.success(f"[CREATE ROOM] by: {sid}, room id: {new_room_id}")
    join_room_impl(sid, new_room_id, message.password)


@sio.event
async def join_room(sid: str, data: dict) -> bool:
    message = parse_message(JoinRoom, data, "JOIN ROOM")
    if message is None:
        return

    return await join_room_impl(sid, message.id, message.password)


async def join_room_impl(sid: str, room_id: str, password: str) -> bool:
    is_room_exist = room_id in room_meta_by_id.keys()
    is_same_password = room_meta_by_id[room_id].password == password

    if is_room_exist and is_same_password:
        sio.enter_room(sid, room_id)

        async with sio.session(sid) as session:
            player = cast(PlayerSession, session["session"])
            player.current_location = PlayerLocation.ROOM

        logger.success(f"[JOIN ROOM] {sid} to {room_id}")
        return True

    if not is_room_exist:
        logger.warning(f"[JOIN ROOM FAILED] No room({sid} to {room_id})")
    elif not is_same_password:
        logger.warning(f"[JOIN ROOM FAILED] Wrong password({sid} to {room_id})")

    return False


def run() -> None:
    web.run_app(app, port=10008)
