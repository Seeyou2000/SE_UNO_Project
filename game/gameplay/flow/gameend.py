from engine.events.event import Event
from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.flow.gameflowmachine import GameFlowMachineEventType
from game.gameplay.gamestate import GameState


class GameEndFlowNode(AbstractGameFlowNode):
    def __init__(self, game_state: GameState) -> None:
        super().__init__(game_state)

    def enter(self) -> None:
        super().enter()
        self.machine.events.emit(
            GameFlowMachineEventType.GAME_END,
            Event(
                {
                    "turn": self.game_state.turn.current,
                    "player": self.game_state.get_current_player(),
                }
            ),
        )
