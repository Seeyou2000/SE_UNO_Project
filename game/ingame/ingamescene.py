import pygame

from engine.button import BaseButton, Button, ButtonSurfaces, SpriteButton
from engine.event import Event, EventHandler
from engine.layout import LayoutAnchor
from engine.scene import Scene
from engine.sprite import Sprite
from engine.text import Text
from engine.world import World
from game.constant import NAME, ColorableAbilityType
from game.font import FontType, get_font
from game.gameplay.card import Card
from game.gameplay.cardentitiy import CardEntity
from game.gameplay.flow.abstractflownode import AbstractGameFlowNode
from game.gameplay.flow.discardcard import DiscardCardFlowNode
from game.gameplay.flow.drawcard import DrawCardFlowNode
from game.gameplay.flow.gameend import GameEndFlowNode
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
from game.gameplay.timer import Timer
from game.ingame.otherplayerentry import OtherPlayerEntry
from game.ingame.timerindicator import TimerIndicator
from game.ingame.turndirectionindicator import TurnDirectionIndicator


class InGameScene(Scene):
    def __init__(
        self, world: World, player_count: int, my_player_index: int = 0
    ) -> None:
        super().__init__(world)

        self.my_player_index = my_player_index

        self.font = get_font(FontType.UI_BOLD, 20)
        self.other_player_entries = []
        self.my_card_entities = []
        self.game_state = GameState()
        self.screen_size = self.world.get_rect()
        self.mytimer_display = None
        self.show_time = None
        self.text_ability = None

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
            self.on_transition(None, GameEndFlowNode, self.end_game),
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
        self.game_state.turn_timer.update(dt)
        if self.show_time is not None:
            self.show_time.update(dt)
            self._time, self._duration = self.show_time.get_time()
            if self._time >= self._duration:
                if self.text_ability is not None and self.has_child(self.text_ability):
                    self.remove_child(self.text_ability)

        my_cards = self.get_me().cards
        # print(len(cards))
        for i, card in enumerate(my_cards):
            # 일단 트윈 대신 감속 공식으로 애니메이션 구현
            card_entity = next(
                filter(lambda ce: ce.card is card, self.my_card_entities)
            )
            constraint = self.layout.get_constraint(card_entity)
            if constraint is None:
                continue
            existing_margin = constraint.margin
            cards_len = len(my_cards)
            gap = 24
            delta = CardEntity.WIDTH - gap
            x = (
                (i - cards_len / 2.0) * 800 / cards_len + gap
                if cards_len > 10
                else (i - 1 - cards_len / 2.0) * delta + CardEntity.WIDTH + gap / 2
            )
            y = (
                -30
                if self.is_my_turn() and card_entity.is_hovered
                else -4
                if self.is_my_turn()
                else 12
            )
            target = pygame.Vector2(x, y)
            self.layout.update_constraint(
                card_entity,
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
            ),
            lambda _: self.flow.is_uno(self.game_state, self.get_me())
            # gameflowmachine의 우노 판별 함수 호출
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
            card_entity = CardEntity(card)
            self.layout.add(
                card_entity,
                LayoutAnchor.BOTTOM_CENTER,
                pygame.Vector2(0, 0),
            )

            self.add_child(card_entity)
            self.my_card_entities.append(card_entity)

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

            entry = OtherPlayerEntry(
                pygame.Vector2(250, 150),
                player,
                layout_info[0],
                self.game_state.turn_timer,
            )
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

    def cards_amount(self) -> None:
        print(self.leftcards)  # 화면에 출력 필요

    def place_decks(self) -> None:
        self.discard_position = pygame.Vector2(16, 0)

        deck_button = Button(
            "",
            pygame.Rect(0, 0, CardEntity.WIDTH, CardEntity.HEIGHT),
            self.font,
            lambda _: self.flow.transition_to(DrawCardFlowNode(self.game_state)),
        )
        self.add_child(deck_button)
        self.layout.add(
            deck_button,
            LayoutAnchor.CENTER,
            self.discard_position - pygame.Vector2(CardEntity.WIDTH + 20, 0),
        )
        self.deck_button = deck_button

        # 덱에서 한 장 열어놓기
        last_drawn_card_entity = CardEntity(self.game_state.discard_pile.get_last())
        self.add_child(last_drawn_card_entity)
        self.layout.add(
            last_drawn_card_entity, LayoutAnchor.CENTER, self.discard_position
        )

        self.text_cardnum = Text(
            str(self.game_state.game_deck.get_card_amount()),
            pygame.Vector2(),
            get_font(FontType.UI_BOLD, 23),
            pygame.Color("black"),
        )
        self.layout.add(
            self.text_cardnum,
            LayoutAnchor.CENTER,
            self.discard_position - pygame.Vector2(CardEntity.WIDTH + 20, 50),
        )
        self.add_child(self.text_cardnum)

    def activate_my_card_handlers(self, event: TransitionEvent) -> None:
        if self.is_my_turn():
            if self.mytimer_display is not None and self.has_child(
                self.mytimer_display
            ):
                self.remove_child(self.mytimer_display)
            self.mytimer_display = TimerIndicator(
                pygame.Rect(
                    0,
                    0,
                    20,
                    20,
                ),
                self.game_state.turn_timer,
            )
            self.layout.add(
                self.mytimer_display,
                LayoutAnchor.BOTTOM_CENTER,
                pygame.Vector2(0, -180),
            )
            self.add_child(self.mytimer_display)
            me = self.game_state.get_current_player()
            cards = me.cards
            for card in cards:
                for child in self._children:
                    if isinstance(child, CardEntity) and child.card is card:
                        child.off("click")
                        child.on("click", self.create_card_click_handler(card))
        else:
            if self.has_child(self.mytimer_display):
                self.remove_child(self.mytimer_display)

        self.text_cardnum.set_text(str(self.game_state.game_deck.get_card_amount()))

    def place_discarded_card(self, event: TransitionEvent) -> None:
        discarded_card_entity = CardEntity(self.game_state.discard_pile.get_last())
        self.add_child(discarded_card_entity)
        self.layout.add(
            discarded_card_entity, LayoutAnchor.CENTER, self.discard_position
        )

    def handle_card_played(self, event: Event) -> None:
        card: Card = event.data["card"]
        # 능력카드 발생시 이벤트 추가
        match card.ability:
            case ColorableAbilityType.GIVE_TWO_CARDS:
                self.text_ability = Text(
                    "Give Two cards",
                    pygame.Vector2(),
                    get_font(FontType.UI_BOLD, 25),
                    "black",
                )
                self.add_child(self.text_ability)
                self.layout.add(
                    self.text_ability, LayoutAnchor.CENTER, pygame.Vector2(0, -115)
                )
                self.show_time = Timer(2)
            case ColorableAbilityType.GIVE_FOUR_CARDS:
                self.text_ability = Text(
                    "Give Four cards",
                    pygame.Vector2(),
                    get_font(FontType.UI_BOLD, 25),
                    "black",
                )
                self.add_child(self.text_ability)
                self.layout.add(
                    self.text_ability, LayoutAnchor.CENTER, pygame.Vector2(0, -115)
                )
                self.show_time = Timer(2)
            case ColorableAbilityType.SKIP_ORDER:
                self.text_ability = Text(
                    "Skip",
                    pygame.Vector2(),
                    get_font(FontType.UI_BOLD, 25),
                    "black",
                )
                self.add_child(self.text_ability)
                self.layout.add(
                    self.text_ability, LayoutAnchor.CENTER, pygame.Vector2(0, -115)
                )
                self.show_time = Timer(2)
            case ColorableAbilityType.REVERSE_ORDER:
                self.text_ability = Text(
                    "Reverse",
                    pygame.Vector2(),
                    get_font(FontType.UI_BOLD, 25),
                    "black",
                )
                self.add_child(self.text_ability)
                self.layout.add(
                    self.text_ability, LayoutAnchor.CENTER, pygame.Vector2(0, -115)
                )
                self.show_time = Timer(2)
        for child in self._children:
            if isinstance(child, CardEntity) and child.card is card:
                self.remove_child(child)
                self.layout.remove(child)
                self.my_card_entities.remove(child)

    def handle_me_card_earned(self, event: Event) -> None:
        card: Card = event.data["card"]
        player: Player = event.data["player"]
        card_entity = CardEntity(card)

        self.text_cardnum.set_text(str(self.game_state.game_deck.get_card_amount()))
        if player is not self.get_me():
            return

        self.add_child(card_entity)
        card_entity.set_colorblind(self.world.settings.is_colorblind)
        deck_margin = self.layout.get_constraint(self.deck_button).margin
        self.layout.add(
            card_entity,
            LayoutAnchor.BOTTOM_CENTER,
            pygame.Vector2(
                deck_margin.x,
                -self.deck_button.absolute_rect.centery + deck_margin.y,
            ),
        )
        self.my_card_entities.append(card_entity)

    def update_cards_colorblind(self) -> None:
        for child in self._children:
            if isinstance(child, CardEntity):
                child.set_colorblind(self.world.settings.is_colorblind)

    def end_game(self, event: Event) -> None:
        if len(self.get_me().cards) == 0:
            self.game_result = "Win"
        else:
            self.game_result = "Lose"

        self.text_gameend = Text(
            self.game_result,
            pygame.Vector2(),
            get_font(FontType.YANGJIN, 50),
            pygame.Color("black"),
        )
        self.add_child(self.text_gameend)
        self.layout.add(
            self.text_gameend,
            LayoutAnchor.CENTER,
            pygame.Vector2(),
        )

    # utils
    def get_me(self) -> Player:
        return self.game_state.players[self.my_player_index]

    def is_my_turn(self) -> bool:
        return self.game_state.get_current_player() == self.get_me()
