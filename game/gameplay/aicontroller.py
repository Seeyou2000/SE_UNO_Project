import random
from enum import Enum

from engine.events.event import Event
from game.constant import COLORS, AbilityType
from game.gameplay.card import Card
from game.gameplay.flow.changefieldcolor import ChangeFieldColorFlowNode
from game.gameplay.flow.drawcard import DrawCardFlowNode
from game.gameplay.flow.endability import EndAbilityFlowNode
from game.gameplay.flow.gameend import GameEndFlowNode
from game.gameplay.flow.gameflowmachine import (
    GameFlowMachine,
    GameFlowMachineEventType,
    on_transition,
)
from game.gameplay.flow.startturn import StartTurnFlowNode
from game.gameplay.flow.validatecard import ValidateCardFlowNode
from game.gameplay.gamestate import GameState
from game.gameplay.player import Player
from game.gameplay.timer import Timer


class AIType(Enum):
    NORMAL = 0
    STAGE_1 = 1


class AIController:
    def __init__(self, ai_type: AIType) -> None:
        self.type = ai_type

    def setup(
        self, player: Player, machine: GameFlowMachine, game_state: GameState
    ) -> None:
        self.player = player
        self.machine = machine
        self.game_state = game_state

        self.uno_timer = Timer(5)
        self.uno_timer.on("tick", self.press_uno)
        self.is_enabled = False
        self.is_change_color_enabled = False
        self.is_waiting_uno = False
        self.ai_time = 50

        transition_handlers = [
            on_transition(None, StartTurnFlowNode, self.check_ai_turn_start),
            on_transition(None, ChangeFieldColorFlowNode, self.check_ai_change_color)
            # 우노
        ]
        self.machine.events.on(
            GameFlowMachineEventType.TRANSITION_COMPLETE, transition_handlers
        )

    def check_ai_turn_start(self, event: Event) -> None:
        if self.game_state.get_current_player() is self.player:
            self.is_enabled = True
            self.ai_time = random.random() * 3 + 1

    def check_ai_change_color(self, event: Event) -> None:
        if self.game_state.get_current_player() is self.player:
            self.is_change_color_enabled = True
            self.ai_time = random.random() * 0.5 + 0.5

    def check_ai_uno(self) -> bool:
        for player in self.game_state.players:
            if player is self.player and len(player.cards) == 2:
                self.is_waiting_uno = True
                self.uno_timer.set_duration(random.random() * 3 + 1)
                self.uno_timer.reset()
            elif len(player.cards) == 1:
                self.is_waiting_uno = True
                self.uno_timer.set_duration(random.random() * 3 + 1)
                self.uno_timer.reset()

    def press_uno(self, event: Event) -> None:
        self.machine.check_uno(self.game_state, self.player)
        self.is_waiting_uno = False

    def change_color(self) -> None:
        if self.game_state.get_current_player() is not self.player:
            return
        select_ai_color = random.choice(COLORS)
        self.game_state.change_card_color(select_ai_color)
        card: Card = self.machine._current_node.card  # noqa: SLF001
        self.machine.transition_to(
            EndAbilityFlowNode(
                self.game_state,
                card,
                self.machine._current_node.is_prepare,  # noqa: SLF001
            )
        )

    def action(self) -> None:
        if self.game_state.get_current_player() is not self.player:
            return
        if self.game_state.is_attacked():
            for card in self.game_state.get_current_player().cards:
                if (
                    card.ability == AbilityType.GIVE_FOUR_CARDS
                    or card.ability == AbilityType.GIVE_TWO_CARDS
                    or card.ability == AbilityType.ABSOULTE_ATTACK
                    or card.ability == AbilityType.ABSOULTE_PROTECT
                ):
                    self.machine.transition_to(
                        ValidateCardFlowNode(self.game_state, card)
                    )
                    return
        now_number = self.game_state.discard_pile.get_last().number
        print("----- AI 플레이어 패 -----")
        for card in self.player.cards:
            print(card)
        print("-----------------------")
        for card in self.player.cards:
            if (
                card.color == self.game_state.now_color
                or card.color == "black"
                or (card.number == now_number and now_number is not None)
            ):
                self.machine.transition_to(ValidateCardFlowNode(self.game_state, card))
                return
        self.machine.transition_to(DrawCardFlowNode(self.game_state))

    def update(self, dt: float) -> None:
        if isinstance(self.machine.current_node, GameEndFlowNode):
            return
        time, duration = self.game_state.turn_timer.get_time()

        if self.is_waiting_uno:
            self.uno_timer.update(dt)
        else:
            self.check_ai_uno()
        if time > self.ai_time:
            self.action()
            self.is_enabled = False
        if self.is_change_color_enabled and time > self.ai_time:
            self.change_color()
            self.is_change_color_enabled = False
