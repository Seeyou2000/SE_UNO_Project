import pygame

from engine.button import Button
from engine.event import Event
from engine.layout import LayoutAnchor
from engine.scene import Scene
from engine.world import World
from game.constant import NAME, UI_FONT_BOLD_PATH
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
from game.ingame.otherplayerentry import OtherPlayerEntry


class InGameScene(Scene):
    def __init__(
        self, world: World, player_count: int, self_player_index: int = 0
    ) -> None:
        super().__init__(world)

        from game.menu.menuscene import MenuScene

        self.player_count = player_count
        self.self_player_index = self_player_index
        self.name = NAME

        self.font = pygame.font.Font(UI_FONT_BOLD_PATH, 20)

        menu_button = Button(
            "Back to menu",
            pygame.Rect(10, 10, 180, 60),
            self.font,
            lambda _: self.world.director.change_scene(MenuScene(self.world)),
        )
        self.add_child(menu_button)

        self.other_player_entries = []

        self.game_state = GameState()
        self.on("card_played", self.handle_card_played)

        self.flow = GameFlowMachine()
        self.flow.events.on(GameFlowMachineEventType.TRANSITION, self.handle_flow)
        self.flow.transition_to(
            GameStartFlowNode(
                self.game_state, [Player(name) for name in NAME[:player_count]]
            )
        )

    def update(self, dt: float) -> None:
        super().update(dt)

        my_cards = self.game_state.players[self.self_player_index].cards
        # print(len(cards))
        for i, card in enumerate(my_cards):
            # 일단 트윈 대신 감속 공식으로 애니메이션 구현
            existing_margin = self.layout.get_constraint(card).margin
            target = pygame.Vector2(
                (i - len(my_cards) / 2 + 1) * 600 / len(my_cards), -10
            )
            self.layout.update_constraint(
                card,
                margin=existing_margin + (target - existing_margin) * dt * 10,
            )

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)

    def handle_flow(self, event: TransitionEvent) -> None:
        match event.transition_from, event.transition_to:
            case "GameStartFlowNode", "TurnStartFlowNode":  # 맨 처음
                turn = self.game_state.turn
                players = self.game_state.players

                self.place_decks()

                print(f"턴 시작: {turn.current}")

                # 모든 플레이어의 카드를 scene에 추가

                # 현재 플레이어
                me = players[self.self_player_index]
                cards = me.cards
                for card in cards:
                    card.on("click", self.create_card_click_handler(card))
                    self.layout.add(
                        card,
                        LayoutAnchor.BOTTOM_CENTER,
                        pygame.Vector2(0, 0),
                    )

                    self.add_child(card)

                # 다른 플레이어
                layout_infos = [  # 플레이어 위치에서 시계방향으로
                    (LayoutAnchor.MIDDLE_LEFT, pygame.Vector2(0, 70)),
                    (LayoutAnchor.MIDDLE_LEFT, pygame.Vector2(0, -70)),
                    (LayoutAnchor.TOP_CENTER, pygame.Vector2(0, 10)),
                    (LayoutAnchor.MIDDLE_RIGHT, pygame.Vector2(0, -70)),
                    (LayoutAnchor.MIDDLE_RIGHT, pygame.Vector2(0, 70)),
                ]
                fill_order = [  # 적 1명에서 5명까지
                    [2],
                    [1, 3],
                    [1, 2, 3],
                    [0, 1, 2, 3],
                    [0, 1, 2, 3, 4],
                ]

                other_players = (
                    players[: self.self_player_index]
                    + players[self.self_player_index + 1 :]
                )

                for i, player in enumerate(other_players):
                    entry = OtherPlayerEntry(pygame.Vector2(250, 150), player)
                    self.other_player_entries.append(entry)
                    self.add_child(entry)
                    layout_info = layout_infos[fill_order[len(other_players) - 1][i]]
                    self.layout.add(entry, layout_info[0], layout_info[1])

            case _, "TurnStartFlowNode":
                if self.self_player_index == self.game_state.turn.current:
                    me = self.game_state.get_current_player()
                    cards = me.cards
                    for card in cards:
                        card.on("click", self.create_card_click_handler(card))

            case "TurnStartFlowNode", _:  # 플레이어가 동작을 한 후
                for card in self.game_state.players[self.self_player_index].cards:
                    card.off("click")

            case "NumberCardFlowNode" | "AbilityCardFlowNode", _:  # 구조 바꾸면 바뀌어야 함
                last_drawn_card = self.game_state.drawn_deck.get_last()
                self.add_child(last_drawn_card)
                self.layout.add(
                    last_drawn_card, LayoutAnchor.CENTER, pygame.Vector2(Card.WIDTH, 0)
                )

    def create_card_click_handler(self, card: Card) -> None:
        def handler(event: Event) -> None:
            if card.ability is None:
                self.flow.transition_to(NumberCardFlowNode(self.game_state, card))
            else:
                self.flow.transition_to(AbilityCardFlowNode(self.game_state, card))

        return handler

    def place_decks(self) -> None:
        deck_button = Button(
            "",
            pygame.Rect(0, 0, Card.WIDTH, Card.HEIGHT),
            self.font,
            lambda _: self.flow.transition_to(DrawCardFlowNode(self.game_state)),
        )
        self.add_child(deck_button)
        self.layout.add(
            deck_button, LayoutAnchor.CENTER, pygame.Vector2(-Card.WIDTH, 0)
        )

        # 덱에서 한 장 열어놓기
        last_drawn_card = self.game_state.drawn_deck.get_last()
        self.add_child(last_drawn_card)
        self.layout.add(
            last_drawn_card, LayoutAnchor.CENTER, pygame.Vector2(Card.WIDTH, 0)
        )

    def handle_card_played(self, event: Event) -> None:
        card: Card = event.data["card"]
        self.remove_child(card)
        self.layout.remove(card)
