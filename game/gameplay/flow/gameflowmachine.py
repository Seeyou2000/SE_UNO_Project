from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from loguru import logger

from engine.events.emitter import EventEmitter, EventHandler
from engine.events.event import Event
from engine.fsm import FlowMachine

if TYPE_CHECKING:
    from game.gameplay.aicontroller import AIController

from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.gamestate import GameState
from game.gameplay.player import Player


class GameFlowMachineEventType(Enum):
    TRANSITION = "transition"
    TRANSITION_COMPLETE = "transition_complete"
    CARD_PLAYED = "card_played"
    GAME_END = "game_end"


class TransitionEvent(Event):
    before: AbstractGameFlowNode
    after: AbstractGameFlowNode

    def __init__(
        self,
        transition_from: AbstractGameFlowNode,
        transition_to: AbstractGameFlowNode,
    ) -> None:
        super().__init__(None)
        self.before = transition_from
        self.after = transition_to


class GameFlowMachine(FlowMachine, EventEmitter):
    events: EventEmitter
    ai_controllers: list[AIController]

    def __init__(self, ai_controllers: list[AIController]) -> None:
        super().__init__()
        self.events = EventEmitter()
        self.ai_controllers = ai_controllers

    def transition_to(self, new_node: AbstractGameFlowNode) -> None:
        self.events.emit(
            GameFlowMachineEventType.TRANSITION,
            TransitionEvent(self._current_node, new_node),
        )
        logger.info(
            f"[트랜지션] {type(self._current_node).__name__} -> {type(new_node).__name__}"
        )
        super().transition_to(new_node)
        self.events.emit(
            GameFlowMachineEventType.TRANSITION_COMPLETE,
            TransitionEvent(self._current_node, new_node),
        )

    def check_uno(self, game_state: GameState, pressed_player: Player) -> None:
        # 우노판별
        current_player = game_state.get_current_player()
        print(pressed_player.name + "가 눌렀습니다!!!!!!!!!!!!!!!!!!!!!!!")
        self.condition = False
        if current_player is pressed_player:
            if len(current_player.cards) == 2:
                game_state.set_uno_clicked(current_player)
                self.condition = True
            elif (
                len(current_player.cards) == 1 and pressed_player is not current_player
            ):
                game_state.set_uno_clicked(current_player)
                self.condition = True
        else:
            for player in game_state.players:
                if player is not pressed_player:
                    if len(player.cards) == 1 and player.is_unobutton_clicked is False:
                        game_state.draw_card(player)
                    else:
                        self.condition = False
            if len(pressed_player.cards) == 1:
                game_state.set_uno_clicked(pressed_player)
                self.condition = True
        # if self.condition is not True:
        # game_state.draw_card(pressed_player)

    def update(self, dt: float) -> None:
        super().update(dt)
        # from game.gameplay.aicontroller import AIController

        for ai in self.ai_controllers:
            ai.update(dt)


def on_transition(
    before: type[AbstractGameFlowNode] | None,
    after: type[AbstractGameFlowNode] | None,
    handler: EventHandler,
) -> EventHandler:
    def transition_handler(event: TransitionEvent) -> None:
        satisfies_before = before is None or isinstance(event.before, before)
        satisfies_after = after is None or isinstance(event.after, after)
        if satisfies_before and satisfies_after:
            handler(event)

    return transition_handler
