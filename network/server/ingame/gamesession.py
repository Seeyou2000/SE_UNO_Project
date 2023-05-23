from dataclasses import dataclass

from game.gameplay.flow.gameflowmachine import GameFlowMachine
from game.gameplay.gamestate import GameState


class GameSession:
    machine: GameFlowMachine
    state: GameState

    def __init__(self, machine: GameFlowMachine, state: GameState) -> None:
        self.machine = machine
        self.state = state
