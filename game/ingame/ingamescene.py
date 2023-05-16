import random
from datetime import datetime

import pygame

from engine.button import Button, ButtonSurfaces, SpriteButton
from engine.events.emitter import EventHandler
from engine.events.event import Event
from engine.layout import (
    LayoutAnchor,
    LayoutConstraint,
    update_horizontal_linear_overlapping_layout,
)
from engine.scene import Scene
from engine.sprite import Sprite
from engine.text import Text
from engine.world import World
from game.constant import COLORS, NAME, AbilityType
from game.font import FontType, get_font
from game.gameplay.aiplayer import AIPlayer
from game.gameplay.card import Card
from game.gameplay.cardentitiy import CardEntity, create_card_sprite
from game.gameplay.flow.changefieldcolor import ChangeFieldColorFlowNode
from game.gameplay.flow.discardcard import DiscardCardFlowNode
from game.gameplay.flow.drawcard import DrawCardFlowNode
from game.gameplay.flow.endability import EndAbilityFlowNode
from game.gameplay.flow.gameend import GameEndFlowNode
from game.gameplay.flow.gameflowmachine import (
    GameFlowMachine,
    GameFlowMachineEventType,
    TransitionEvent,
    on_transition,
)
from game.gameplay.flow.prepare import PrepareFlowNode
from game.gameplay.flow.startturn import StartTurnFlowNode
from game.gameplay.flow.useability import UseAbilityFlowNode
from game.gameplay.flow.validatecard import ValidateCardFlowNode
from game.gameplay.gamestate import GameState, GameStateEventType
from game.gameplay.player import Player
from game.gameplay.timer import Timer
from game.ingame.changecolormodal import ChangeColorModal
from game.ingame.nowcolorindicator import NowColorIndicator
from game.ingame.otherplayerentry import OtherPlayerEntry
from game.ingame.timerindicator import TimerIndicator
from game.ingame.turndirectionindicator import TurnDirectionIndicator


class InGameScene(Scene):
    discarding_card_entities: list[CardEntity]
    delay_timers: list[Timer]

    def __init__(
        self,
        world: World,
        player_count: int,
        more_ability_cards: bool = False,
        give_every_card_to_players: bool = False,
        random_color: bool = False,
        random_turn: bool = False,
        my_player_index: int = 0,
    ) -> None:
        super().__init__(world)

        self.deck_button = None
        self.more_ability_cards = more_ability_cards
        self.give_every_card_to_players = give_every_card_to_players
        self.random_color = random_color
        self.random_turn = random_turn
        self.earned_card_idx_in_this_frame = 0

        self.my_player_index = my_player_index

        self.font = get_font(FontType.UI_BOLD, 20)
        self.other_player_entries = []
        self.my_card_entities = []
        self.discarding_card_entities = []
        self.delay_timers = []
        self.game_state = GameState()
        self.screen_size = self.world.get_rect()
        self.mytimer_display = None
        self.card_effect_timer = Timer(2)
        self.text_ability = Text(
            "", pygame.Vector2(), get_font(FontType.UI_BOLD, 25), pygame.Color("black")
        )
        self.card_effect_timer.on("tick", self.hide_text_ability)
        self.layout.add(self.text_ability, LayoutAnchor.CENTER, pygame.Vector2(0, -115))
        self.change_color_modal = None

        self.setup_base()
        self.flow = GameFlowMachine()
        transition_handlers = [
            lambda event: print(
                f"\nFLOW: {type(event.before).__name__} -> {type(event.after).__name__}"  # noqa: E501
            ),
            on_transition(PrepareFlowNode, None, self.setup_players),
            on_transition(
                UseAbilityFlowNode,
                ChangeFieldColorFlowNode,
                self.show_change_color_modal,
            ),
            on_transition(
                ChangeFieldColorFlowNode,
                EndAbilityFlowNode,
                self.remove_change_color_modal,
            ),
            on_transition(None, StartTurnFlowNode, self.handle_start_turn),
            on_transition(
                None,
                StartTurnFlowNode,
                lambda event: print(
                    f"턴 시작: {self.game_state.get_current_player().name}"
                ),
            ),
            on_transition(None, StartTurnFlowNode, self.handle_color_change),
            on_transition(None, StartTurnFlowNode, self.handle_reverse_change),
            on_transition(DiscardCardFlowNode, None, self.place_discarded_card),
            on_transition(None, GameEndFlowNode, self.end_game),
            on_transition(None, GameEndFlowNode, self.back_to_menu),
        ]
        self.flow.events.on(GameFlowMachineEventType.TRANSITION, transition_handlers)
        self.flow.events.on(
            GameFlowMachineEventType.CARD_PLAYED, self.handle_card_played
        )
        self.flow.transition_to(
            PrepareFlowNode(
                self.game_state,
                [Player(name) for name in NAME[:player_count]],
                self.more_ability_cards,
                self.give_every_card_to_players,
            )
        )

        self.world.settings.on("change", lambda _: self.update_cards_colorblind)

        self.on("keydown", self.handle_keydown)
        self.flow.events.on(
            GameFlowMachineEventType.GAME_END, self.check_win_less_10turn
        )

    def handle_color_change(self, event: TransitionEvent) -> None:
        is_turn_five = self.game_state.turn.total % 5 == 0
        if self.random_color and is_turn_five:
            self.game_state.change_card_color(random.choice(COLORS))

    def handle_reverse_change(self, event: TransitionEvent) -> None:
        is_turn_five = self.game_state.turn.total % 5 == 0
        if self.random_turn and is_turn_five:
            self.game_state.reverse_turn_direction()

    def handle_keydown(self, event: Event) -> None:
        key: int = event.data["key"]
        # 우노
        if key == self.world.settings.keymap.get("draw_card"):
            self.try_draw()
        elif key == self.world.settings.keymap.get("uno"):
            self.flow.check_uno(self.game_state, self.get_me())

        # 색 선택
        from game.gameplay.flow.endability import EndAbilityFlowNode

        if self.change_color_modal is None:
            return
        if self.has_child(self.change_color_modal):
            card: Card = self.flow._current_node.card  # noqa: SLF001
            match key:
                case pygame.K_1:
                    self.game_state.change_card_color("red")
                    self.flow.transition_to(
                        EndAbilityFlowNode(
                            self.game_state,
                            card,
                            self.flow._current_node.is_prepare,  # noqa: SLF001
                        )
                    )
                case pygame.K_2:
                    self.game_state.change_card_color("yellow")
                    self.flow.transition_to(
                        EndAbilityFlowNode(
                            self.game_state,
                            card,
                            self.flow._current_node.is_prepare,  # noqa: SLF001
                        )
                    )
                case pygame.K_3:
                    self.game_state.change_card_color("green")
                    self.flow.transition_to(
                        EndAbilityFlowNode(
                            self.game_state,
                            card,
                            self.flow._current_node.is_prepare,  # noqa: SLF001
                        )
                    )
                case pygame.K_4:
                    self.game_state.change_card_color("blue")
                    self.flow.transition_to(
                        EndAbilityFlowNode(
                            self.game_state,
                            card,
                            self.flow._current_node.is_prepare,  # noqa: SLF001
                        )
                    )

    def update(self, dt: float) -> None:
        super().update(dt)
        self.game_state.turn_timer.update(dt)
        for timer in self.delay_timers:
            timer.update(dt)
            if not timer.enabled:
                self.delay_timers.remove(timer)

        self.earned_card_idx_in_this_frame = 0

        for ai in self.ai:
            ai.update(dt)

        self.card_effect_timer.update(dt)

        update_horizontal_linear_overlapping_layout(
            objects=self.my_card_entities,
            layout=self.layout,
            dt=dt,
            max_width=800,
            gap=24,
            offset_retriever=lambda obj, _: pygame.Vector2(
                0,
                -30
                if self.is_my_turn() and obj.has_focus
                else -4
                if self.is_my_turn()
                else 12,
            ),
        )
        self.update_discarding_card_animation(dt)

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)

    def update_discarding_card_animation(self, dt: float) -> None:
        screen_center = pygame.Vector2(self.screen_size.size) / 2
        for card_entity in self.discarding_card_entities:
            target_pos = screen_center + self.discard_position
            card_center = pygame.Vector2(card_entity.rect.center)
            card_entity.rect.center = card_center + (target_pos - card_center) * dt * 10
            if card_center.distance_to(target_pos) < 10:
                self.discarding_card_entities.remove(card_entity)
                self.remove_child(card_entity)

    def create_card_click_handler(self, card: Card) -> EventHandler:
        def handler(event: Event) -> None:
            if self.get_me() is self.game_state.get_current_player() and isinstance(
                self.flow.current_node, StartTurnFlowNode
            ):
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
            lambda _: self.check_uno_and_play_sound(self.game_state, self.get_me()),
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

        now_color_indicator = NowColorIndicator(self.game_state, self.world.settings)
        self.add_child(now_color_indicator)
        self.layout.add(
            now_color_indicator, LayoutAnchor.CENTER, pygame.Vector2(130, -40)
        )
        screenx = self.world.get_rect().right
        screeny = self.world.get_rect().bottom
        pygame.draw.rect(
            self.world.screen, "#FDE3BC", [screenx - 400, screeny - 150, 400, 150]
        )

    def setup_players(self, event: TransitionEvent) -> None:
        self.place_decks()
        self.setup_me()
        self.setup_other_players()

    def setup_me(self) -> None:
        me = self.get_me()

        self.game_state.on(
            GameStateEventType.PLAYER_EARNED_CARD, self.handle_me_card_earned
        )

        # 카드
        for card in me.cards:
            self.add_card_entity(
                card,
                is_mine=True,
                delay=0,
                layout_constaint=LayoutConstraint(
                    LayoutAnchor.BOTTOM_CENTER, pygame.Vector2(0, 0)
                ),
            )

        # 타이머
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
            pygame.Vector2(100, -175),
        )
        # 본인 이름 출력
        name_font = get_font(FontType.UI_BOLD, 20)
        name_text = Text(
            me.name, pygame.Vector2(50, 10), name_font, pygame.Color("black")
        )
        self.add_child(name_text)
        self.layout.add(name_text, LayoutAnchor.BOTTOM_CENTER, pygame.Vector2(0, -175))

        # 우노
        self.my_uno_text = Text(
            "UNO",
            pygame.Vector2(50, 10),
            get_font(FontType.UI_BOLD, 20),
            pygame.Color("gray"),
        )
        self.add_child(self.my_uno_text)
        self.layout.add(
            self.my_uno_text, LayoutAnchor.BOTTOM_CENTER, pygame.Vector2(-100, -175)
        )

        def update_uno_text(event: Event) -> None:
            self.my_uno_text.set_color(
                pygame.Color("blue")
                if self.get_me().is_unobutton_clicked
                else pygame.Color("gray")
            )

        self.game_state.on(
            GameStateEventType.PLAYER_UNO_STATUS_CHANGED, update_uno_text
        )

    def setup_other_players(self) -> None:
        players = self.game_state.players
        me = self.get_me()
        self.ai = [
            AIPlayer(player, self.flow, self.game_state)
            for player in filter(lambda x: x is not me, players)
        ]
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
                pygame.Vector2(300, 150),
                player,
                layout_info[0],
                self.game_state.turn_timer,
                self.flow,
                self.deck_button,
            )
            self.other_player_entries.append(entry)
            self.game_state.on(
                GameStateEventType.PLAYER_EARNED_CARD, entry.handle_card_earned
            )
            self.game_state.on(
                GameStateEventType.PLAYER_UNO_STATUS_CHANGED, entry.handle_uno_clicked
            )
            self.flow.events.on(
                GameFlowMachineEventType.CARD_PLAYED, entry.handle_card_played
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

        deck_button_sprite = create_card_sprite(
            color="red", is_back=True, is_colorblind=False, is_small=False
        )
        deck_button_surfaces = ButtonSurfaces(
            deck_button_sprite.image,
            deck_button_sprite.image,
            deck_button_sprite.image,
        )
        deck_button = SpriteButton(deck_button_surfaces, lambda _: self.try_draw())
        self.deck_button = deck_button
        self.add_child(deck_button)
        self.layout.add(
            deck_button,
            LayoutAnchor.CENTER,
            self.discard_position - pygame.Vector2(CardEntity.WIDTH + 20, 0),
        )

        # 덱에서 한 장 열어놓기
        self.add_card_entity(
            self.game_state.discard_pile.get_last(),
            is_mine=False,
            delay=0,
            layout_constaint=LayoutConstraint(
                LayoutAnchor.CENTER, self.discard_position
            ),
        )

        self.text_cardnum = Text(
            str(self.game_state.game_deck.get_card_amount()),
            pygame.Vector2(),
            get_font(FontType.UI_BOLD, 23),
            pygame.Color("white"),
        )
        self.layout.add(
            self.text_cardnum,
            LayoutAnchor.CENTER,
            self.discard_position - pygame.Vector2(CardEntity.WIDTH + 20, 50),
        )
        self.add_child(self.text_cardnum)

    def handle_start_turn(self, event: TransitionEvent) -> None:
        if self.is_my_turn():
            if self.mytimer_display is not None and self.has_child(
                self.mytimer_display
            ):
                self.remove_child(self.mytimer_display)
            self.add_child(self.mytimer_display)
        else:
            if self.has_child(self.mytimer_display):
                self.remove_child(self.mytimer_display)
        self.text_cardnum.set_text(str(self.game_state.game_deck.get_card_amount()))

    def place_discarded_card(self, event: TransitionEvent) -> None:
        self.remove_card_entity(self.game_state.discard_pile.cards[-2])
        self.add_card_entity(
            self.game_state.discard_pile.get_last(),
            is_mine=False,
            delay=0,
            layout_constaint=LayoutConstraint(
                LayoutAnchor.CENTER, self.discard_position
            ),
        )

    def handle_card_played(self, event: Event) -> None:
        card: Card = event.data["card"]
        player: Player = event.data["player"]

        removed = self.remove_card_entity(card)
        start_position: tuple[float, float]
        if removed is not None:
            start_position = removed.absolute_rect.center
        else:
            other_player_entry = self.other_player_entries[0]
            for entry in self.other_player_entries:
                if entry.player is player:
                    other_player_entry = entry
                    break
            start_position = other_player_entry.card_sprites[-1].absolute_rect.center

        animating_card_entity = CardEntity(card)
        animating_card_entity.set_colorblind(self.world.settings.is_colorblind)
        animating_card_entity.rect.center = start_position
        self.discarding_card_entities.append(animating_card_entity)
        self.add_child(animating_card_entity)
        self.world.audio_player.play_effect_card_playing()

        # 능력카드 발생시 화면에 띄우기
        if card.ability is not None:
            match card.ability:
                case AbilityType.GIVE_TWO_CARDS:
                    self.text_ability.set_text(f"GIVE TWO CARDS by {player.name}")
                case AbilityType.GIVE_FOUR_CARDS:
                    self.text_ability.set_text(f"GIVE FOUR CARDS by {player.name}")
                case AbilityType.ABSOULTE_ATTACK:
                    self.text_ability.set_text(f"ABSOLUTE ATTACK by {player.name}")
                case AbilityType.ABSOULTE_PROTECT:
                    self.text_ability.set_text(f"ABSOLUTE PROTECT by {player.name}")
                case AbilityType.SKIP_ORDER:
                    self.text_ability.set_text(f"SKIP by {player.name}")
                case AbilityType.REVERSE_ORDER:
                    self.text_ability.set_text(f"REVERSE by {player.name}")
                case AbilityType.CHANGE_CARD_COLOR:
                    self.text_ability.set_text(f"CARD COLOR CHANGE by {player.name}")
            if not self.has_child(self.text_ability):
                self.add_child(self.text_ability)
            self.card_effect_timer.reset()

    def handle_me_card_earned(self, event: Event) -> None:
        card: Card = event.data["card"]
        player: Player = event.data["player"]

        self.earned_card_idx_in_this_frame += 1

        self.text_cardnum.set_text(str(self.game_state.game_deck.get_card_amount()))
        if player is not self.get_me():
            return

        deck_margin = self.layout.get_constraint(self.deck_button).margin
        self.add_card_entity(
            card,
            is_mine=True,
            delay=0.1 * self.earned_card_idx_in_this_frame,
            layout_constaint=LayoutConstraint(
                LayoutAnchor.BOTTOM_CENTER,
                pygame.Vector2(
                    deck_margin.x,
                    -self.deck_button.absolute_rect.centery + deck_margin.y,
                ),
            ),
        )

    def update_cards_colorblind(self) -> None:
        for child in self._children:
            if isinstance(child, CardEntity):
                child.set_colorblind(self.world.settings.is_colorblind)

    def try_draw(self) -> None:
        print(self.is_my_turn(), isinstance(self.flow.current_node, StartTurnFlowNode))
        if self.is_my_turn() and isinstance(self.flow.current_node, StartTurnFlowNode):
            self.flow.transition_to(DrawCardFlowNode(self.game_state))

    def end_game(self, event: Event) -> None:
        won_player: Player
        for player in self.game_state.players:
            if len(player.cards) == 0:
                won_player = player
        if won_player is self.get_me():
            self.game_result = f"{won_player.name} Win!"
        else:
            self.game_result = f"Lose! {won_player.name} Won!"

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

    def back_to_menu(self, event: Event) -> None:
        from game.menu.menuscene import MenuScene

        menu_button = Button(
            "Back to menu",
            pygame.Rect(10, 10, 180, 60),
            self.font,
            lambda _: self.world.director.change_scene(MenuScene(self.world)),
        )
        self.add_child(menu_button)
        self.layout.add(menu_button, LayoutAnchor.CENTER, pygame.Vector2(0, 150))

    def hide_text_ability(self, event: Event) -> None:
        if self.has_child(self.text_ability):
            self.remove_child(self.text_ability)

    # utils
    def get_me(self) -> Player:
        return self.game_state.players[self.my_player_index]

    def is_my_turn(self) -> bool:
        return self.game_state.get_current_player() == self.get_me()

    def show_change_color_modal(self, event: TransitionEvent) -> None:
        self.change_color_modal = ChangeColorModal(
            self.game_state,
            self.flow,
            self.world.settings,
            self.flow.current_node.is_prepare,
        )
        self.layout.add(
            self.change_color_modal, LayoutAnchor.CENTER, pygame.Vector2(0, 0)
        )
        self.add_child(self.change_color_modal)

    def remove_change_color_modal(self, event: TransitionEvent) -> None:
        self.remove_child(self.change_color_modal)

    def add_card_entity(
        self,
        card: Card,
        is_mine: bool,
        delay: float,
        layout_constaint: LayoutConstraint | None = None,
    ) -> CardEntity:
        card_entity = CardEntity(card)
        card_entity.set_colorblind(self.world.settings.is_colorblind)
        if is_mine:
            delay_timer = Timer(delay)
            delay_timer.on("tick", self.append_card_animation(card_entity))
            delay_timer.update(0)
            self.delay_timers.append(delay_timer)
            card_entity.on("click", self.create_card_click_handler(card))
            card_entity.set_colorblind(self.world.settings.is_colorblind)
            self.focus_controller.add(card_entity)
            card_entity.on("focus", self.handle_focus_sound)
        else:
            self.add_child(card_entity)
            self.set_order(card_entity, 4)

        if layout_constaint is not None:
            self.layout.add(
                card_entity, layout_constaint.anchor, layout_constaint.margin
            )

        return card_entity

    def append_card_animation(self, card_entity: CardEntity) -> EventHandler:
        def handler(event: Event) -> None:
            self.add_child(card_entity)
            self.my_card_entities.append(card_entity)

        return handler

    def remove_card_entity(self, card: Card) -> CardEntity | None:
        for child in self._children:
            if isinstance(child, CardEntity) and child.card is card:
                self.remove_child(child)
                if child in self.my_card_entities:
                    self.my_card_entities.remove(child)
                    self.focus_controller.remove(child)
                return child
        return None
        return None

    def check_uno_and_play_sound(
        self, game_state: GameState, pressed_player: Player
    ) -> None:
        self.flow.check_uno(game_state, pressed_player)
        if pressed_player is self.get_me():
            self.world.audio_player.play_effect_uno_clicked()

    def handle_focus_sound(self, event: Event) -> None:
        self.world.audio_player.play_effect_card_sliding()

    def check_win_less_10turn(self, event: Event) -> None:
        if event.data["turn"] <= 10 and event.data["player"] is self.get_me():
            self.world.achievements.set_values(
                win_less_10turn=[True, f"{datetime.now()}"]
            )
