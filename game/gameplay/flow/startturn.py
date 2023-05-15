import random

from engine.events.event import Event
from game.constant import COLORS
from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.gamestate import GameState


class StartTurnFlowNode(AbstractGameFlowNode):
    def __init__(self, gamestate: GameState) -> None:
        super().__init__(gamestate)

    def enter(self) -> None:
        super().enter()

        is_turn_five = self.game_state.turn.total % 5 == 0
        if self.game_state.game_params.random_color and is_turn_five:
            self.game_state.change_card_color(random.choice(COLORS))

        if self.game_state.game_params.random_turn and is_turn_five:
            self.game_state.reverse_turn_direction()

        player = self.game_state.get_current_player()

        if self.game_state.is_absolute_attack():
            self.game_state.flush_attack_cards(self.game_state.get_current_player())
        if self.game_state.is_attacked():
            if not self.game_state.have_attack_card_or_protect_card():
                self.game_state.flush_attack_cards(self.game_state.get_current_player())
        self.game_state.turn_timer.on("tick", self.transition_to_draw_card)

        if len(player.cards) == 1 and player.is_unobutton_clicked is not True:
            self.game_state.draw_card(player)

    def transition_to_draw_card(self, event: Event) -> None:
        if self.game_state.is_attacked():
            self.game_state.flush_attack_cards(self.game_state.get_current_player())
        from game.gameplay.flow.drawcard import DrawCardFlowNode

        self.machine.transition_to(DrawCardFlowNode(self.game_state))

    def update(self, dt: float) -> None:
        super().update(dt)

    def exit(self) -> None:
        super().exit()
        self.game_state.turn_timer.off("tick", self.transition_to_draw_card)
