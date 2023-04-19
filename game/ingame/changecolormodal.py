import pygame

from engine.button import Button
from engine.gameobjectcontainer import GameObjectContainer
from engine.sprite import Sprite
from game.font import FontType, get_font
from game.gameplay.flow.gameflowmachine import GameFlowMachine
from game.gameplay.gamestate import GameState


class ChangeColorModal(GameObjectContainer):
    def __init__(self, game_state: GameState, flow_machine: GameFlowMachine) -> None:
        super().__init__()
        self.game_state = game_state
        self.surface = pygame.Surface([520, 300])
        self.surface.fill((128, 0, 0))
        self.rect = pygame.Rect(0, 0, 500, 300)
        self.sprite = Sprite(self.surface)
        self.add_child(self.sprite)
        self.font = get_font(FontType.UI_BOLD, 20)
        self.show_black_to_another()

    def show_black_to_another(self) -> None:
        red_color = Button(
            "red",
            pygame.Rect(0, 50, 70, 200),
            self.font,
            lambda _: self.game_state.change_card_color("red"),
        )
        self.add_child(red_color)

        yellow_color = Button(
            "yellow",
            pygame.Rect(100, 50, 150, 200),
            self.font,
            lambda _: self.game_state.change_card_color("yellow"),
        )
        self.add_child(yellow_color)

        green_color = Button(
            "green",
            pygame.Rect(200, 50, 225, 200),
            self.font,
            lambda _: self.game_state.change_card_color("green"),
        )
        self.add_child(green_color)

        blue_color = Button(
            "blue",
            pygame.Rect(300, 50, 300, 200),
            self.font,
            lambda _: self.game_state.change_card_color("blue"),
        )
        self.add_child(blue_color)

    # def handle_click(self) -> None:
    #    from game.gameplay.flow.endability import EndAbilityFlowNode


#        self.machine.transition_to(
#           EndAbilityFlowNode(self.game_state, self.card, self.is_prepare)
#      )
