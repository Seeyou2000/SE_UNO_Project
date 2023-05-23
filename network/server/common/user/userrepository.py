from typing import cast
from uuid import uuid4

from network.server.common.room.roomrepository import room_repository
from network.server.common.room.roomsession import SlotStatusType
from network.server.common.user.usersession import UserSession
from network.server.server import io


class UserRepository:
    async def create(self, sid: str, username: str) -> str:
        new_user_id = str(uuid4())
        await io.save_session(
            sid,
            {
                "session": UserSession(
                    new_user_id,
                    username,
                    sid,
                )
            },
        )
        return new_user_id

    async def get_by_sid(self, sid: str) -> UserSession:
        async with io.session(sid) as session:
            user = cast(UserSession, session["session"])
            return user

    async def delete(self, sid: str) -> str:
        user = await user_repository.get_by_sid(sid)
        room = room_repository.get_by_sid(sid)
        if room is not None:
            await room.remove_human_player(user, SlotStatusType.OPEN)
        return user.name


user_repository = UserRepository()
