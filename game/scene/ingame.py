import pygame

from engine.button import Button
from engine.scene import Scene
from engine.world import World
from game.gameplay.flow.gameflowmachine import (
    GameFlowMachine,
    GameFlowMachineEventType,
    TransitionEvent,
)
from game.gameplay.flow.gamestart import GameStartFlowNode
from game.gameplay.gamestate import GameState
from game.scene.constant import NAME
from game.scene.player import Player


class InGameScene(Scene):
    def __init__(self, world: World, player_count: int) -> None:
        super().__init__(world)

        from game.scene.menu import MenuScene

        menu_button = Button(
            "Back to menu",
            pygame.Rect(600, 500, 200, 100),
            pygame.font.SysFont("Arial", 20),
            lambda event: self.world.director.change_scene(MenuScene(self.world)),
        )
        deck_button = Button(
            "",
            pygame.Rect(300, 200, 30, 50),
            pygame.font.SysFont("Arial", 20),
            lambda event: self.game_state.get_current_player().draw_card(
                self.game_state.game_deck
            ),
        )
        self.hand = pygame.Rect(0, 500, 600, 100)
        self.add_children([menu_button, deck_button])

        self.game_state = GameState()

        self.flow = GameFlowMachine()

        self.flow.events.on(GameFlowMachineEventType.TRANSITION, self.handle_flow)
        self.flow.transition_to(
            GameStartFlowNode(
                self.game_state, [Player(name) for name in NAME[:player_count]]
            )
        )

    def update(self) -> None:
        super().update()

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)
        pygame.draw.rect(surface, (80, 188, 223, 0), self.hand)

    def handle_flow(self, event: TransitionEvent) -> None:
        match event.transition_from, event.transition_to:
            case "GameStartFlowNode", "TurnStartFlowNode":
                print("test")
