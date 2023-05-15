from loguru import logger

from game.gameplay.card import Card
from game.gameplay.flow.changefieldcolor import ChangeFieldColorFlowNode
from game.gameplay.flow.endability import EndAbilityFlowNode
from network.common.messages.ingame import ChangeColor, PlayCard
from network.server.server import io
from network.server.utils import parse_if_valid_room


@io.event
async def change_color(sid: str, data: dict) -> None:
    room, message = parse_if_valid_room(sid, ChangeColor, data, "색 변경")
    if room is None:
        return

    color = message.color

    # HACK: 이거 엄밀히 하려면 색 바꾸기 요청 받으면 요청한 플레이어를 저장하고
    # 그 외 플레이어에게서 요청이 오면 무시해야됨(패킷 만들어서 해킹하는 것 방지)
    if not isinstance(room.game_session.machine.current_node, ChangeFieldColorFlowNode):
        logger.warning("잘못된 요청")
        return

    machine = room.game_session.machine
    game_state = room.game_session.state

    card: Card = machine.current_node.card

    game_state.change_card_color(color)

    machine.transition_to(
        EndAbilityFlowNode(
            game_state,
            card,
            machine.current_node.is_prepare,
        )
    )


@io.event
async def play_card(sid: str, data: dict) -> None:
    room, message = parse_if_valid_room(sid, PlayCard, data, "카드 내기")
    if room is None:
        return

    await room.play_human_card(sid, message.card)
