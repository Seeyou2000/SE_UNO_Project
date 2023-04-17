import random

from engine.event import Event
from game.constant import AbilityType
from game.gameplay.flow.drawcard import DrawCardFlowNode
from game.gameplay.flow.gameflowmachine import (
    GameFlowMachine,
    GameFlowMachineEventType,
    on_transition,
)
from game.gameplay.flow.startturn import StartTurnFlowNode
from game.gameplay.flow.validatecard import ValidateCardFlowNode
from game.gameplay.gamestate import GameState
from game.gameplay.player import Player


class AIPlayer:
    def __init__(
        self, player: Player, flow: GameFlowMachine, game_state: GameState
    ) -> None:
        self.player = player
        self.flow = flow
        self.game_state = game_state
        self.is_enabled = False

        transition_handlers = [
            on_transition(None, StartTurnFlowNode, self.is_ai_turn),
            # 우노
        ]
        self.flow.events.on(
            GameFlowMachineEventType.TRANSITION_COMPLETE, transition_handlers
        )

    def is_ai_turn(self, event: Event) -> None:
        if self.game_state.get_current_player() is self.player:
            self.is_enabled = True
            self.ai_time = random.random() * 3 + 1

    def action(self) -> None:
        if self.game_state.get_current_player() is not self.player:
            return
        if self.game_state.is_attacked():
            for card in self.game_state.get_current_player().cards:
                if (
                    card.ability == AbilityType.GIVE_FOUR_CARDS
                    or card.ability == AbilityType.GIVE_TWO_CARDS
                ):
                    self.flow.transition_to(ValidateCardFlowNode(self.game_state, card))
                    return
        print(self.game_state.get_current_player().name, self.player.name)
        now_number = self.game_state.discard_pile.get_last().number
        for card in self.player.cards:
            print(card)
            if (
                card.color == self.game_state.now_color
                or card.color == "black"
                or (card.number == now_number and now_number is not None)
            ):
                self.flow.transition_to(ValidateCardFlowNode(self.game_state, card))
                return
        self.flow.transition_to(DrawCardFlowNode(self.game_state))

    def update(self, dt: float) -> None:
        time, duration = self.game_state.turn_timer.get_time()

        if self.is_enabled and time > self.ai_time:
            self.action()
            self.is_enabled = False
