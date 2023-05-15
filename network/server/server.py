import asyncio
import sys
from collections.abc import Awaitable, Callable
from time import monotonic_ns

from aiohttp import web
from loguru import logger
from socketio import AsyncServer

from network.common.messages.common import CommonMessageType, Connected

app = web.Application()
io = AsyncServer(async_mode="aiohttp", logger=True)
io.attach(app)


@io.event
async def connect(sid: str, environ: dict, auth: dict) -> None:
    from network.server.common.user.userrepository import user_repository

    logger.info(f"[접속] {auth['username']}({sid})")
    id = await user_repository.create(sid, auth["username"])
    await io.emit(CommonMessageType.CONNECTED.value, Connected(id).to_dict())


@io.event
async def disconnect(sid: str) -> None:
    from network.server.common.user.userrepository import user_repository

    name = await user_repository.delete(sid)
    logger.info(f"[접속 해제] {name}({sid})")


"""
HACK: on-import side effect를 사용하는건 좋지 않은 일이지만,
일을 가시적으로 나누기 위해 사용
"""
import network.server.ingame.handler  # noqa: E402, F401
import network.server.lobby.handler  # noqa: E402, F401
import network.server.pregame.handler  # noqa: E402, F401

TARGET_SERVER_TICK = 1 / 20


async def loop() -> None:
    from network.server.common.room.roomrepository import room_repository

    # HACK: 싱글스레드지만 급하니까
    game_time_seconds = monotonic_ns() / 1_000_000_000

    while True:
        current_time_seconds = monotonic_ns() / 1_000_000_000

        while current_time_seconds - game_time_seconds > TARGET_SERVER_TICK:
            room_repository.update_rooms(TARGET_SERVER_TICK)
            game_time_seconds += TARGET_SERVER_TICK

            if current_time_seconds - game_time_seconds > 4 * TARGET_SERVER_TICK:
                game_time_seconds = current_time_seconds

        await asyncio.sleep(TARGET_SERVER_TICK)


task: asyncio.Task


async def start_game_loop(_: web.Application) -> None:
    global task
    task = asyncio.create_task(loop())


def run_server(task: Callable[[Awaitable[None]], None] | None = None) -> None:
    if task is not None:
        app.on_startup.append(task)
    app.on_startup.append(start_game_loop)
    web.run_app(app, port=10008)
