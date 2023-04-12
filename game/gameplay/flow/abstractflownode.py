from __future__ import annotations

import abc
from typing import TYPE_CHECKING

from engine.fsm import FlowNode
from game.gameplay.gamestate import GameState

if TYPE_CHECKING:
    from game.gameplay.flow.gameflowmachine import GameFlowMachine


class AbstractGameFlowNode(FlowNode, abc.ABC):
    game_state: GameState
    machine: GameFlowMachine

    def __init__(self, game_state: GameState) -> None:
        super().__init__()
        self.game_state = game_state
