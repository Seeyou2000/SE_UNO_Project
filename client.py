import asyncio

import socketio
from loguru import logger

from network.common.messages import CreateRoom

sio = socketio.AsyncClient()


@sio.event
async def connect() -> None:
    logger.info("[CONNECT]")


@sio.event
async def disconnect() -> None:
    logger.info("[DISCONNECT]")


async def main() -> None:
    await sio.connect("http://127.0.0.1:10008", auth={"username": "Test Player"})

    await sio.emit(
        "create_room",
        CreateRoom("TESTROOM", "mypassword").to_dict(),
        callback=lambda: logger.info("Room created"),
    )

    await sio.emit("room_list", callback=lambda rooms: print(rooms))
    await sio.wait()


if __name__ == "__main__":
    asyncio.run(main())
