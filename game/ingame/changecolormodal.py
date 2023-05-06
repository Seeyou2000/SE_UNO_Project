import pygame

from engine.events.event import Event
from engine.gameobjectcontainer import GameObjectContainer
from engine.sprite import Sprite
from game.font import FontType, get_font
from game.gameplay.flow.gameflowmachine import GameFlowMachine
from game.gameplay.gamestate import GameState
from game.ingame.colorbutton import ColorButton
from game.settings.settings import Settings


class ChangeColorModal(GameObjectContainer):
    def __init__(
        self,
        game_state: GameState,
        flow_machine: GameFlowMachine,
        settings: Settings,
        is_prepare: bool,
    ) -> None:
        super().__init__()
        self.game_state = game_state
        self.is_prepare = is_prepare
        self.settings = settings

        surface = pygame.Surface([525, 150], pygame.SRCALPHA)
        pygame.draw.rect(surface, (12, 12, 12), surface.get_rect(), border_radius=45)
        background = Sprite(surface)
        self.add_child(background)

        self.rect = background.rect.copy()
        self.place_color_buttons()
        self.font = get_font(FontType.UI_BOLD, 20)
        self.flow_machine = flow_machine

    def place_color_buttons(self) -> None:
        red_color = ColorButton(
            pygame.Rect(25, 25, 100, 100),
            "red",
            self.settings,
            self.create_click_handler("red"),
        )
        self.add_child(red_color)

        yellow_color = ColorButton(
            pygame.Rect(150, 25, 100, 100),
            "yellow",
            self.settings,
            self.create_click_handler("yellow"),
        )
        self.add_child(yellow_color)

        green_color = ColorButton(
            pygame.Rect(275, 25, 100, 100),
            "green",
            self.settings,
            self.create_click_handler("green"),
        )
        self.add_child(green_color)

        blue_color = ColorButton(
            pygame.Rect(400, 25, 100, 100),
            "blue",
            self.settings,
            self.create_click_handler("blue"),
        )
        self.add_child(blue_color)

    def create_click_handler(self, color: str) -> None:
        def handler(event: Event) -> None:
            self.game_state.change_card_color(color)

            from game.gameplay.flow.endability import EndAbilityFlowNode

            self.flow_machine.transition_to(
                EndAbilityFlowNode(
                    self.game_state,
                    self.flow_machine.current_node.card,
                    self.is_prepare,
                )
            )

        return handler
