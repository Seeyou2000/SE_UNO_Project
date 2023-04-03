from typing import Callable

import pygame

from engine.button import Button
from engine.event import Event
from engine.scene import Scene
from engine.world import World
from game.constant import NAME
from game.gameplay.card import Card
from game.gameplay.flow.abilitycard import AbilityCardFlowNode
from game.gameplay.flow.drawcard import DrawCardFlowNode
from game.gameplay.flow.gameflowmachine import (
    GameFlowMachine,
    GameFlowMachineEventType,
    TransitionEvent,
)
from game.gameplay.flow.gamestart import GameStartFlowNode
from game.gameplay.flow.numbercard import NumberCardFlowNode
from game.gameplay.gamestate import GameState
from game.gameplay.player import Player


class InGameScene(Scene):
    def __init__(self, world: World, player_count: int) -> None:
        super().__init__(world)

        from game.menu.menuscene import MenuScene

        self.player_count = player_count
        self.name = NAME
        menu_button = Button(
            "Back to menu",
            pygame.Rect(600, 500, 200, 100),
            pygame.font.SysFont("Arial", 20),
            lambda event: self.world.director.change_scene(MenuScene(self.world)),
        )
        self.deck_button = Button(
            "",
            pygame.Rect(300, 200, 30, 50),
            pygame.font.SysFont("Arial", 20),
            lambda event: self.flow.transition_to(DrawCardFlowNode(self.game_state)),
        )

        self.hand = pygame.Rect(0, 500, 600, 100)
        self.otherplayers = pygame.Rect(600, 0, 200, 500)
        self.otherplayer = []
        for i in range(0, self.player_count - 1):
            self.otherplayer.append(pygame.Rect(600, i * 100, 200, 100))
        self.otherplayertext = []
        for i in range(0, self.player_count - 1):
            self.otherplayertext.append(
                Button(
                    self.name[i + 1],
                    pygame.Rect(600, i * 100, 200, 20),
                    pygame.font.SysFont("Arial", 20),
                )
            )
            self.add_child(self.otherplayertext[i])
        self.add_children([menu_button, self.deck_button])

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
        pygame.draw.rect(surface, (80, 188, 223, 0), self.hand)
        pygame.draw.rect(surface, (100, 100, 100, 0), self.otherplayers)
        for i in range(0, self.player_count - 1):
            pygame.draw.rect(surface, (230, 230, 230, 0), self.otherplayer[i])
        super().render(surface)

    """def handle_flow(self, event: TransitionEvent) -> None:
        match event.transition_from, event.transition_to:
            case _, "TurnStartFlowNode":
                self.add_children(self.game_state.get_current_player().cards)
                self.add_child(self.game_state.drawn_deck.get_last())
                self.game_state.drawn_deck.get_last().rect = self.deck_button.rect.move(
                    60, 0
                )
                for i, card in enumerate(self.game_state.get_current_player().cards):
                    card.rect.center = (50 + 50 * i, 550)
                    card.off("click")
                    card.on("click", self.handle_click_card(card))"""

    def handle_flow(self, event: TransitionEvent) -> None:
        match event.transition_from, event.transition_to:
            case _, "TurnStartFlowNode":
                self.add_children(self.game_state.get_current_player().cards)
                self.add_child(self.game_state.drawn_deck.get_last())
                self.game_state.drawn_deck.get_last().rect = self.deck_button.rect.move(
                    60, 0
                )
                for j in range(0, self.player_count):
                    for i, card in enumerate(self.game_state.players[j].cards):
                        if j == 0:
                            card.rect.center = (50 + 50 * i, 550)
                            card.off("click")
                            card.on("click", self.handle_click_card(card))
                        else:
                            card.rect = pygame.Rect(0, 0, 12, 20)
                            card.rect.center = (610 + 13 * i, (j - 1) * 100 + 60)

    def handle_click_card(self, card: Card) -> None:
        def handler(event: Event) -> None:
            if card.ability is None:
                self.flow.transition_to(NumberCardFlowNode(self.game_state, card))
            else:
                self.flow.transition_to(AbilityCardFlowNode(self.game_state, card))

        return handler
