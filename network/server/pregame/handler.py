from loguru import logger

from game.gameplay.aicontroller import AIType
from network.common.messages.pregamehost import (
    AddAI,
    ClosePlayerSlot,
    KickPlayer,
    OpenPlayerSlot,
    StartGame,
    SwapPlayerSlot,
)
from network.server.common.room.roomsession import SlotStatusType
from network.server.server import io
from network.server.utils import parse_if_valid_room


@io.event
async def quit_room(sid: str) -> None:
    from network.server.common.room.roomrepository import room_repository
    from network.server.common.user.userrepository import user_repository

    user = await user_repository.get_by_sid(sid)
    room = room_repository.get_by_sid(sid)
    if room is None:
        logger.warning("방에 없는데 quit 요청을 날림")
        return
    await room.remove_human_player(user, SlotStatusType.OPEN)


@io.event
async def start_game(sid: str, data: dict) -> None:
    room, message = parse_if_valid_room(sid, StartGame, data, "게임 시작")
    if room is None or message is None:
        logger.warning("잘못된 메시지 형식")
        return

    await room.start_game(message.game_params)


@io.event
async def add_ai(sid: str, data: dict) -> None:
    room, message = parse_if_valid_room(sid, AddAI, data, "AI 추가")
    if room is None or message is None:
        logger.warning("잘못된 메시지 형식")
        return

    await room.add_ai_player(message.slot_index, AIType(message.ai_type))


@io.event
async def open_player_slot(sid: str, data: dict) -> None:
    room, message = parse_if_valid_room(sid, OpenPlayerSlot, data, "슬롯 열기")
    if room is None or message is None:
        logger.warning("잘못된 메시지 형식")
        return

    await room.open_player_slot(message.slot_index)


@io.event
async def close_player_slot(sid: str, data: dict) -> None:
    room, message = parse_if_valid_room(sid, ClosePlayerSlot, data, "슬롯 닫기")
    if room is None or message is None:
        logger.warning("잘못된 메시지 형식")
        return

    await room.close_player_slot(message.slot_index)


@io.event
async def swap_player_slot(sid: str, data: dict) -> None:
    room, message = parse_if_valid_room(sid, SwapPlayerSlot, data, "슬롯 열기")
    if room is None or message is None:
        logger.warning("잘못된 메시지 형식")
        return

    await room.swap_player_slot(message.before_slot_index, message.after_slot_index)


@io.event
async def kick_player(sid: str, data: dict) -> None:
    room, message = parse_if_valid_room(sid, KickPlayer, data, "슬롯 열기")
    if room is None or message is None:
        logger.warning("잘못된 메시지 형식")
        return

    await room.remove_player(message.slot_index, SlotStatusType.OPEN)
