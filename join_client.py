import asyncio

import socketio
from loguru import logger

from network.common.messages import JoinRoom
from network.common.models import LobbyRoom  # noqa: E402

sio = socketio.AsyncClient()


@sio.event
async def connect() -> None:
    logger.info("[CONNECT]")


@sio.event
async def disconnect() -> None:
    logger.info("[DISCONNECT]")


@sio.event
def lobby_room_list(data: list[LobbyRoom]) -> None:
    logger.info(f"[ROOM LIST] {data}")


async def main() -> None:
    await sio.connect("http://127.0.0.1:10008", auth={"username": "Test Player"})

    rooms = await sio.call("room_list")
    room = LobbyRoom.from_dict(rooms[0])

    success = await sio.call("join_room", JoinRoom(room.id, "mypassword").to_dict())
    if success:
        logger.info("Room joined")
    else:
        logger.error("Room join failed")

    await sio.wait()


if __name__ == "__main__":
    asyncio.run(main())
