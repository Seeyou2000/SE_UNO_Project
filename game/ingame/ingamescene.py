import pygame

from engine.button import BaseButton, Button, ButtonSurfaces, SpriteButton
from engine.event import Event, EventHandler
from engine.layout import LayoutAnchor
from engine.scene import Scene
from engine.sprite import Sprite
from engine.world import World
from game.constant import NAME
from game.font import FontType, get_font
from game.gameplay.card import Card
from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.flow.discardcard import DiscardCardFlowNode
from game.gameplay.flow.drawcard import DrawCardFlowNode
from game.gameplay.flow.gameflowmachine import (
    GameFlowMachine,
    GameFlowMachineEventType,
    TransitionEvent,
)
from game.gameplay.flow.prepare import PrepareFlowNode
from game.gameplay.flow.startturn import StartTurnFlowNode
from game.gameplay.flow.validatecard import ValidateCardFlowNode
from game.gameplay.gamestate import GameState, GameStateEventType
from game.gameplay.player import Player
from game.ingame.otherplayerentry import OtherPlayerEntry
from game.ingame.turndirectionindicator import TurnDirectionIndicator


class InGameScene(Scene):
    def __init__(
        self, world: World, player_count: int, my_player_index: int = 0
    ) -> None:
        super().__init__(world)

        self.my_player_index = my_player_index

        self.font = get_font(FontType.UI_BOLD, 20)
        self.other_player_entries = []
        self.game_state = GameState()

        self.setup_base()

        self.flow = GameFlowMachine()
        transition_handlers = [
            lambda event: print(
                f"\nFLOW: {type(event.before).__name__} -> {type(event.after).__name__}"  # noqa: E501
            ),
            self.on_transition(PrepareFlowNode, None, self.setup_players),
            self.on_transition(None, StartTurnFlowNode, self.activate_my_card_handlers),
            self.on_transition(
                None,
                StartTurnFlowNode,
                lambda event: print(
                    f"턴 시작: {self.game_state.get_current_player().name}"
                ),
            ),
            self.on_transition(DiscardCardFlowNode, None, self.place_discarded_card),
        ]
        self.flow.events.on(GameFlowMachineEventType.TRANSITION, transition_handlers)
        self.flow.events.on(
            GameFlowMachineEventType.CARD_PLAYED, self.handle_card_played
        )
        self.flow.transition_to(
            PrepareFlowNode(
                self.game_state, [Player(name) for name in NAME[:player_count]]
            )
        )

        self.world.settings.on("change", lambda _: self.update_cards_colorblind)

    def update(self, dt: float) -> None:
        super().update(dt)

        my_cards = self.get_me().cards
        # print(len(cards))
        for i, card in enumerate(my_cards):
            # 일단 트윈 대신 감속 공식으로 애니메이션 구현
            constraint = self.layout.get_constraint(card)
            if constraint is None:
                continue
            existing_margin = constraint.margin
            cards_len = len(my_cards)
            gap = 24
            delta = Card.WIDTH - gap
            x = (
                (i - cards_len / 2.0) * 800 / cards_len + gap
                if cards_len > 10
                else (i - 1 - cards_len / 2.0) * delta + Card.WIDTH + gap / 2
            )
            y = (
                -30
                if self.is_my_turn() and card.is_hovered
                else -4
                if self.is_my_turn()
                else 12
            )
            target = pygame.Vector2(x, y)
            self.layout.update_constraint(
                card,
                margin=existing_margin + (target - existing_margin) * dt * 10,
            )

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)

    def on_transition(
        self,
        before: type[AbstractGameFlowNode] | None,
        after: type[AbstractGameFlowNode] | None,
        handler: EventHandler,
    ) -> EventHandler:
        def transition_handler(event: TransitionEvent) -> None:
            satisfies_before = before is None or isinstance(event.before, before)
            satisfies_after = after is None or isinstance(event.after, after)
            if satisfies_before and satisfies_after:
                handler(event)

        return transition_handler

    def create_card_click_handler(self, card: Card) -> EventHandler:
        def handler(event: Event) -> None:
            if self.get_me() is self.game_state.get_current_player():
                print(f"ACTION: Use card {card}")
                self.flow.transition_to(ValidateCardFlowNode(self.game_state, card))

        return handler

    def setup_base(self) -> None:
        from game.menu.menuscene import MenuScene

        menu_button = Button(
            "Back to menu",
            pygame.Rect(10, 10, 180, 60),
            self.font,
            lambda _: self.world.director.change_scene(MenuScene(self.world)),
        )
        self.add_child(menu_button)

        center_base_sprite = Sprite(
            pygame.image.load("resources/images/center-base.png")
        )
        self.add_child(center_base_sprite)
        self.layout.add(center_base_sprite, LayoutAnchor.CENTER, pygame.Vector2(0, 0))

        uno_button = SpriteButton(
            ButtonSurfaces(
                pygame.image.load("resources/images/uno-button-normal.png"),
                pygame.image.load("resources/images/uno-button-hover.png"),
                pygame.image.load("resources/images/uno-button-pressed.png"),
            )
        )
        self.add_child(uno_button)
        self.layout.add(uno_button, LayoutAnchor.CENTER, pygame.Vector2(191, 90))

        self.turn_direction_indicator = TurnDirectionIndicator()
        self.game_state.on(
            GameStateEventType.TURN_DIRECTION_REVERSE,
            lambda _: self.turn_direction_indicator.set_direction(
                self.game_state.turn.is_clockwise
            ),
        )
        self.add_child(self.turn_direction_indicator)
        self.layout.add(
            self.turn_direction_indicator, LayoutAnchor.CENTER, pygame.Vector2(0, -150)
        )

    def setup_players(self, event: TransitionEvent) -> None:
        players = self.game_state.players

        self.place_decks()

        # 모든 플레이어의 카드를 scene에 추가

        # 현재 플레이어
        me = self.get_me()
        self.game_state.on(
            GameStateEventType.PLAYER_EARNED_CARD, self.handle_me_card_earned
        )
        cards = me.cards
        for card in cards:
            self.layout.add(
                card,
                LayoutAnchor.BOTTOM_CENTER,
                pygame.Vector2(0, 0),
            )

            self.add_child(card)

        self.update_cards_colorblind()

        # 다른 플레이어
        layout_infos = [  # 플레이어 위치에서 시계방향으로
            (LayoutAnchor.MIDDLE_LEFT, pygame.Vector2(0, 80)),
            (LayoutAnchor.MIDDLE_LEFT, pygame.Vector2(0, -80)),
            (LayoutAnchor.TOP_CENTER, pygame.Vector2(0, 10)),
            (LayoutAnchor.MIDDLE_RIGHT, pygame.Vector2(0, -80)),
            (LayoutAnchor.MIDDLE_RIGHT, pygame.Vector2(0, 80)),
        ]
        fill_order = [  # 적 1명에서 5명까지
            [2],
            [1, 3],
            [1, 2, 3],
            [0, 1, 2, 3],
            [0, 1, 2, 3, 4],
        ]

        other_players = (
            players[: self.my_player_index] + players[self.my_player_index + 1 :]
        )

        for i, player in enumerate(other_players):
            layout_info = layout_infos[fill_order[len(other_players) - 1][i]]

            entry = OtherPlayerEntry(pygame.Vector2(250, 150), player, layout_info[0])
            self.other_player_entries.append(entry)
            self.game_state.on(
                GameStateEventType.PLAYER_EARNED_CARD, entry.handle_card_earned
            )
            self.game_state.on(
                GameStateEventType.TURN_DIRECTION_REVERSE,
                entry.handle_turn_direction_reverse,
            )
            self.game_state.on(
                GameStateEventType.TURN_NEXT,
                entry.handle_next_turn,
            )
            entry.show_or_hide_indicators(self.game_state)
            self.add_child(entry)
            self.layout.add(entry, layout_info[0], layout_info[1])

    def place_decks(self) -> None:
        self.discard_position = pygame.Vector2(16, 0)

        deck_button = Button(
            "",
            pygame.Rect(0, 0, Card.WIDTH, Card.HEIGHT),
            self.font,
            lambda _: self.flow.transition_to(DrawCardFlowNode(self.game_state)),
        )
        self.add_child(deck_button)
        self.layout.add(
            deck_button,
            LayoutAnchor.CENTER,
            self.discard_position - pygame.Vector2(Card.WIDTH + 20, 0),
        )
        self.deck_button = deck_button

        # 덱에서 한 장 열어놓기
        last_drawn_card = self.game_state.discard_pile.get_last()
        self.add_child(last_drawn_card)
        self.layout.add(last_drawn_card, LayoutAnchor.CENTER, self.discard_position)

    def activate_my_card_handlers(self, event: TransitionEvent) -> None:
        if self.is_my_turn():
            me = self.game_state.get_current_player()
            cards = me.cards
            for card in cards:
                card.off("click")
                card.on("click", self.create_card_click_handler(card))

    def place_discarded_card(self, event: TransitionEvent) -> None:
        discarded_card = self.game_state.discard_pile.get_last()
        self.add_child(discarded_card)
        self.layout.add(discarded_card, LayoutAnchor.CENTER, self.discard_position)

    def handle_card_played(self, event: Event) -> None:
        card: Card = event.data["card"]
        self.remove_child(card)
        self.layout.remove(card)

    def handle_me_card_earned(self, event: Event) -> None:
        card: Card = event.data["card"]
        player: Player = event.data["player"]

        if player is not self.get_me():
            return

        self.add_child(card)
        card.set_colorblind(self.world.settings.is_colorblind)
        deck_margin = self.layout.get_constraint(self.deck_button).margin
        self.layout.add(
            card,
            LayoutAnchor.BOTTOM_CENTER,
            pygame.Vector2(
                deck_margin.x,
                -self.deck_button.absolute_rect.centery + deck_margin.y,
            ),
        )

    def update_cards_colorblind(self) -> None:
        for child in self._children:
            if isinstance(child, Card):
                child.set_colorblind(self.world.settings.is_colorblind)

    # utils
    def get_me(self) -> Player:
        return self.game_state.players[self.my_player_index]

    def is_my_turn(self) -> bool:
        return self.game_state.get_current_player() == self.get_me()
