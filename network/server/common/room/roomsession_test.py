import asyncio
from collections.abc import Generator
from uuid import uuid4

import pytest
import pytest_asyncio

from network.server.common.room.roomsession import RoomSession, SlotStatusType
from network.server.common.user.usersession import UserSession
from network.server.server import io

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture
def host() -> Generator[UserSession]:
    yield UserSession(str(uuid4()), "HOST", "HOST")


@pytest.fixture
def user() -> Generator[UserSession]:
    yield UserSession(str(uuid4()), "USER", "USER")


@pytest_asyncio.fixture()
async def room(monkeypatch: pytest.MonkeyPatch, host: RoomSession) -> RoomSession:
    monkeypatch.setattr(io, "enter_room", lambda _, __: None)
    session = RoomSession(str(uuid4()), "TEST ROOM", None, host)
    tasks = asyncio.all_tasks()
    current_task = asyncio.current_task()
    tasks.remove(current_task)
    await asyncio.wait(tasks)

    return session


def test_initial_player_count(room: RoomSession) -> None:
    assert room.player_count == (1, 6)


@pytest.mark.asyncio
async def test_add_player(
    monkeypatch: pytest.MonkeyPatch, room: RoomSession, user: UserSession
) -> None:
    monkeypatch.setattr(io, "enter_room", lambda _, __: None)
    await room.join(None, user)
    current, _ = room.player_count
    assert current == 2


@pytest.mark.asyncio
async def test_remove_player(
    monkeypatch: pytest.MonkeyPatch,
    room: RoomSession,
    host: UserSession,
    user: UserSession,
) -> None:
    monkeypatch.setattr(io, "enter_room", lambda _, __: None)
    await room.join(None, user)

    await room.remove_human_player(user, SlotStatusType.OPEN)
    current, _ = room.player_count
    assert current == 1

    assert room.find_human_game_player(host.sid) is not None


@pytest.mark.asyncio
async def test_remove_host(
    monkeypatch: pytest.MonkeyPatch,
    room: RoomSession,
    host: UserSession,
    user: UserSession,
) -> None:
    monkeypatch.setattr(io, "enter_room", lambda _, __: None)
    await room.join(None, user)

    await room.remove_human_player(host, SlotStatusType.OPEN)
    current, _ = room.player_count
    assert current == 1

    assert room.find_human_game_player(user.sid) is not None
    assert room.host_player is user
