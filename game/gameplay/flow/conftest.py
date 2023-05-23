import random
from collections.abc import Generator

import pytest

from game.constant import NAME
from game.gameplay.aicontroller import AIController, AIType
from game.gameplay.flow.gameflowmachine import GameFlowMachine
from game.gameplay.flow.prepare import PrepareFlowNode
from game.gameplay.gamestate import GameState
from game.gameplay.player import Player


@pytest.fixture(scope="package")
def game_state() -> Generator[GameState]:
    yield GameState()


@pytest.fixture(scope="package")
def flow_machine_2p(game_state: GameState) -> Generator[GameFlowMachine]:
    random.seed(2)
    flow = GameFlowMachine([])
    player_count = 2
    flow.transition_to(
        PrepareFlowNode(game_state, [Player(name) for name in NAME[:player_count]])
    )

    yield flow


@pytest.fixture(scope="package")
def flow_machine_2p_ai(
    game_state: GameState,
) -> Generator[tuple[GameFlowMachine, AIController]]:
    random.seed(2)
    player_count = 2
    players = [Player(name) for name in NAME[:player_count]]
    ai = AIController(AIType.NORMAL)
    flow = GameFlowMachine([ai])
    flow.transition_to(PrepareFlowNode(game_state, players))

    yield flow, ai
